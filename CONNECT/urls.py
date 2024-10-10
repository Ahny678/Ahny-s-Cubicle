from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.Jumpin, name='Jumpin'),
    path('jail', views.jail, name='jail'),
    path('PostMessages', views.PostMessages, name='PostMessages'),
    path('<str:chatroom>/', views.TheRoom, name='chatroom'),
    path('getMessages/<str:chatroom>/', views.getMessages, name='getMessages'),
    path('chatChecker', views.chatChecker, name='chatChecker'),
    path('Register', views.Register, name='Register'),
    path('sendEmail', views.sendEmail, name='sendEmail')

] 