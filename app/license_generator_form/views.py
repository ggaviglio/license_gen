from django.shortcuts import (
    render,
    render_to_response,
    redirect
)
from django.template import RequestContext
from django.http import HttpResponse
import alfresco_license_generators
from alfresco_license_generators import (
    JavaNotFoundError,
    GeneratorCommandError
)
from license_generator_form.license_request_unmarshal \
    import LicenseRequestUnmarshaller
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from license_generator_form.forms import AuthForm
from django.core.urlresolvers import reverse
from license_generator_form.models import License


def handler404(request):
    response = render_to_response(
        '404.html',
        {},
        context_instance=RequestContext(request)
    )
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response(
        '500.html',
        {},
        context_instance=RequestContext(request)
    )
    response.status_code = 500
    return response


@csrf_exempt
@login_required(login_url='/login/')
def home_page(request):
    return render(request, 'home.html')


def form_generate_alfresco(request):
    _form_validate_request(request)
    args = LicenseRequestUnmarshaller.alfresco(request.POST)
    License.objects.create(
        release_key= request.POST['release_key'],
        notes = request.POST['notes'],
        external_id = request.POST['external_id'],
        external_id_type = request.POST['external_id_type'],
        license_type = request.POST['license_types'],
        account_holder = request.POST['field_holder_name'],
        expiry_days = request.POST['field_days'],
        max_users =request.POST['field_max_users'],
        no_heartbeat = request.POST['field_no_heartbeat'],
        heartbeat_url = request.POST['field_heartbeat_url'],
        clustering_enabled = request.POST['field_cluster_enabled'],
        license_group = request.POST['field_license_group'],
        expiry_date = request.POST['field_end_date'],
        max_docs = request.POST['field_max_docs'],
        cloud_sync = request.POST['field_cloud_sync'],
        server_end_date = request.POST['field_ats_end_date'],
        crypto_doc = request.POST['field_cryptodoc_enabled']
    )
    return _form_generate(
        request,
        args,
        alfresco_license_generators.Alfresco.generate,
        'Alfresco'
    )


def form_generate_activiti(request):
    _form_validate_request(request)

    args = LicenseRequestUnmarshaller.activiti(request.POST)

    return _form_generate(
        request,
        args,
        alfresco_license_generators.Activiti.generate,
        'Activiti'
    )


@csrf_exempt
def rest_generate_alfresco(request):
    error_status_code = _rest_validate_request(request)
    if error_status_code:
        return HttpResponse(content="", status=error_status_code)

    args = LicenseRequestUnmarshaller.alfresco(
        json.loads(request.body.decode('UTF-8'))
    )
    return _rest_generate(
        request,
        args,
        alfresco_license_generators.Alfresco.generate
    )


@csrf_exempt
def rest_generate_activiti(request):
    error_status_code = _rest_validate_request(request)
    if error_status_code:
        return HttpResponse(content="", status=error_status_code)
    try:
        args = LicenseRequestUnmarshaller.activiti(
            json.loads(request.body.decode('UTF-8'))
        )
    except Exception as e:
        message = e
        status_code = 401

        message = {u"error_message": str(message)}
        return HttpResponse(
            content=json.dumps(message),
            content_type="application/json",
            status=status_code
        )

    return _rest_generate(
        request,
        args,
        alfresco_license_generators.Activiti.generate
    )


def _form_validate_request(request):
    if not request.method == 'POST':
        return redirect('/')


def _rest_validate_request(request):
    if not request.method == 'POST':
        return 405

    if not request.META.get('CONTENT_TYPE') == 'application/json':
        return 415


def _form_generate(request, args, generator, tab_selected):
    try:
        stdout, binary = generator(**args)
        return _get_downloadable_binary_file(
            request,
            binary,
            request.POST.get('output_filename')
        )
    except Exception as e:
        return render(
            request,
            'home.html',
            {
                'error_message': e,
                'tab_selected': tab_selected
            }
        )


def _rest_generate(request, args, generator):
    try:
        stdout, binary = generator(**args)
        return JsonResponse({'stdout': str(stdout), 'binary': str(binary)})
    except (JavaNotFoundError, GeneratorCommandError) as e:
        message = e
        status_code = 500
    except Exception as e:
        message = e
        status_code = 400

    message = {u"error_message": str(message)}
    return HttpResponse(
        content=json.dumps(message),
        content_type="application/json",
        status=status_code
    )


def _get_downloadable_binary_file(request, file_bytes, filename):
    response = HttpResponse(file_bytes)
    type = None

    if type is None:
        type = 'application/octet-stream'
        response['Content-Type'] = type
        response['Content-Length'] = str(len(file_bytes))

    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        filename_header = 'filename=%s' % filename

    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        filename_header = ''
    else:
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(filename)

    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


def upload_alfresco_license(request):
    _upload_validate_request(request)

    return _upload_license(
        request,
        request.FILES['file'].read(),
        alfresco_license_generators.Alfresco.dump
    )


def upload_activiti_license(request):
    _upload_validate_request(request)

    return _upload_license(
        request,
        request.FILES['file'].read(),
        alfresco_license_generators.Activiti.dump
    )


def _upload_validate_request(request):
    if not (request.method == 'POST' and request.is_ajax()):
        error_message = "\nMethod not allowed."\
                        + " Please check the uploaded file and try again,"\
                        + " or raise a ticket with ITS if you "\
                        + "feel this is in error."
        return HttpResponse(content=error_message, status=405)


def _upload_license(request, _file, uploader):
    try:
        dump = uploader(_file)
        dump_message = dump.decode('UTF-8')
        return JsonResponse({'message': dump_message})

    except (JavaNotFoundError, GeneratorCommandError, Exception) as e:
        logging.error(str(e))
        error_message = "\nAn error was thrown by the license dumping "\
                        + "tool. Please check the uploaded file and "\
                        + "try again, or raise a ticket with ITS if "\
                        + "you feel this is an error."
        return HttpResponse(content=error_message, status=500)


def logout_view(request):
    logout(request)
    return redirect('/')


def okta_auth(request):
    auth_error = False
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('site_root')

        if username and password:
            auth_error = True

    form = AuthForm(request.POST or None)

    return render(
        request, 'auth_form.html', {'form': form, 'auth_error': auth_error}
    )
