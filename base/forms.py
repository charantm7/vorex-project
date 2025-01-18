from django.forms import ModelForm
from .models import Room, UserProfile
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'tags','is_private']
        

class ProfileForm(ModelForm):
    class Meta:
        model= UserProfile
        fields = ['profile_pic', 'bio']
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']

