from ckeditor.widgets import CKEditorWidget
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, TextInput, Select, FileInput
from django.urls import reverse
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField

from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
        )

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank='True')
    keywords = models.CharField(max_length=200, blank='True')
    status = models.CharField(max_length=10, choices=STATUS)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(null=False, unique=True)
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)



    class MPTTMeta:
        order_insertion_by = ['title']


    def __str__(self):
        fullpath = [self.title]
        k = self.parent
        while k is not None:
            fullpath.append(k.title)
            k = k.parent
        return ' -> '.join(fullpath[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Places(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank='True')
    details = RichTextField()
    slug = models.SlugField(null=False, unique=True)
    keywords = models.CharField(max_length=200, blank='True')
    status = models.CharField(max_length=10, choices=STATUS)
    image = models.ImageField(blank='True', upload_to='images/')
    price = models.FloatField()
    country = models.CharField(max_length=20, blank='True')
    audience = models.CharField(max_length=20, blank='True')

    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


    def get_absolute_url(self):
        return reverse('places_detail', kwargs={'slug': self.slug})

    def catimg_tag(self):
        return mark_safe((Category.status))


class PlacesForm(ModelForm):
    class Meta:
        model = Places
        fields = ['category', 'title', 'slug', 'keywords','price','country', 'audience', 'description', 'image', 'details']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Title'}),
            'slug': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Slug'}),
            'keywords': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Keywords'}),
            'description': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Description'}),
            'price': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Price'}),
            'country': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Country'}),
            'audience': TextInput(attrs={'class': 'form-control valid', 'placeholder': 'Audience'}),
            'category': Select(attrs={'class': 'form-control valid', 'placeholder': 'Category'}, choices=Category.objects.all()),
            'image': FileInput(attrs={'class': 'form-control valid', 'placeholder': 'Image'}),
            'details': CKEditorWidget(),
        }






class Comment(models.Model):
    STATUS = (
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(blank='True', max_length=50)
    comment = models.TextField(blank='True', max_length=255)
    rate = models.IntegerField(blank = 'True')
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    ip = models.CharField(blank='True', max_length=20)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']



class Images(models.Model):
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(blank='True', upload_to='images/')
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))

    image_tag.short_description = 'Image'


class ImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title', 'image']



