from django.shortcuts import render, reverse, redirect, HttpResponse
from .models import Comment
from django.contrib.contenttypes.models import ContentType
from .forms import Commentform
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.
def comment_add(request):
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    comment_form = Commentform(request.POST, user=request.user)
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text'].replace('&nbsp;', '')
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root_comment = parent.root_comment if parent.root_comment is not None else parent
            comment.parent_comment = parent
            comment.reply_to = parent.user
        comment.save()

        '''发送邮件通知'''
        comment.send_email_for_comments_or_reply()
        data = {
            'status': 'SUCCESS',
            'username': comment.user.get_niname_or_username(),
            'comment_time': timezone.localtime(comment.comment_time).strftime('%Y{y}%m{m}%d{d} %H{a}%M').format(y='年', m='月', d='日', a=':'),
            'text': comment.text,
            'content_type': ContentType.objects.get_for_model(comment).model,
        }
        if parent is not None:
            data['reply_to'] = comment.reply_to.get_niname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_comment_pk'] = comment.root_comment.pk if comment.root_comment is not None else ''

    else:
        data = {
            'status': 'ERROR',
            'message': list(comment_form.errors.values())[0][0],
        }
    return JsonResponse(data)

    # if not request.user.is_authenticated:
    #     return HttpResponse("您还没有登录哦~~")
    #
    # text = request.POST.get('text').strip()
    # if text == '':
    #     return HttpResponse("不能评论空内容哦~~")
    #
    # try:
    #     object_id = int(request.POST.get('object_id', ''))
    #     '''从前端传递过来的都是字符串数据'''
    #     content_type = request.POST.get('content_type', '')
    #     '''获取关联Comment的模型'''
    #     model_class = ContentType.objects.get(model=content_type).model_class()
    #     '''获取该comment对象关联的具体blog对象'''
    #     content_object = model_class.objects.get(pk=object_id)
    # except Exception as e:
    #     return HttpResponse("该新闻不在了~~")
    #
    # comment = Comment()
    # comment.user = request.user
    # comment.text = text
    # comment.content_object = content_object
    # comment.save()
    #
    # '''获取请求头信息页面信息，任然返回当前页面,不存在具体头信息时，返回首页'''
    # referer = request.META.get('HTTP_REFERER', reverse('index'))
    # return redirect(referer)
