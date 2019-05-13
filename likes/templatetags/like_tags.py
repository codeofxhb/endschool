from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Likecount, Likerecord

register = template.Library()

@register.simple_tag
def get_like_counts(object):
    content_type = ContentType.objects.get_for_model(object)
    like_count, created = Likecount.objects.get_or_create(content_type=content_type, object_id=object.pk)
    return like_count.like_counts

@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    if not user.is_authenticated:
        return ''
    if Likerecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model