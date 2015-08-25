from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from license_generator_form.license_generator import generate
import mimetypes  # I will move this line from here to the top of the file


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

    file_bytes = ""
    filename = ""
    datos = {}

    try:
        if request.POST.get('alfresco_generate_btn'):
            alfresco_data = {}
            alfresco_data['release_key'] = request.POST.get('release_key')
            alfresco_data['notes'] = request.POST.get('notes')
            alfresco_data['external_id'] = request.POST.get('external_id')
            alfresco_data['external_id_type'] = request.POST.get('external_id_type')
            alfresco_data['tag_trial'] = request.POST.get('tag_trial')
            alfresco_data['tag_internal_use_only'] = request.POST.get('tag_internal_use_only')
            alfresco_data['tag_proof_of_concept'] = request.POST.get('tag_proof_of_concept')
            alfresco_data['tag_extension'] = request.POST.get('tag_extension')
            alfresco_data['tag_perpetual'] = request.POST.get('tag_perpetual')
            alfresco_data['field_holder_name'] = request.POST.get('field_holder_name')

            if request.POST.get('field_days') == '':
                alfresco_data['field_days'] = 0
            else:
                alfresco_data['field_days'] = int(request.POST.get('field_days'))

            if request.POST.get('field_max_users') == '':
                alfresco_data['field_max_users'] = 0
            else:
                alfresco_data['field_max_users'] = int(request.POST.get('field_max_users'))

            alfresco_data['field_no_heartbeat'] = request.POST.get('field_no_heartbeat')
            alfresco_data['field_heartbeat_url'] = request.POST.get('field_heartbeat_url')
            alfresco_data['field_cluster_enabled'] = request.POST.get('field_cluster_enabled')
            alfresco_data['field_license_type'] = request.POST.get('field_license_type')
            alfresco_data['field_end_date'] = request.POST.get('field_end_date')

            if request.POST.get('field_max_docs') == '':
                alfresco_data['field_max_docs'] = 0
            else:
                alfresco_data['field_max_docs'] = int(request.POST.get('field_max_docs'))

            alfresco_data['field_cloud_sync'] = request.POST.get('field_cloud_sync')
            alfresco_data['field_ats_end_date'] = request.POST.get('field_ats_end_date')
            alfresco_data['field_cryptodoc_enabled'] = request.POST.get('field_cryptodoc_enabled')
            alfresco_data['output_filename'] = request.POST.get('output_filename')
            filename = alfresco_data['output_filename']
            # Ok, at this point I have all the values gathered from the form, so what I have got to do is just
            # stream_bytes = license_generator.alfresco.generate(alfresco_data)
            # Now in this point I have to generate the file to download and after this
            for key in alfresco_data:
                file_bytes = file_bytes + key + ' ' + str(alfresco_data[key]) + '\n'

            datos = alfresco_data
            datos.update({'alfresco_generate_btn':'1'})
            generate(datos)

        elif request.POST.get('activiti_generate_btn'):
            activiti_data = {}
            activiti_data['notes'] = request.POST.get('notes')
            activiti_data['external_id'] = request.POST.get('external_id')
            activiti_data['external_id_type'] = request.POST.get('external_id_type')
            activiti_data['tag_trial'] = request.POST.get('tag_trial')
            activiti_data['tag_internal_use_only'] = request.POST.get('tag_internal_use_only')
            activiti_data['tag_proof_of_concept'] = request.POST.get('tag_proof_of_concept')
            activiti_data['tag_extension'] = request.POST.get('tag_extension')
            activiti_data['tag_perpetual'] = request.POST.get('tag_perpetual')
            activiti_data['field_holder_name'] = request.POST.get('field_holder_name')
            activiti_data['field_start_day'] = request.POST.get('field_start_day')

            if request.POST.get('field_number_of_admins') == '':
                activiti_data['field_number_of_admins'] = 0
            else:
                activiti_data['field_number_of_admins'] = int(request.POST.get('field_number_of_admins'))

            if request.POST.get('field_number_of_editors') == '':
                activiti_data['field_number_of_editors'] = 0
            else:
                activiti_data['field_number_of_editors'] = int(request.POST.get('field_number_of_editors'))

            activiti_data['field_multi_tenant'] = request.POST.get('field_multi_tenant')
            activiti_data['field_version'] = request.POST.get('field_version')
            activiti_data['field_end_date'] = request.POST.get('field_end_date')

            if request.POST.get('field_number_of_licenses') == '':
                activiti_data['field_number_of_licenses'] = 0
            else:
                activiti_data['field_number_of_licenses'] = int(request.POST.get('field_number_of_licenses'))

            if request.POST.get('field_number_of_processes') == '':
                activiti_data['field_number_of_processes'] = 0
            else:
                activiti_data['field_number_of_processes'] = int(request.POST.get('field_number_of_processes'))

            activiti_data['field_default_tenant'] = request.POST.get('field_default_tenant')
            activiti_data['output_filename'] = request.POST.get('output_filename')
            filename = activiti_data['output_filename']

            # file_bytes = license_generator.activiti.generate(activiti_data)
            for key in activiti_data:
                file_bytes = file_bytes + key + ' ' + str(activiti_data[key]) + '\n'

            datos = activiti_data
            datos.update({'activiti_generate_btn':'1'})

            generate(datos)

    #except EmptyDictionary:
    except ValidationError:
        # If I am can not generate a file I will have to show some error messages an I might redirect
        # the page to a the same view?
        return redirect('/')

    except ValidationError:
        return redirect('/')

    else:
        ##########################################################################

        #file_bytes = "Here we will allocate the future content of what the license_generator.alfresco or license_generator.activiti will retrieve us!"

        response = HttpResponse(file_bytes)
        type, encoding = mimetypes.guess_type(file_bytes)  # I think that this line is not necessary

        if type is None:
            type = 'application/octet-stream'
            response['Content-Type'] = type
            response['Content-Length'] = str(len(file_bytes))  # It will retrieve the number of bytes

        if encoding is not None:
            response['Content-Encoding'] = encoding

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
        #####################################################################
