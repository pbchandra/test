from django.contrib import admin
from django.urls import path
 
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns =[
     
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('login/login_test',views.login_test,name='login_test'),
    path('profile/',views.profile,name='profile'),
    path('profile_update',views.profile_update,name='profile_update'),
    path('profile/rest_password',views.rest_password,name='rest_password'),
     path('logout',views.logout,name='logout'),
     path('dashboard',views.dashboard,name='dashboard'),
    #Build in password reset
    path('password_reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
    ]
