from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.exceptions import ValidationError
import alfresco_license_generators
import datetime


def get_value_number(request, field):
    result = None

    if request.POST.get(field) == '':
        result = 0
    else:
        result = int(request.POST.get(field))

    return result


def get_checkbox_value(value):
    result = ""

    if value == '1':
        result = True
    elif value is None:
        result = False

    return result


def get_downloadable_binary_file(request, file_bytes, filename):
    response = HttpResponse(file_bytes)
    #type, encoding = mimetypes.guess_type(file_bytes)  # I think that this line is not necessary
    type = None

    if type is None:
        type = 'application/octet-stream'
        response['Content-Type'] = type
        response['Content-Length'] = str(len(file_bytes))  # It will retrieve the number of bytes

    #if encoding is not None:
    #    response['Content-Encoding'] = encoding

    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        filename_header = 'filename=%s' % filename

    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
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
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


def generate_license(request):

    file_bytes = ''
    filename = ''
    datos = {}

    try:
        if request.POST.get('alfresco_generate_btn'):
            alfresco_data = {}
            alfresco_data['release_key'] = request.POST.get('release_key')
            alfresco_data['notes'] = request.POST.get('notes')
            alfresco_data['external_id'] = request.POST.get('external_id')
            alfresco_data['external_id_type'] = request.POST.get('external_id_type')
            alfresco_data['tag_trial'] = get_checkbox_value(request.POST.get('tag_trial'))
            alfresco_data['tag_internal_use_only'] = get_checkbox_value(request.POST.get('tag_internal_use_only'))
            alfresco_data['tag_proof_of_concept'] = get_checkbox_value(request.POST.get('tag_proof_of_concept'))
            alfresco_data['tag_extension'] = get_checkbox_value(request.POST.get('tag_extension'))
            alfresco_data['tag_perpetual'] = get_checkbox_value(request.POST.get('tag_perpetual'))
            alfresco_data['field_holder_name'] = request.POST.get('field_holder_name')

            alfresco_data['field_days'] = get_value_number(request, 'field_days')
            alfresco_data['field_max_users'] = get_value_number(request, 'field_max_users')

            alfresco_data['field_no_heartbeat'] = get_checkbox_value(request.POST.get('field_no_heartbeat'))
            alfresco_data['field_heartbeat_url'] = request.POST.get('field_heartbeat_url')
            alfresco_data['field_cluster_enabled'] = get_checkbox_value(request.POST.get('field_cluster_enabled'))
            alfresco_data['field_license_type'] = request.POST.get('field_license_type')
            alfresco_data['field_end_date'] = request.POST.get('field_end_date')

            alfresco_data['field_max_docs'] = get_value_number(request, 'field_max_docs')

            alfresco_data['field_cloud_sync'] = get_checkbox_value(request.POST.get('field_cloud_sync'))
            alfresco_data['field_ats_end_date'] = request.POST.get('field_ats_end_date')
            alfresco_data['field_cryptodoc_enabled'] = get_checkbox_value(request.POST.get('field_cryptodoc_enabled'))
            alfresco_data['output_filename'] = request.POST.get('output_filename')
            filename = alfresco_data['output_filename']

            '''print("Ahora vamos a ver que tenemos aqui: ")
            for key in alfresco_data:
                file_bytes = file_bytes + key + ' ' + str(alfresco_data[key]) + '\n'

            print(file_bytes)'''

            ## TESTINGGG
            stdout, binary = alfresco_license_generators.Alfresco.generate(
                release=alfresco_data['release_key'],
                cloudsync=alfresco_data['field_cloud_sync'],
                h=alfresco_data['field_holder_name'],
                e=alfresco_data['field_end_date'],
                heartbeaturl=alfresco_data['field_heartbeat_url'],
                ats=alfresco_data['field_ats_end_date'],
                mu=alfresco_data['field_max_users'],
                noheartbeat=alfresco_data['field_no_heartbeat'],
                l=alfresco_data['field_license_type'],
                clusterenabled=alfresco_data['field_cluster_enabled'],
                md=alfresco_data['field_max_docs'],
                cryptodocenabled=alfresco_data['field_cryptodoc_enabled']
            )
            ## TESTINGGG
            file_bytes = binary

        elif request.POST.get('activiti_generate_btn'):
            activiti_data = {}
            activiti_data['notes'] = request.POST.get('notes')
            activiti_data['external_id'] = request.POST.get('external_id')
            activiti_data['external_id_type'] = request.POST.get('external_id_type')
            activiti_data['tag_trial'] = get_checkbox_value(request.POST.get('tag_trial'))
            activiti_data['tag_internal_use_only'] = get_checkbox_value(request.POST.get('tag_internal_use_only'))
            activiti_data['tag_proof_of_concept'] = get_checkbox_value(request.POST.get('tag_proof_of_concept'))
            activiti_data['tag_extension'] = get_checkbox_value(request.POST.get('tag_extension'))
            activiti_data['tag_perpetual'] = get_checkbox_value(request.POST.get('tag_perpetual'))
            activiti_data['field_holder_name'] = request.POST.get('field_holder_name')
            activiti_data['field_start_date'] = request.POST.get('field_start_date')

            activiti_data['field_number_of_admins'] = get_value_number(request, 'field_number_of_admins')
            activiti_data['field_number_of_editors'] = get_value_number(request, 'field_number_of_editors')

            activiti_data['field_multi_tenant'] = request.POST.get('field_multi_tenant')
            activiti_data['field_version'] = request.POST.get('field_version')
            activiti_data['field_end_date'] = request.POST.get('field_end_date')

            activiti_data['field_number_of_licenses'] = get_value_number(request, 'field_number_of_licenses')
            activiti_data['field_number_of_processes'] = get_value_number(request, 'field_number_of_processes')
            activiti_data['field_number_of_apps'] = get_value_number(request, 'field_number_of_apps')

            activiti_data['field_default_tenant'] = request.POST.get('field_default_tenant')
            activiti_data['output_filename'] = request.POST.get('output_filename')
            filename = activiti_data['output_filename']

            '''print("Ahora vamos a ver que tenemos aqui ACTIVITI: ")
            for key in activiti_data:
                file_bytes = file_bytes + key + ' ' + str(activiti_data[key]) + '\n'

            print(file_bytes)'''

            ## TESTTTT
            stdout, binary = alfresco_license_generators.Activiti.generate(
                numberOfAdmins=activiti_data['field_number_of_admins'],
                h=activiti_data['field_holder_name'],
                v=activiti_data['field_version'],
                e=datetime.datetime.strptime(activiti_data['field_end_date'], '%d/%m/%Y').strftime('%Y%m%d'),
                numberOfLicenses=activiti_data['field_number_of_licenses'],
                numberOfEditors=activiti_data['field_number_of_editors'],
                numberOfProcesses=activiti_data['field_number_of_processes'],
                numberOfApps=activiti_data['field_number_of_apps'],
                s=datetime.datetime.strptime(activiti_data['field_start_date'], '%d/%m/%Y').strftime('%Y%m%d'),
                multiTenant=activiti_data['field_multi_tenant'],
                defaultTenant=activiti_data['field_default_tenant']
            )
            ## TESTTTT
            file_bytes = binary

    #except EmptyDictionary:
    except ValidationError:
        # If I am can not generate a file I will have to show some error messages an I might redirect
        # the page to a the same view?
        return redirect('/')

    except ValidationError:
        return redirect('/')

    else:
        #file_bytes = "Here we will allocate the future content of what the license_generator.alfresco or license_generator.activiti will retrieve us!"
        return get_downloadable_binary_file(request, file_bytes, filename)
