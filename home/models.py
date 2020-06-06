from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.db import models
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe


class Setting(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank='True')
    keywords = models.CharField(max_length=200, blank='True')
    company = models.CharField(max_length=200)
    address = models.CharField(blank='True', max_length=200)
    phone = models.CharField(blank='True', max_length=15)
    fax = models.CharField(blank='True', max_length=15)
    email = models.CharField(max_length=50)
    smtpserver = models.CharField(max_length=20)
    smtpemail = models.CharField(max_length=20)
    smtppassword = models.CharField(max_length=10)
    smtpport = models.CharField(max_length=5)
    icon = models.ImageField(blank='True', upload_to='images/')
    facebook = models.CharField(max_length=20)
    twitter = models.CharField(max_length=20)
    instagram = models.CharField(max_length=20)
    aboutus = RichTextUploadingField()
    reference = RichTextUploadingField()
    contact = RichTextUploadingField(blank='True')
    status = models.CharField(max_length=10, choices=STATUS)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class ContactFormMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name = models.CharField(blank='True', max_length=20)
    email = models.CharField(blank='True', max_length=50)
    subject = models.CharField(blank='True', max_length=50)
    message = models.CharField(blank='True', max_length=255)
    status = models.CharField(max_length=15, choices=STATUS, default='New')
    ip = models.CharField(blank='True', max_length=20)
    note = models.CharField(blank='True', max_length=15)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ContactFormu(ModelForm):
    class Meta:
        model = ContactFormMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': TextInput(attrs={'class': 'contact_input', 'placeholder': 'Name & Surname'}),
            'subject': TextInput(attrs={'class': 'contact_input ', 'placeholder': 'Subject'}),
            'email': TextInput(attrs={'class': 'contact_input', 'placeholder': 'Email Address'}),
            'message': Textarea(attrs={'class': 'contact_textarea contact_input', 'placeholder': 'Your Message', 'rows' : '5'}),
        }



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(blank=True, max_length=20)
    address = models.CharField(blank=True, max_length=150)
    city = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    image = models.ImageField(blank=True, upload_to='images/users/')

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' '+self.user.last_name + ' [ ' +self.user.username + ' ] '


    def image_tag(self):
        return mark_safe('<img src="{}" height="50" />'.format(self.image.url))
    image_tag.short_description = 'Image'


class UserProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'city', 'country', 'image']
