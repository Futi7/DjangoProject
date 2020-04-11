from django.db import models


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
    aboutus = models.TextField()
    reference = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title