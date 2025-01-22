from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='Home'),
    
    path('rooms/<str:room_name>',views.rooms, name='Rooms'),
    path('authentication/',views.auth_page, name='auth_page'),
    path('user_login/',views.user_login, name='User_login'),
    path('profile/<str:user_tag>/',views.profile, name='Profile'),
    path('update_user/<str:user_tag>/',views.user_update, name='Update-user'),
    path('update_profile/<str:user_tag>/',views.profile_update, name='Update-profile'),
    path('user_signup/',views.user_signup, name='User_signup'),
    path('user_logout/',views.user_logout, name='User_logout'),
    path('create_room/',views.create_room, name='Create-room'),
    path('edit_room/<str:room_name>/',views.edit_room, name='Edit-room'),
    path('delete_room/<str:room_name>/',views.delete_room, name='Delete-room'),
    path('<str:tag_name>/',views.tag, name='Tag'),
    path('join_room/<str:room_name>/',views.join_room, name='Join-room'),
    path('exit_room/<str:room_name>/',views.exit_room, name='Exit-room'),
    path('404-error/',views.error_404, name='Error-page'),
    path('room-members/<str:room_tag>/',views.room_member_count, name='Room-members'),
    path('send-follow-request/<int:user_id>/', views.send_follow_request, name='send-follow-request'),
    path('accept-follow-request/<int:request_id>/', views.accept_follow_request, name='accept-follow-request'),
    path('decline-follow-request/<int:request_id>/', views.reject_follow_request, name='decline-follow-request'),
    path('followers/<str:user_tag>/', views.followers_list, name='followers-list'),
    path('following/<str:user_tag>/', views.following_list, name='following-list'),
    path('follow-request/<str:user_tag>', views.follow_request, name='follow-request'),
    
]