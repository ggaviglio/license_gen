from django.shortcuts import render


def generator_selection(request):
    return render(request, 'home.html')
