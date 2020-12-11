from django.db import models
from django.urls import reverse

from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from todoapp.ru_taggit import RuTaggedItem

class TodoItem(models.Model):
    PRIORITY_HIGH = 1
    PRIORITY_MEDIUM = 2
    PRIORITY_LOW = 3

    PRIORITY_CHOICES = [
        (PRIORITY_HIGH, "Высокий приоритет"),
        (PRIORITY_MEDIUM, "Средний приоритет"),
        (PRIORITY_LOW, "Низкий приоритет"),
    ]
    # verbose_neme = <title>
    # help_text = <br><span>...</span>
    description = models.CharField(max_length=64)
    is_completed = models.BooleanField("выполнено", default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    priority = models.IntegerField(
        "Приоритет", choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM
    )
    tags = TaggableManager(through=RuTaggedItem)
    trello_id_board = models.CharField(max_length=50, blank=True, null=True)
    trello_id_card = models.CharField(max_length=50, blank=True, null=True)


    def __str__(self):
        return self.description.lower()

    def get_absolute_url(self):
        return reverse("tasks:details", args=[self.pk])

    class Meta:
        ordering = ('-created',)
    

class TagCount(models.Model):
    tag_slug = models.CharField(max_length=128)
    tag_name = models.CharField(max_length=128)
    tag_id = models.PositiveIntegerField(default=0)
    tag_count = models.PositiveIntegerField(db_index=True, default=0)


class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()
