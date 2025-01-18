from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='Home'),
    path('rooms/<str:room_name>',views.rooms, name='Rooms'),
    path('authentication/',views.auth_page, name='auth_page'),
    path('user_login/',views.user_login, name='User_login'),
    path('profile/<str:user_tag>/',views.profile, name='Profile'),
    path('update_user/<str:user_tag>/',views.user_update, name='Update-user'),
    path('update_profile/',views.profile_update, name='Update-profile'),
    path('user_signup/',views.user_signup, name='User_signup'),
    path('user_logout/',views.user_logout, name='User_logout'),
    path('create_room/',views.create_room, name='Create-room'),
    path('edit_room/<str:room_name>/',views.edit_room, name='Edit-room'),
    path('delete_room/<str:room_name>/',views.delete_room, name='Delete-room'),
    path('<str:tag_name>/',views.tag, name='Tag'),
    path('join_room/<str:room_name>/',views.join_room, name='Join-room'),
    path('exit_room/<str:room_name>/',views.exit_room, name='Exit-room'),
    
]