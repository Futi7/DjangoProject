from django.shortcuts import render

def index(request):
    return render(request, 'index.html')


def fonksiyon(request):
    return render(request, 'index.html')