from django.db import models

class AdminUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=255)  # hashed password
    full_name = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=20, blank=True, null=True)
    profile_photo = models.ImageField(upload_to="admin_photos/", blank=True, null=True, default="admin_photos/default.jpg")

    def __str__(self):
        return self.username
