from django.shortcuts import render, get_object_or_404
from .models import Tag, CustomUser, Room, RoomMembership, ChatBox, StudyMaterials

def home(request):
    room = Room.objects.all()
    tag = Tag.objects.all()
    return render(request, 'base/home.html', {'rooms': room,'tags': tag})

def rooms(request,pk):
    room = get_object_or_404(Room, pk=pk)
    return render(request, 'base/room.html',{'rooms': room} )

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    room = Room.objects.filter(tags=tag)
    context = {'tags': tag,'rooms': room}
    return render(request, 'base/tags.html', context)

def auth_page(request):
    return render(request, 'base/authentication/auth.html')

def user_login(request):
    pass

def user_signup(request):
    pass


