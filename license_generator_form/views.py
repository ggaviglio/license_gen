from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.core.exceptions import ValidationError
#import license_generator  # this is the module to be implemented by Dan


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
    # Following will be the expected dictionaries when we get a post
    # alfresco-data / activiti-data
    # no-alfresco-data / no-activiti-data
    # bad-alfresco-data / bad-activiti-data
    stream_bytes = ""

    try:
        if request.POST.get('alfresco-data'):
            stream_bytes = license_generator.alfresco.generate(request.POST.get('alfresco-data'))
        elif request.POST.get('activiti-data'):
            stream_bytes = license_generator.activiti.generate(request.POST.get('activiti-data'))

    except EmptyDictionary:
        print("The dictionary is empty")

    except BadDictionary:
        print("The dictionary does contain bad data")
    else:
        # If there is no exception execute this!!!
        print("there is no exception therefore I will be dealing with the stream_bytes")
        error = "I still don't know what sort of error control can I put in here"
        return render(request, 'home.html', {'error': error})
