from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user_avatars/%Y/%m/%d', blank=True, default='user_avatars/avatar.jpeg')

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
