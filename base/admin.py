from django.contrib import admin

# Register your models here.
from .models import Room, RoomMembership, ChatBox, Tag, StudyMaterials,UserProfile,Followrequest, Folder

admin.site.register(RoomMembership)
admin.site.register(StudyMaterials)
admin.site.register(ChatBox)
admin.site.register(Room)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Followrequest)
admin.site.register(Folder)