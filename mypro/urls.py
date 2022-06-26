from django.urls import include
from django.contrib import admin
from django.urls import path
from django.conf.urls import handler404
import mysite
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mysite.urls')),
]
handler404=mysite.views.error_404