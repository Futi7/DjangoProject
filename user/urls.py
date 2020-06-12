from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('update/', views.user_update, name='update'),
    path('password/', views.change_password, name='change'),
    path('comments/', views.comments, name='comments'),
    path('deletecomment/<int:id>/', views.deletecomment, name='deletecomment'),

    path('places/', views.places, name='places'),
    path('user_new_place/', views.user_new_place, name='user_new_place'),
    path('user_edit_place/<int:id>/', views.user_edit_place, name='user_edit_place'),
]
