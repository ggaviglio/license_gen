from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import alfresco_license_generators
from alfresco_license_generators import (
    JavaNotFoundError,
    GeneratorCommandError
)
import datetime


def _get_value_date(request, field):
    result = None

    if request.POST.get(field) == '':
        result = ''
    else:
        result = datetime.datetime.strptime(
            request.POST.get(field),
            '%d/%m/%Y'
        ).strftime('%Y%m%d')

    return result


def _get_value_number(request, field):
    result = None

    if request.POST.get(field) == '':
        result = 0
    else:
        result = int(request.POST.get(field))

    return result


def _get_checkbox_value(value):
    result = ""

    if value == '1':
        result = True
    elif value is None:
        result = False

    return result


def _generate_alfresco_license(request):
    stdout, binary = alfresco_license_generators.Alfresco.generate(
        release=request.POST.get('release_key'),
        cloudsync=_get_checkbox_value(request.POST.get('field_cloud_sync')),
        h=request.POST.get('field_holder_name'),
        e=request.POST.get('field_end_date'),
        heartbeaturl=request.POST.get('field_heartbeat_url'),
        ats=request.POST.get('field_ats_end_date'),
        mu=_get_value_number(request, 'field_max_users'),
        noheartbeat=_get_checkbox_value(
            request.POST.get('field_no_heartbeat')
        ),
        l=request.POST.get('field_license_type'),
        clusterenabled=_get_checkbox_value(
            request.POST.get('field_cluster_enabled')
        ),
        md=_get_value_number(request, 'field_max_docs'),
        cryptodocenabled=_get_checkbox_value(
            request.POST.get('field_cryptodoc_enabled')
        )
    )
    return (stdout, binary)


def _generate_activiti_license(request):
    stdout, binary = alfresco_license_generators.Activiti.generate(
        numberOfAdmins=_get_value_number(request, 'field_number_of_admins'),
        h=request.POST.get('field_holder_name'),
        v=request.POST.get('field_version'),
        e=_get_value_date(request, 'field_end_date'),
        numberOfLicenses=_get_value_number(
            request,
            'field_number_of_licenses'
        ),
        numberOfEditors=_get_value_number(request, 'field_number_of_editors'),
        numberOfProcesses=_get_value_number(
            request,
            'field_number_of_processes'
        ),
        numberOfApps=_get_value_number(request, 'field_number_of_apps'),
        s=_get_value_date(request, 'field_start_date'),
        multiTenant=request.POST.get('field_multi_tenant'),
        defaultTenant=request.POST.get('field_default_tenant')
    )
    return (stdout, binary)


def get_downloadable_binary_file(request, file_bytes, filename):
    response = HttpResponse(file_bytes)
    type = None

    if type is None:
        type = 'application/octet-stream'
        response['Content-Type'] = type
        response['Content-Length'] = str(len(file_bytes))

    # To inspect details for the below code,
    # see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % filename

    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL,
        # so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231
        # (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(filename)

    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


def home_page(request):
    return render(request, 'home.html')


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def generate_license(request):

    filename = ''
    stdout = ''

    try:
        if request.POST.get('alfresco_generate_btn'):
            filename = request.POST.get('output_filename')
            tab_selected = 'alfresco'
            stdout, binary = _generate_alfresco_license(request)

        elif request.POST.get('activiti_generate_btn'):
            filename = request.POST.get('output_filename')
            tab_selected = 'activiti'
            stdout, binary = _generate_activiti_license(request)

    except JavaNotFoundError as error_message:
        return render(
            request,
            'home.html',
            {'java_error_message': error_message, 'tab_selected': tab_selected}
        )

    except GeneratorCommandError as error_message:
        return render(
            request,
            'home.html',
            {'generator_error_message': error_message, 'tab_selected': tab_selected}
        )

    else:
        return get_downloadable_binary_file(request, binary, filename)
