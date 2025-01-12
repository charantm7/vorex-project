from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Room, RoomMembership, ChatBox, StudyMaterials
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm
from django.contrib.auth.models import User

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
    context = {'tag': tag,'rooms': room}
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

def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Home')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = RoomForm()
    context = {'form':form}
    return render(request, 'base/createroom.html',context)

def edit_room(request,pk):
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = RoomForm(instance=room)
    context = {'form':form}
    return render(request, 'base/createroom.html',context)

def delete_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.delete()
    return redirect('Home')

def join_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.user in room.members_count.all():
        messages.error(request, 'You are already a member of this room')
        return redirect('Rooms', pk=pk)
    else:
        room.members_count.add(request.user)
        return redirect('Rooms', pk=pk)

