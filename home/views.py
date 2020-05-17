from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from home.models import Setting, ContactFormu, ContactFormMessage
from places.models import Places


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderData = Places.objects.all()[0:5]
    context = {'setting': setting, 'page': 'home', 'sliderData': sliderData}

    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'about'}

    return render(request, 'aboutus.html', context)

def reference(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'reference'}

    return render(request, 'references.html', context)

def contact(request):

    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.ip = request.META.get('REMOTE_ADDR')
            data.message = form.cleaned_data['message']
            data.save()
            messages.success(request, "Mesajınız başarıyla gönderilmiştir")
            return HttpResponseRedirect('/contact')





    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form, 'page': 'contact'}

    return render(request, 'contact.html', context)