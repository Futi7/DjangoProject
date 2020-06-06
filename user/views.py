from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from home.models import Setting, UserProfile
from places.models import Places, Category
from user.forms import UserUpdateForm, ProfileUpdateForm


@login_required(login_url='/login')
def index(request):
    lastData = Places.objects.all().order_by('-id')[:3]
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
        lastData = Places.objects.all().order_by('-id')[:3]
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
        lastData = Places.objects.all().order_by('-id')[:3]
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
