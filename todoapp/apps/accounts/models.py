from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='user_avatars/%Y/%m/%d', blank=True, default='user_avatars/avatar.jpeg')
    # for trello
    trello_api_key = models.CharField(max_length=32, blank=True, null=True)
    trello_api_secret = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"
