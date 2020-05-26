from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from home.models import Setting, ContactFormu, ContactFormMessage
from places.models import Places, Category


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderData = Places.objects.all()[0:5]
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    context = {'setting': setting, 'page': 'home', 'sliderData': sliderData, 'categories': categories, 'lastData':lastData}

    return render(request, 'index.html', context)


def aboutus(request):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'about', 'categories': categories, 'lastData':lastData}

    return render(request, 'aboutus.html', context)

def reference(request):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'reference', 'categories': categories, 'lastData':lastData}

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

    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form, 'page': 'contact', 'categories': categories,'lastData':lastData}

    return render(request, 'contact.html', context)




def category_products(request, id, slug):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    categoriesData = Category.objects.get(pk=id)
    products = Places.objects.filter(category_id=id)
    count = Places.objects.filter(category_id = id).count()
    context = {'products': products, 'categories':categories,'page': 'prop', 'count':count, 'catData':categoriesData, 'lastData':lastData}
    return render(request, 'places.html', context)





def product_detail(request, id, slug):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()

    product = Places.objects.filter(pk=id)
    context = {'product': product, 'categories':categories,'page': 'prop',  'lastData':lastData}
    return render(request, 'places.html', context)