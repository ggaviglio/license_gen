from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
import license_generator  # this is the module to be implemented by Dan


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

    return HttpResponse("Hello world!")
