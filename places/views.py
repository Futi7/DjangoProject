from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from home.models import Setting
from places.models import CommentForm, Comment, ImageForm, Images, Places, Category


def index(request):
    lastData = Places.objects.all().order_by('-id')[:3]
    categories = Category.objects.all()
    setting = Setting.objects.get(pk=1)
    places = Places.objects.all()
    count = Places.objects.all().count()
    context = {'places': places, 'categories': categories, 'page': 'prop', 'count': count, 'setting': setting,
                'lastData': lastData}
    return render(request, 'places.html', context)


@login_required(login_url='/login')
def addcomment(request, id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            current_user = request.user

            data = Comment()
            data.user_id = current_user.id
            data.place_id = id
            data.subject = form.cleaned_data['subject']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()

            messages.success(request, "Yorumunuz başarıyla gönderilmiştir")

            return HttpResponseRedirect(url)
    messages.warning(request, "Yorumunuz kaydedilmedi.Lütfen kontrol ediniz.")

    return HttpResponseRedirect(url)




@login_required(login_url='/login')
def place_delete_image(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        Images.objects.filter(id=id).delete()

        messages.success(request, 'Image succesfully deleted.')
        return HttpResponseRedirect(lasturl)


def image_gallery(request, id):
    if request.method == 'POST':
        lasturl = request.META.get('HTTP_REFERER')
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            data = Images()
            data.title = form.cleaned_data['title']
            data.place_id = id
            data.image = form.cleaned_data['image']
            data.save()
            messages.success(request, 'Image uploaded succesfully !')
            return HttpResponseRedirect(lasturl)
        else:
            messages.warning(request, 'Form Error :' + str(form.errors))
            return HttpResponseRedirect(lasturl)
    else:
        place = Places.objects.get(id=id)
        images = Images.objects.filter(place_id=id)
        form = ImageForm()
        context = {
            'place': place,
            'images': images,
            'form': form,
        }
        return render(request, 'image_gallery.html', context)


