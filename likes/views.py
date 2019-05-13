from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import Likecount, Likerecord
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

# Create your views here.

def success_json(like_counts):
    data = {
        'status': 'SUCCESS',
        'like_counts': like_counts,
    }
    return JsonResponse(data)

def error_json(code, message):
    data = {
        'status': 'ERROR',
        'code': code,
        'message': message,
    }
    return JsonResponse(data)

def give_like(request):
    '''获取数据'''
    user = request.user
    if not user.is_authenticated:
        return error_json(400, 'You have not login yet!')

    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))
    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return error_json(401, 'object is not exist!')

    '''处理数据，if_like为true时为点赞，否则取消点赞'''
    if request.GET.get('is_like') == 'true':
        like_record, created = Likerecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        '''通过created判断是否点过赞'''
        if created:
            like_count, created = Likecount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_counts += 1
            like_count.save()
            return success_json(like_count.like_counts)
        else:
            return error_json(402, 'You have gaven a like!')
    else:
        if Likerecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            like_record = Likerecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = Likecount.objects.get_or_create(content_type=content_type, object_id=object_id)
            if not created:
                like_count.like_counts -= 1
                like_count.save()
                return success_json(like_count.like_counts)
            else:
                return error_json(404, 'data error!')
        else:
            return error_json(403, 'You have not liked is yet!')


