from django.db.models.signals import m2m_changed
from django.dispatch import receiver
# from taggit.models import Tag

from tasks.models import TagCount, TodoItem

@receiver(m2m_changed, sender=TodoItem.tags.through)
def task_tags_updated(sender, instance, action, model, **kwargs):
    if action != 'post_add':
        return
    print('---------------------')
    print('model', model)
    print('model', model.id)
    print('model', model.taggit_taggeditem_items)
    print('model', model.objects.all())
    print('**********************')
    print('model', str(model.taggit_taggeditem_items))
    
    print('kwargs', kwargs)
    print('sender', sender)


    print('instance', instance)

    count = model.taggit_taggeditem_items.count()
    t = TagCount.object.filter(tag_id=model.id).first()
    if t is None:
        t = TagCount.object.get_or_create(
            tag_slug=model.slug,
            tag_name=model.name,
            tag_id=model.id,
            tag_count=count,
        )
    else:
        t.tag_count = count

    t.save()
