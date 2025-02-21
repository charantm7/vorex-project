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

class StudyMaterials(models.Model):
    upload_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="myuploads")
    title = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="study_materials/")   

class ChatBox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

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
    
    