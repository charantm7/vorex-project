from django.contrib import admin

# Register your models here.
from .models import  Room, RoomMembership, ChatBox, Tag, StudyMaterials

admin.site.register(RoomMembership)
admin.site.register(StudyMaterials)
admin.site.register(ChatBox)
admin.site.register(Room)
admin.site.register(Tag)