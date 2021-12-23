from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf.urls import handler404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('media4.urls', namespace='media4')),
]

handler404 = 'media4.views.notfound'