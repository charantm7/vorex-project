from django.forms import ModelForm
from .models import Room, UserProfile

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

class ProfileForm(ModelForm):
    class Meta:
        model: UserProfile
        fields = '__all__'
        


