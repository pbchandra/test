from django.urls import path

from . import views


urlpatterns =[
     
    path('',views.index,name='index'),
    path('Encrypt_and_send',views.Encrypt_and_send,name='Encrypt_and_send'),
    path('Encrypt_and_download',views.Encrypt_and_download,name='Encrypt_and_download'),
    path('decbtn',views.decbtn,name='decbtn'),
    path('encryptandsend',views.encryptandsend,name='encryptandsend'),
    path('encryptanddownload',views.encryptanddownload,name='encryptanddownload'),
    path('decryption',views.decryption,name='decryption'),
    path('userdecryption',views.userdecryption,name='userdecryption'),
    path('user_decrypt',views.user_decrypt,name='user_decrypt'),

    path('sent',views.sent,name='sent'),
    path('received',views.received,name='received'),


    ]
