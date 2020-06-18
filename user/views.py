from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from home.models import Setting, UserProfile
from places.models import Places, Category, Comment, PlacesForm
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'user', 'categories': categories, 'lastData': lastData, 'profile':profile}

    return render(request, 'userprofile.html', context)


@login_required(login_url='/login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('/user')
    else:
        categories = Category.objects.all()
        user_form = UserUpdateForm(instance=request.user)
        lastData = Places.objects.filter(status='True').order_by('-id')[:3]
        current_user = request.user

        setting = Setting.objects.get(pk=1)
        profile = UserProfile.objects.get(user_id=current_user.id)
        profile_form = ProfileUpdateForm(instance=request.user.userprofile)
        context = {
            'setting': setting,
            'categories': categories,
            'user_form': user_form,
            'page': 'user',
            'lastData': lastData,
            'profile': profile,
            'profile_form': profile_form,
        }
        return render(request, 'update.html', context)


@login_required(login_url='/login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was succesfully updated!')
            return redirect('/user')
        else:
            messages.error(request, 'Please correct the error below.<br>' + str(form.errors))
            return HttpResponseRedirect('/user/password')
    else:
        categories = Category.objects.all()
        setting = Setting.objects.get(pk=1)
        current_user = request.user
        lastData = Places.objects.filter(status='True').order_by('-id')[:3]
        profile = UserProfile.objects.get(user_id=current_user.id)
        form = PasswordChangeForm(request.user)
        context = {
            'setting': setting,
            'categories': categories,
            'form': form,
            'profile': profile,
            'page': 'user',
            'lastData': lastData,
        }
        return render(request, 'changepassword.html', context)

@login_required(login_url='/login')
def comments(request):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    comment = Comment.objects.filter(user_id=current_user.id)
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'user', 'categories': categories, 'lastData': lastData, 'comments':comment, 'profile': profile}

    return render(request, 'usercomments.html', context)


@login_required(login_url='/login')
def deletecomment(request, id):
    current_user = request.user
    Comment.objects.filter(id=id, user_id= current_user).delete()
    messages.success(request, 'Comment succesfully deleted.')
    return HttpResponseRedirect('/user/comments')


@login_required(login_url='/login')
def places(request):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    places = Places.objects.filter(user_id=current_user.id)
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'user', 'categories': categories, 'lastData': lastData, 'places':places, 'profile': profile}

    return render(request, 'user_places.html', context)


def user_new_place(request):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    places = Places.objects.filter(user_id=current_user.id)
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    page_title = "Add New Place"
    if request.method == 'POST':
        form = PlacesForm(request.POST, request.FILES)
        if form.is_valid():
            current_user = request.user
            data = Places()
            data.user_id = current_user.id
            data.title = form.cleaned_data['title']
            data.keywords = form.cleaned_data['keywords']
            data.description = form.cleaned_data['description']
            data.image = form.cleaned_data['image']
            data.price = form.cleaned_data['price']
            data.country = form.cleaned_data['country']
            data.visit_hours = form.cleaned_data['visit_hours']
            data.currency = form.cleaned_data['currency']
            data.audience = form.cleaned_data['audience']
            data.category = form.cleaned_data['category']
            data.slug = form.cleaned_data['slug']
            data.details = form.cleaned_data['details']
            data.status = 'False'
            data.save()
            messages.success(request, 'Place add succesfully registered.')
            return HttpResponseRedirect('/user/places/')
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/user_new_place')
    else:
        category = Category.objects.all()
        form = PlacesForm()
        context = {'category': category, 'form': form, 'setting': setting, 'page': 'user', 'categories': categories, 'lastData': lastData, 'places':places, 'profile': profile,'page_title':page_title}
        return render(request, 'user_new_place.html', context)



@login_required(login_url='/login')
def user_edit_place(request, id):
    lastData = Places.objects.filter(status='True').order_by('-id')[:3]
    current_user = request.user
    profile = UserProfile.objects.get(user_id=current_user.id)
    place = Places.objects.get(id=id)
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    page_title = "Edit Place: "+ place.title
    if request.method == 'POST':
        form = PlacesForm(request.POST, request.FILES, instance=place)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your place successfuly updated')
            return HttpResponseRedirect('/user/places')
        else:
            messages.success(request, 'Content Form Error :' + str(form.errors))
            return HttpResponseRedirect('/user/user_edit_place/' + str(id))
    else:
        category = Category.objects.all()
        form = PlacesForm(instance=place)
        context = {'category': category, 'form': form, 'setting': setting, 'page': 'user', 'categories': categories,
                   'lastData': lastData, 'places': places, 'profile': profile, 'page_title':page_title}


    return render(request, 'user_new_place.html', context)