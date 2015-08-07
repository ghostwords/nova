from django.shortcuts import render


def index(request):
    return render(request, 'homepage/index.html')


def privacy(request):
    return render(request, 'homepage/privacy.html')
