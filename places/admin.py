from django.contrib import admin

# Register your models here.
from places.models import Category, Places, Images




class PlacesImageInLine(admin.TabularInline):
    model = Images
    extra = 5



class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class PlacesAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'price', 'status']
    list_filter = ['status', 'category', 'price']
    inlines = [PlacesImageInLine]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'place']


admin.site.register(Category, CategoryAdmin)
admin.site.register(Places, PlacesAdmin)
admin.site.register(Images, ImagesAdmin)