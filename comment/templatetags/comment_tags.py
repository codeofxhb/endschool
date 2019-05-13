from django import template
from django.contrib.contenttypes.models import ContentType
from ..models import Comment
from ..forms import Commentform

register = template.Library()

@register.simple_tag()
def get_comment_count(blog):
    content_type = ContentType.objects.get_for_model(blog)
    return Comment.objects.filter(content_type=content_type, object_id=blog.pk).count()

@register.simple_tag()
def get_comment_form(blog):
    content_type = ContentType.objects.get_for_model(blog)
    form = comment_form = Commentform(initial={
        'content_type': content_type.model,
        'object_id': blog.pk,
        'reply_comment_id': 0,
    })
    return form

@register.simple_tag()
def get_comment_list(blog):
    content_type = ContentType.objects.get_for_model(blog)
    comments = Comment.objects.filter(content_type=content_type, object_id=blog.pk, parent_comment=None)
    return comments.order_by('-comment_time')