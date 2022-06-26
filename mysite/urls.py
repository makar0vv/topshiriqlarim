from django.urls import path
from .views import *
import mysite.views
from django.conf.urls import handler404

urlpatterns=[
    path('',home,name='home-page'),
    path('signup/',signup,name='signup-page'),
    path('login/',loginForm,name='login-page'),
    path('logout/',logout_view,name='logout-page'),
    path('task_delete/<int:pk>',task_delete,name='task-delete-page'),
    path('task_edit/<int:pk>',task_edit,name='task-edit-page'),
    path('dashboard/', profilepage, name='profile-page'),
    path('check_user/',check_user,name='check_user'),
    path('dashboard/change_password/',change_password,name='change_password'),
    path('forget_password/',forget_password,name='forget_password'),
    path('dashboard/reset_password/', reset_password, name='reset_password'),
    path('dashboard/contact/', contact, name='contact_page'),
]

handler404 = mysite.views.error_404