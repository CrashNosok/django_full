from django.contrib import admin
from tasks.models import TodoItem, Publisher, TagCount

# admin.site.register(TodoItem)

@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = ('description', 'is_completed', 'created')


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'website')

@admin.register(TagCount)
class TagCountAdmin(admin.ModelAdmin):
    list_display = ('tag_slug', 'tag_name', 'tag_id', 'tag_count',)
