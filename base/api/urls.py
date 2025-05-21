from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoutes),
    path('rooms/', views.getRooms),
    path('rooms/<str:pk>/', views.getRoom),

    # path('create-room/', views.createRoom, name='create-room'),
    # path('update-room/<str:pk>/', views.updateRoom, name='update-room'),
    # path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),
    # path('delete-message/<str:pk>/', views.deleteMessage, name='delete-message'),
]