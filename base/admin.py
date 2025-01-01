from django.contrib import admin

# Register your models here.
from .models import CustomUser, Room, RoomMembership, ChatBox, Tag, StudyMaterials

admin.site.register(CustomUser)
admin.site.register(RoomMembership)
admin.site.register(StudyMaterials)
admin.site.register(ChatBox)
admin.site.register(Room)
admin.site.register(Tag)