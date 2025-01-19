from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Room, RoomMembership, ChatBox, StudyMaterials, UserProfile
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm, ProfileForm, UserForm
from django.contrib.auth.models import User


def home(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            room = Room.objects.all()
        else:
            room = Room.objects.filter(is_private=False) | Room.objects.filter(
                created_by=request.user)
    else:
        room = Room.objects.filter(is_private=False)
    tag = Tag.objects.all()
    context = {'rooms': room, 'tags': tag}
    return render(request, 'base/home.html', context)


@login_required(login_url='User_login')
def rooms(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    context = {'rooms': room, 'members': room.member_count}
    if request.user in room.members_count.all():
        return render(request, 'base/room.html', context)
    else:
        messages.error(
            request, 'You are not a member of this room! join the room to continue')
        return redirect('Home')


def tag(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    room = Room.objects.filter(tags=tag)
    context = {'tag': tag, 'rooms': room}
    return render(request, 'base/tags.html', context)


def auth_page(request):
    return render(request, 'base/authentication/auth.html')


def user_signup(request):
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?~"
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            messages.error(
                request, 'Username already exists! Try another username')
            return redirect('User_signup')
        elif len(username) < 3:
            messages.error(
                request, 'Username must be at least 3 characters long')
            return redirect('User_signup')
        elif len(username) > 15:
            messages.error(request, 'Username must be less than 15 characters')
            return redirect('User_signup')
        elif len(password) < 8:
            messages.error(
                request, 'Password must be at least 8 characters long')
            return redirect('User_signup')
        elif len(password) > 20:
            messages.error(
                request, 'Password must be less than 20 characters')
            return redirect('User_signup')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists! Try another email')
            return redirect('User_signup')
        elif not any(char.isdigit() for char in password):
            messages.error(request, 'Password must contain at least one digit')
            return redirect('User_signup')
        elif not any(char.isupper() for char in password):
            messages.error(
                request, 'Password must contain at least one uppercase letter')
            return redirect('User_signup')
        elif not any(char.islower() for char in password):
            messages.error(
                request, 'Password must contain at least one lowercase letter')
            return redirect('User_signup')
        elif not any(char in special_characters for char in password):
            messages.error(
                request, 'Password must contain at least one special character')
            return redirect('User_signup')
        elif password != confirm_password:
            messages.error(request, 'Password does not match')
            return redirect('User_signup')
        elif (username == 'admin' or username == 'Admin' or username == 'ADMIN' or password == 'admin' or password == 'Admin' or password == 'ADMIN'):
            messages.error(request, 'Username or password cannot be admin') 
            return redirect('User_signup')
        elif (password == username or password == email):
            messages.error(request, 'Password cannot be username or email')
            return redirect('User_signup')
        else:
            user = User.objects.create_user(
                username=username, email=email, password=password)
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
            form.members_count.add(form.created_by)
            return redirect('Home')

        else:
            messages.error(request, 'Invalid form')
            return redirect('Create-room')
    else:
        form = RoomForm()
    context = {'form': form}
    return render(request, 'base/createroom.html', context)


def edit_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('Home')
        else:
            messages.error(request, 'Invalid form')
    else:
        form = RoomForm(instance=room)
    context = {'form': form}
    return render(request, 'base/editroom.html', context)


def delete_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    room.delete()
    messages.success(request, 'Room deleted successfully')
    return redirect('Home')


def join_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    if request.user in room.members_count.all():
        messages.error(request, 'You are already a member of this room')
        return redirect('Rooms', room_name=room_name)
    else:
        room.members_count.add(request.user)
        room.save()
        messages.success(request, 'You are now a member of this room')
        return redirect('Rooms', room_name=room_name)


def exit_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    room.members_count.remove(request.user)
    room.save()
    messages.success(request, 'Exited from the room successfully')
    return redirect('Home')


@login_required(login_url='User_login')
def profile(request, user_tag):
    user = User.objects.get(username=user_tag)
    room = Room.objects.filter(created_by=user) | Room.objects.filter(members_count=user)
    if user.username == user_tag:
        private = Room.objects.filter(is_private=True) | Room.objects.filter(is_private=False)
    if not UserProfile.objects.filter(user=user).exists():
        UserProfile.objects.create(user=user)
        profile = UserProfile.objects.get(user=user)

    else:
        profile = UserProfile.objects.get(user=user)
    context = {'user': user, 'rooms': room, 'profile': profile, 'private': private}
    return render(request, 'base/profile.html', context)


@login_required(login_url='User_login')
def profile_update(request, user_tag):
    user = User.objects.get(username=user_tag)
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('Profile', user_tag=user_tag)
        else:
            messages.error(request, 'Invalid form')

    else:   
        form = ProfileForm(instance=profile)

    context = {'form': form, 'profile': profile}
    return render(request, 'base/updateprofile.html', context)


@login_required(login_url='User_login')
def user_update(request, user_tag):
    user = User.objects.get(username=user_tag)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            updated_user = form.save()
            updated_user.save()
            messages.success(request, 'User updated successfully')
            return redirect('Profile', user_tag=updated_user.username)

        else:
            messages.error(request, 'Invalid form')
    else:
        form = UserForm(instance=user)
    context = {'form': form}
    return render(request, 'base/updateuser.html', context)
