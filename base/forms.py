from django.forms import ModelForm
from .models import Room, UserProfile, ChatBox
from django.contrib.auth.models import User
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['name', 'description', 'tags','is_private']
        

class ProfileForm(ModelForm):
    class Meta:
        model= UserProfile
        fields = ['profile_pic', 'bio']
        widgets = {
            'profile_pic': forms.ClearableFileInput(attrs={'accept': 'profile_pic/*'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_pic'].initial = None
        
class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']


class ChatBoxForm(forms.ModelForm):
    class Meta:
        model = ChatBox
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Type a message...'})
        }