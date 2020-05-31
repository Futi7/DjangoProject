from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from djangoProject import settings
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('places/', include('places.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('contact/', views.contact, name='contact'),
    path('aboutus/', views.aboutus, name='about'),
    path('reference/', views.reference, name='reference'),
    path('category/<int:id>/<slug:slug>/', views.category_places, name='category'),
    path('place/<int:id>/<slug:slug>/', views.place_detail, name='place'),
    path('search/', views.place_search, name="place_search")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)