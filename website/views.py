from django.shortcuts import render


def home(request):
    return render(request, template_name='website/home.html')


def about(request):
    return render(request, template_name='website/about.html')
