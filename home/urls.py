from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('aboutus/', views.aboutus, name='aboutus'),
    path('references/', views.reference, name='reference'),
    path('contact/', views.contact, name='contact'),
]
