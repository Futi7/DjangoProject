from django.contrib import admin

# Register your models here.
from places.models import Category, Places


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class PlacesAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'status']
    list_filter = ['status', 'category', 'price']



admin.site.register(Category, CategoryAdmin)

admin.site.register(Places, PlacesAdmin)