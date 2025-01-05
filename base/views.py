from django.shortcuts import render, get_object_or_404, redirect
from .models import Tag, CustomUser, Room, RoomMembership, ChatBox, StudyMaterials
from .forms import Signup, Login
from django.contrib.auth.views import LoginView
def home(request):
    room = Room.objects.all()
    tag = Tag.objects.all()
    return render(request, 'base/home.html', {'rooms': room,'tags': tag})

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
    if request.method == 'POST':
        form = Signup(request.POST)
        if form.is_valid():
            user = form.save()
            user_login(request,user)
            return redirect('Home')
    else:
        form = Signup()
    return render(request, 'base/authentication/auth.html',{'form':form})

