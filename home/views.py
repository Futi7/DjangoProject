import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile
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




def category_places(request, id, slug):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    categoriesData = Category.objects.get(pk=id)
    setting = Setting.objects.get(pk=1)
    places = Places.objects.filter(category_id=id)
    count = Places.objects.filter(category_id = id).count()
    context = {'places': places, 'categories':categories,'page': 'prop', 'count':count,'setting': setting, 'catData':categoriesData, 'lastData':lastData}
    return render(request, 'places.html', context)


def category_all(request, id, slug):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    categoriesData = Category.objects.filter(parent_id=id)
    setting = Setting.objects.get(pk=1)
    places = []
    for cat in categoriesData:
        places += Places.objects.filter(category_id=cat.id)
    places += Places.objects.filter(category_id=id)
    categoriesData = Category.objects.get(id=id)
    count = len(places)
    context = {'places': places, 'categories':categories,'page': 'prop', 'count':count,'setting': setting, 'catData':categoriesData, 'lastData':lastData}
    return render(request, 'places.html', context)








def place_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            lastData = Places.objects.all().order_by('-id')[:3]
            categories = Category.objects.all()
            setting = Setting.objects.get(pk=1)
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                places = Places.objects.filter(title__icontains=query)
            else:
                places = Places.objects.filter(title__icontains=query, category_id=catid)
            count = places.count()
            context = {'places': places, 'categories': categories, 'page': 'prop', 'count': count, 'setting': setting,
                        'lastData': lastData}

            return render(request, 'places.html', context)
    return HttpResponseRedirect('/')



def place_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        place = Places.objects.filter(title__icontains=q)
        results = []
        for rs in place:
            place_json = {}
            place_json = rs.title
            results.append(place_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)



def place_detail(request, id, slug):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    comments = Comment.objects.filter(place_id=id, status ='True')
    setting = Setting.objects.get(pk=1)
    images = Images.objects.filter(place_id=id)
    place = Places.objects.get(pk=id)
    keywords = place.keywords.split(', ')
    context = {'place': place, 'categories':categories,'page': 'prop',  'lastData':lastData,'setting': setting, 'keywords':keywords, 'images':images, 'comments':comments}
    return render(request, 'place.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Hata ! Kullanıcı adı ya da şifre yanlış")
            return HttpResponseRedirect('/login')
    return render(request, 'login.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request,
                             "Welcome to most in-demand touristic site !")
            return HttpResponseRedirect('/')

    form = SignUpForm()
    context ={
        'form': form,
    }
    return render(request, 'signup.html', context)
