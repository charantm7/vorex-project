from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='Home'),
    path('rooms/<str:pk>',views.rooms, name='Rooms'),
    path('authentication/',views.auth_page, name='auth_page'),
    path('user_login/',views.user_login, name='User_login'),
    path('user_signup/',views.user_signup, name='User_signup'),
    path('create_room/',views.create_room, name='Create-room'),
    path('edit_room/<str:pk>/',views.edit_room, name='Edit-room'),
    path('<str:tag_name>/',views.tag, name='Tag'),
    
]