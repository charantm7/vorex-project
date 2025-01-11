from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, User, Room, RoomMembership, ChatBox, StudyMaterials
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def home(request):
    room = Room.objects.all()
    tag = Tag.objects.all()
    return render(request, 'base/home.html', {'rooms': room,'tags': tag})

@login_required(login_url='User_login')
def rooms(request,pk):
    room = get_object_or_404(Room, pk=pk)
    context = {'rooms': room,'members':room.member_count}
    return render(request, 'base/room.html',context )

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    room = Room.objects.filter(tags=tag)
    context = {'tags': tag,'rooms': room}
    return render(request, 'base/tags.html', context)

def auth_page(request):
    return render(request, 'base/authentication/auth.html')


def user_signup(request):
    return render(request, 'base/authentication/auth.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Invalid password')

    return render(request, 'base/authentication/auth.html')
@login_required(login_url='User_login')
def user_logout(request):
    logout(request)
    return redirect('Home')