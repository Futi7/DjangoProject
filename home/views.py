from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render

from home.models import Setting, ContactFormu, ContactFormMessage
from places.models import Places, Category, Images, Comment


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
    setting = Setting.objects.get(pk=1)
    products = Places.objects.filter(category_id=id)
    count = Places.objects.filter(category_id = id).count()
    context = {'products': products, 'categories':categories,'page': 'prop', 'count':count,'setting': setting, 'catData':categoriesData, 'lastData':lastData}
    return render(request, 'places.html', context)


def place_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            places = Places.objects.filter(title__icontains=query)
            context = {
                'category': category,
                'blogs': blogs,
            }
            return render(request, 'blogs_search.html', context)
    return HttpResponseRedirect('/')








def product_detail(request, id, slug):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    comments = Comment.objects.filter(place_id=id, status ='True')
    setting = Setting.objects.get(pk=1)
    images = Images.objects.filter(place_id=id)
    product = Places.objects.get(pk=id)
    keywords = product.keywords.split(', ')
    context = {'product': product, 'categories':categories,'page': 'prop',  'lastData':lastData,'setting': setting, 'keywords':keywords, 'images':images, 'comments':comments}
    return render(request, 'place.html', context)