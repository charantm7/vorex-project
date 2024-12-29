from django.shortcuts import render
from .models import CustomUser, Room, RoomMembership, ChatBox, StudyMaterials



def home(request):
    room = Room.objects.all()
    return render(request, 'base/home.html', {'rooms': room})

def rooms(request):
    return render(request, 'base/room.html')

def auth_page(request):
    return render(request, 'base/authentication/auth.html')

def user_login(request):
    pass

def user_signup(request):
    pass


