from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addcomment/<int:id>', views.addcomment, name='addcomment'),
    path('place_delete_image/<int:id>', views.place_delete_image, name='place_delete_image'),
    path('image_gallery/<int:id>', views.image_gallery, name='image_gallery'),
]
