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
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


def _get_checkbox_value(value):
    result = ""

    if value == '1':
        result = True
    elif value is None:
        result = False
    else:
        result = value

    return result


def _rest_generate_alfresco_license(data):

    args = {}
    expected_arguments = {
        'release_key': 'release',
        'cloud_sync': 'cloudsync',
        'holder_name': 'h',
        'end_date': 'e',
        'heartbeat_url': 'heartbeaturl',
        'ats_end_date': 'ats',
        'max_users': 'mu',
        'no_heartbeat': 'noheartbeat',
        'license_type': 'l',
        'cluster_enabled': 'clusterenabled',
        'max_docs': 'md',
        'cryptodoc_enabled': 'cryptodocenabled'
    }

    for key, value in data.items():
        if key in expected_arguments:
            if _get_checkbox_value(value) != '':
                args.update(
                    {expected_arguments[key]: _get_checkbox_value(value)}
                )

        else:  # Bad request 400
            raise Exception(
                "\n\nError:\nArgument not expected: {}".format(key)
            )

    stdout, binary = alfresco_license_generators.Alfresco.generate(**args)

    return (str(stdout), str(binary))


def _rest_generate_activiti_license(data):

    args = {}
    expected_arguments = {
        'number_of_admins': 'numberOfAdmins',
        'holder_name': 'h',
        'version': 'v',
        'end_date': 'e',
        'number_of_licenses': 'numberOfLicenses',
        'number_of_editors': 'numberOfEditors',
        'number_of_processes': 'numberOfProcesses',
        'number_of_apps': 'numberOfApps',
        'start_date': 's',
        'multi_tenant': 'multiTenant',
        'default_tenant': 'defaultTenant'
    }

    for key, value in data.items():
        if key in expected_arguments:
            if _get_checkbox_value(value) != '':

                if expected_arguments[key] in ['e', 's']:
                    args.update({
                        expected_arguments[key]: datetime.datetime.strptime(
                            value,
                            '%d/%m/%Y'
                        ).strftime('%Y%m%d')
                    })

                else:
                    args.update({expected_arguments[key]: value})

        else:  # Bad request 400
            raise Exception(
                "\n\nError:\nArgument not expected: {}".format(key)
            )

    stdout, binary = alfresco_license_generators.Activiti.generate(**args)

    return (str(stdout), str(binary))


def _generate_alfresco_license(request):

    args = {}
    expected_arguments = {
        'release_key': 'release',
        'field_cloud_sync': 'cloudsync',
        'field_holder_name': 'h',
        'field_end_date': 'e',
        'field_heartbeat_url': 'heartbeaturl',
        'field_ats_end_date': 'ats',
        'field_max_users': 'mu',
        'field_no_heartbeat': 'noheartbeat',
        'field_license_type': 'l',
        'field_cluster_enabled': 'clusterenabled',
        'field_max_docs': 'md',
        'field_cryptodoc_enabled': 'cryptodocenabled'
    }

    for key, value in request.POST.items():
        if key in expected_arguments:
            if value != '':
                args.update(
                    {expected_arguments[key]: _get_checkbox_value(value)}
                )

    stdout, binary = alfresco_license_generators.Alfresco.generate(**args)

    return (stdout, binary)


def _generate_activiti_license(request):

    args = {}
    expected_arguments = {
        'field_number_of_admins': 'numberOfAdmins',
        'field_holder_name': 'h',
        'field_version': 'v',
        'field_end_date': 'e',
        'field_number_of_licenses': 'numberOfLicenses',
        'field_number_of_editors': 'numberOfEditors',
        'field_number_of_processes': 'numberOfProcesses',
        'field_number_of_apps': 'numberOfApps',
        'field_start_date': 's',
        'field_multi_tenant': 'multiTenant',
        'field_default_tenant': 'defaultTenant'
    }

    for key, value in request.POST.items():
        if key in expected_arguments:
            if value != '':
                if expected_arguments[key] in ['e', 's']:
                    args.update({
                        expected_arguments[key]: datetime.datetime.strptime(
                            value,
                            '%d/%m/%Y'
                        ).strftime('%Y%m%d')
                    })

                else:
                    args.update({expected_arguments[key]: value})

    stdout, binary = alfresco_license_generators.Activiti.generate(**args)

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

    try:
        if request.POST.get('alfresco_generate_btn'):
            filename = request.POST.get('output_filename')
            tab_selected = 'Alfresco'
            stdout, binary = _generate_alfresco_license(request)

        elif request.POST.get('activiti_generate_btn'):
            filename = request.POST.get('output_filename')
            tab_selected = 'Activiti'
            stdout, binary = _generate_activiti_license(request)

    except JavaNotFoundError as e:
        return render(
            request,
            'home.html',
            {'java_error_message': e, 'tab_selected': tab_selected}
        )

    except GeneratorCommandError as e:
        return render(
            request,
            'home.html',
            {
                'generator_error_message': e,
                'tab_selected': tab_selected
            }
        )
    except Exception as e:
        return render(
            request,
            'home.html',
            {'general_error_message': e, 'tab_selected': tab_selected}
        )

    return get_downloadable_binary_file(request, binary, filename)


@csrf_exempt
def rest_generate_license(request):
    path = request.path.split('/')[3]

    if path in ['alfresco', 'activiti']:
        if request.method == 'POST':
            if request.META.get('CONTENT_TYPE') == 'application/json':

                try:
                    json_data = request.body.decode('UTF-8')
                    data = json.loads(json_data)

                    if path == "alfresco":
                        stdout, binary = _rest_generate_alfresco_license(data)

                    else:
                        stdout, binary = _rest_generate_activiti_license(data)

                except JavaNotFoundError as e:
                    msg = {u"java_error_message": str(e)}
                    return HttpResponse(
                        content=json.dumps(msg),
                        content_type="application/json",
                        status=400
                    )

                except GeneratorCommandError as e:
                    msg = {u"generator_error_message": str(e)}
                    return HttpResponse(
                        content=json.dumps(msg),
                        content_type="application/json",
                        status=400
                    )

                except Exception as e:
                    msg = {u"general_error_message": str(e)}
                    return HttpResponse(
                        content=json.dumps(msg),
                        content_type="application/json",
                        status=400
                    )

                return JsonResponse({'stdout': stdout, 'binary': binary})

            else:
                # Unsupported media type
                return HttpResponse(content="", status=415)
        else:
            # Method not allowed
            return HttpResponse(content="", status=405)
    else:
        # Page not found
        return HttpResponse(content="", status=404)
