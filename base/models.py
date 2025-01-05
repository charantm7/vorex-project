from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=100)
    groups = models.ManyToManyField('auth.Group', related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  
        blank=True
    )
    profile_picture = models.ImageField(upload_to='profile_picture/', blank=True, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=500, unique=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE,related_name="rooms")
    name = models.CharField(max_length=50)
    tags = models.ManyToManyField(Tag, related_name="rooms", blank=False)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_private = models.BooleanField(default=False)
    members_count = models.ManyToManyField(CustomUser, related_name="member_count")
    def __str__(self):
        return self.name
    def member_count(self):
        return self.members_count.count()


class RoomMembership(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class StudyMaterials(models.Model):
    upload_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="myuploads")
    title = models.CharField(max_length=255, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="study_materials/")   

class ChatBox(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

