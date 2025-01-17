from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Room, RoomMembership, ChatBox, StudyMaterials, UserProfile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm,ProfileForm,UserForm
from django.contrib.auth.models import User

def home(request):
    room = Room.objects.all()
    tag = Tag.objects.all()
    return render(request, 'base/home.html', {'rooms': room,'tags': tag})

@login_required(login_url='User_login')
def rooms(request,pk):
    room = get_object_or_404(Room, pk=pk)
    context = {'rooms': room,'members':room.member_count}
    if request.user in room.members_count.all():
        return render(request, 'base/room.html',context )
    else:
        messages.error(request, 'You are not a member of this room! join the room to continue')
        return redirect('Home')

def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    room = Room.objects.filter(tags=tag)
    context = {'tag': tag,'rooms': room}
    return render(request, 'base/tags.html', context)

def auth_page(request):
    return render(request, 'base/authentication/auth.html')


def user_signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists! Try another username')
            return redirect('User_signup')
        if password != confirm_password:
            messages.error(request, 'Password does not match')
            return redirect('User_signup')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('Home')
    return render(request, 'base/authentication/auth.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return redirect('User_login')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You are logged in')
            return redirect('Home')
        else:
            messages.error(request, 'Invalid password')
    return render(request, 'base/authentication/auth.html')

@login_required(login_url='User_login')
def user_logout(request):
    logout(request)
    messages.success(request, 'You are logged out')
    return redirect('Home')

@login_required(login_url='User_login')
def create_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.created_by = request.user
            form.save()
            return redirect('Home')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = RoomForm()
    context = {'form':form}
    return render(request, 'base/home.html',context)

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
    messages.success(request, 'Room deleted successfully')
    return redirect('Home')

def join_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    if request.user in room.members_count.all():
        messages.error(request, 'You are already a member of this room')
        return redirect('Rooms', pk=pk)
    else:
        room.members_count.add(request.user)
        return redirect('Rooms', pk=pk)

def exit_room(request, pk):
    room = get_object_or_404(Room, pk=pk)
    room.members_count.remove(request.user)
    return redirect('Home') 

@login_required(login_url='User_login')
def profile(request, user_tag):
    user = User.objects.get(username=user_tag)
    room = Room.objects.filter(created_by=user)
    if not UserProfile.objects.filter(user=user).exists():
        UserProfile.objects.create(user=user)
        profile = UserProfile.objects.get(user=user)
        
    else:
        profile = UserProfile.objects.get(user=user)
    context = {'user': user, 'rooms': room, 'profile': profile}
    return render(request, 'base/profile.html', context)

@login_required(login_url='User_login')
def profile_update(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('Profile', username=request.user.username)
        else:
            messages.error(request, 'Invalid form') 

    else:
        form = ProfileForm(instance=profile)
   
    context = {'form':form}
    return render(request, 'base/updateprofile.html', context)

@login_required(login_url='User_login')
def user_update(request,user_tag):
    user = User.objects.get(username=user_tag)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save()
            updated_user.save()
            return redirect('Profile', user_tag=updated_user.username)
        
        else:
            messages.error(request, 'Invalid form')
    else:
        form = UserForm(instance=user)
    context = {'form':form}
    return render(request, 'base/updateuser.html', context)
