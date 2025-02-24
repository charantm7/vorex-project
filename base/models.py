from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name="rooms",null=True)
    name = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tag, related_name="rooms")
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    members_count = models.ManyToManyField(User, related_name="member_count")
    def __str__(self):
        return self.name
    def member_count(self):
        return self.members_count.count()


class RoomMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="folders",null=True, blank=True)  # 📁 Folder belongs to Room

    def __str__(self):
        return self.name

class StudyMaterials(models.Model):
    upload_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="myuploads", null=True)  
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='study_materials',null=True, blank=True)  
    title = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="study_materials/")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.room != self.folder.room:
            raise ValueError("The study material's room must match the folder's room.")
        super().save(*args, **kwargs)
 

class ChatBox(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages", null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="groupcreation", null=True)
    group_name = models.CharField(max_length=20,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.group_name or "No-Name"
    
class ChatBoxMembership(models.Model):
    message_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="chatbox", null=True)
    chat_box = models.ForeignKey(ChatBox, on_delete=models.CASCADE, related_name="members",null=True)
    content = models.CharField(max_length=255,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f'{self.message_by.username if self.message_by else "Unknown user"} : {self.content or ""}'
    
    class Meta:
        ordering = ['created_at']

class RoomChatIndividual(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="individual_messages", null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", null=True)
    content = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__ (self):
        return f'{self.sender.username} : {self.content}'




class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_pic = models.ImageField(upload_to="profile_pics/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rooms = models.ManyToManyField(Room, related_name="profile-rooms+")
    study_materials = models.ManyToManyField(StudyMaterials, related_name="study_materials")
    bio = models.TextField(blank=True, null=True, max_length=100)
    followers = models.ManyToManyField("self", related_name="followers")
    def __str__(self):
        return self.user.username

class Followrequest(models.Model):
    from_user = models.ForeignKey(User, related_name="send_follow_request", on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name="recieved_follow_request", on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"
    

