from django.forms import ModelForm
from .models import Room, UserProfile
from django.contrib.auth.models import User

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['created_by', 'created_at', 'updated_at','members_count']

class ProfileForm(ModelForm):
    class Meta:
        model= UserProfile
        fields = ['profile_pic', 'bio', 'rooms', 'study_materials', 'user']
        


