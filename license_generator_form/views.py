from django.shortcuts import render
from django.http import HttpResponse

def generator_selection(request):
	return HttpResponse('<html><title>License Generator</title></html>')