from django.db import models
from django.contrib.auth.models import User

class UserFile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Associate file with a user
    file = models.FileField(upload_to='uploads/')  # File upload field
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Track upload time

    def __str__(self):
        return f"{self.user.username}'s file"
    
# Create your models here.
