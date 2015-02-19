from django.shortcuts import render

def generator_selection(request):
	return render(request, 'web_form.html')