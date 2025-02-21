from rest_framework import serializers
from .models import ChatBox

class ChatBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatBox
        fields = '__all__'

        