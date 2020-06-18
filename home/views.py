import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile, FAQ
from places.models import Places, Category, Images, Comment, Likes


def index(request):
    setting = Setting.objects.get(pk=1)
    sliderData = Places.objects.filter(status='True')[0:5]
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    random_places = Places.objects.filter(status='True').order_by('?')
    categories = Category.objects.all()
    context = {'setting': setting, 'page': 'home','random_places':random_places, 'sliderData': sliderData, 'categories': categories, 'lastData':lastData}

    return render(request, 'index.html', context)


def aboutus(request):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'about', 'categories': categories, 'lastData':lastData}

    return render(request, 'aboutus.html', context)

def reference(request):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
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

    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    form = ContactFormu()
    context = {'setting': setting, 'form': form, 'page': 'contact', 'categories': categories,'lastData':lastData}

    return render(request, 'contact.html', context)




def category_places(request, id, slug):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    categories = Category.objects.all()
    categoriesData = Category.objects.get(pk=id)
    setting = Setting.objects.get(pk=1)
    places = Places.objects.filter(category_id=id, status='True')
    count = places.count()
    context = {'places': places, 'categories':categories,'page': 'prop', 'count':count,'setting': setting, 'catData':categoriesData, 'lastData':lastData}
    return render(request, 'places.html', context)


def category_all(request, id, slug):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    categories = Category.objects.all()
    categoriesData = Category.objects.filter(parent_id=id)
    setting = Setting.objects.get(pk=1)
    places = []
    for cat in categoriesData:
        places += Places.objects.filter(category_id=cat.id, status='True')
    places += Places.objects.filter(category_id=id, status='True')
    categoriesData = Category.objects.get(id=id)
    count = len(places)
    context = {'places': places, 'categories':categories,'page': 'prop', 'count':count,'setting': setting, 'catData':categoriesData, 'lastData':lastData}
    return render(request, 'places.html', context)



def faq(request):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    setting = Setting.objects.get(pk=1)
    categories = Category.objects.all()
    faq = FAQ.objects.all().order_by('ordernumber')
    context = {'categories':categories, 'setting': setting, 'faq': faq, 'page': 'faq', 'lastData':lastData}
    return render(request, 'faq.html', context)




def place_search(request):

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            lastData = Places.objects.filter(status='True').order_by('-id')[:3]
            categories = Category.objects.all()
            setting = Setting.objects.get(pk=1)
            query = form.cleaned_data['query']
            catid = form.cleaned_data['catid']
            if catid == 0:
                places = Places.objects.filter(title__icontains=query, status=True)
            else:
                places = Places.objects.filter(title__icontains=query, category_id=catid, status=True)
            count = places.count()
            context = {'places': places, 'categories': categories, 'page': 'prop', 'count': count, 'setting': setting,
                        'lastData': lastData}

            return render(request, 'places.html', context)
    return HttpResponseRedirect('/')



def place_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        place = Places.objects.filter(title__icontains=q, status=True)
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
    lasturl = request.META.get('HTTP_REFERER')
    place = Places.objects.get(pk=id)
    current_user = request.user
    if place.status == 'False' and place.user_id != current_user.id:
        return HttpResponseRedirect(lasturl)

    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    categories = Category.objects.all()
    comments = Comment.objects.filter(place_id=id, status ='True')

    if Likes.objects.filter(place_id=id, user_id=current_user.id).exists():
        obj = True
    else:
        obj = False


    setting = Setting.objects.get(pk=1)
    images = Images.objects.filter(place_id=id)
    profile = UserProfile.objects.get(user=place.user)
    keywords = place.keywords.split(',')
    context = {'place': place, 'categories':categories,'page': 'prop',  'lastData':lastData,'setting': setting, 'keywords':keywords, 'images':images, 'profile':profile, 'liked':obj, 'comments':comments}
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
