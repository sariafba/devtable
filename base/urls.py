from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.registerUser, name="signup"),
    path("login/", views.loginUser, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("update-user/", views.updateUser, name="update-user"),

    path('', views.home, name='home'),
    path('user/<int:id>', views.userProfile, name='user-profile'),

    path('room/<int:id>/', views.room, name='room'),
    path('create-room/', views.createRoom, name='create-room'),
    path('update-room/<int:id>', views.updateRoom, name='update-room'),
    path('delete-room/<int:id>', views.deleteRoom, name='delete-room'),

    path('delete-message/<int:id>', views.deleteMessage, name='delete-message'),

    path('topics/', views.topicsPage, name='topics'),
    path('activity/', views.activityPage, name='activity'),   
]
