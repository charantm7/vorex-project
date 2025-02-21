from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, Room, RoomMembership, ChatBox, StudyMaterials, UserProfile, Followrequest
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RoomForm, ProfileForm, UserForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db.models import Q



def home(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            room = Room.objects.all()
        else:
            room = Room.objects.filter(
                Q(is_private=False) | Q(members_count=request.user)
            ).distinct()
    else:
        room = Room.objects.filter(
            Q(is_private=False))
    tag = Tag.objects.all()
    context = {'rooms': room, 'tags': tag}
    return render(request, 'base/home.html', context)


@login_required(login_url='User_login')
def rooms(request, room_name):
    room = get_object_or_404(Room, name=room_name)
    # user = get_object_or_404(User, username=room.created_by)
    members_joined = room.members_count.all()
    profile = get_object_or_404(UserProfile, user=room.created_by)
    context = {'rooms': room, 'members': room.member_count, 'profile':profile, 'members_joined': members_joined}
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
    messages.success(request, 'Exited from the room successfully')
    return redirect('Home')


@login_required(login_url='User_login')
def profile(request, user_tag):
    user = User.objects.get(username=user_tag)
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            room = Room.objects.filter(created_by=user)
        elif request.user == user:
            room = Room.objects.filter(created_by=user)
        else:
            room = Room.objects.filter(is_private=False,created_by=user)

    if not UserProfile.objects.filter(user=user).exists():
        UserProfile.objects.create(user=user)
        profile = UserProfile.objects.get(user=user)
    else:
        profile = UserProfile.objects.get(user=user)

    if request.user.is_authenticated:
        is_follower = user.profile in request.user.profile.followers.all()

    send_follow_request = Followrequest.objects.filter(from_user=request.user).values_list('to_user__id', flat=True)
    context = {'user': user, 'room': room, 'profile': profile,'is_follower':is_follower,'send_follow_request':send_follow_request}
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


def room_member_count(request, room_tag):
    room = get_object_or_404(Room, name=room_tag)
    members = room.members_count.all()
    context = {'room':room,'members':members}
    return render(request, 'base/room_members.html', context)

@login_required(login_url='User_login')
def send_follow_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    if Followrequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        return redirect('Profile', user_tag=to_user.username)
    request = Followrequest.objects.create(from_user=request.user, to_user=to_user)
    request.save()
    return redirect('Profile', user_tag=to_user.username)


def unfollow_request(request, user_id):
    to_user = get_object_or_404(User, id=user_id)
    to_user_profile = to_user.profile

    if request.user.is_authenticated:
        current_user = request.user.profile
    
        if current_user in to_user_profile.followers.all():
            to_user_profile.followers.remove(current_user)
            return JsonResponse({'success': True, 'message': 'Unfollowed successfully.'})
        else:
            return JsonResponse({'success': False, 'message': 'You are not following this user.'})
    return redirect('Profile', user_tag=to_user.username)

@login_required(login_url='User_login')
def accept_follow_request(request, request_id):
    followrequest = get_object_or_404(Followrequest, id=request_id , to_user=request.user)
    request.user.profile.followers.add(followrequest.from_user.profile  )
    followrequest.from_user.profile.followers.add(request.user.profile)
    followrequest.delete()
    return redirect('Profile', user_tag=request.user.username)


@login_required(login_url='User_login')
def reject_follow_request(request, request_id):
    follow_request = Followrequest.objects.filter(id=request_id, to_user=request.user).first() # Replace with an actual error page
    if follow_request:
        # If the follow request exists, delete it
        follow_request.delete()
        return redirect('Profile', user_tag=request.user.username)
    return redirect('Profile', user_tag=request.user.username)

def followers_list(request, user_tag):
    user = get_object_or_404(User, username=user_tag)
    followers = user.profile.followers.all()
    context = {'followers': followers}
    return render(request, 'base/follower_list.html', context)

def following_list(request, user_tag):
    user = get_object_or_404(User, username=user_tag)
    following = user.following.all()
    return render(request, 'base/follower_list.html', {'following': following})
    
def follow_request(request, user_tag):
    user = get_object_or_404(User, username=user_tag)
    follow_request = Followrequest.objects.filter(to_user=request.user)
    context = {'user': user, 'follow_request': follow_request}
    return render(request, 'base/follow_request.html', context)

def error_404(request):
    return render(request, 'base/error_page.html')