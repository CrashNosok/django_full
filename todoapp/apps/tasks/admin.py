from django.contrib import admin
from tasks.models import TodoItem, Publisher

# admin.site.register(TodoItem)

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'website')
