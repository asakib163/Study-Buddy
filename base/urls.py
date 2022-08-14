from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginPage, name = 'login'),
    path('logout', views.logoutuser, name = 'logout'),
    path('register', views.registerPage, name = 'register'),
    
    path('', views.home, name = 'home'),
    path('room/<str:pk>', views.room, name = 'room'),
    path('profile/<str:pk>', views.userprofile, name = 'userprofile'),
    path('createroom', views.createRoom, name = 'createroom'),
    path('updateroom/<str:pk>', views.updateRoom, name = 'updateroom'),
    path('deleteroom/<str:pk>', views.deleteRoom, name = 'deleteroom'),
    path('deleteMessage/<str:pk>', views.deleteMessage, name = 'deleteMessage'),
    path('updateUser', views.updateUser, name = 'updateUser'),
    path('topics', views.topicpage, name = 'topics'),
    path('activities', views.activitypage, name = 'activities'),
]