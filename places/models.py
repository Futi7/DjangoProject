from django.db import models


class Category(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
        )

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank='True')
    keywords = models.CharField(max_length=200, blank='True')
    status = models.CharField(max_length=10, choices=STATUS)
    image = models.ImageField(blank='True', upload_to='images/')
    slug = models.SlugField()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)


    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Places(models.Model):
    STATUS = (
        ('True', 'Evet'),
        ('False', 'Hayır')
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200, blank='True')
    details = models.TextField()
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




class Images(models.Model):
    place = models.ForeignKey(Places, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(blank='True', upload_to='images/')






