import datetime
import string
import random
import time
from django.utils import timezone
from django.db.models import Sum
from django.shortcuts import render, redirect, HttpResponse
from realing_quantity.utils import get_week_read_num, get_today_hot, get_yesteroday_hot
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.core.cache import cache
from django.contrib import auth
from django.contrib.auth.models import User
from django.urls import reverse
from .forms import Loginform, Regform, ChangeNinameform, BindEmailForm, ChangePasswordForm, FindPasswordForm
from django.http import JsonResponse
from .models import Profile
from django.core.mail import send_mail


def get_week_hot():
    today = timezone.now().date()
    week = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lte=today, read_details__date__gt=week) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]

def login(request):
    # username = request.POST.get('username')
    # password = request.POST.get('password')
    # user = auth.authenticate(request, username=username, password=password)
    # # referer = request.META.get('HTTP_REFERER', reverse('index'))
    #
    # if user is not None:
    #     auth.login(request, user)
    #     # return redirect(referer)
    #     return redirect('index')
    # else:
    #     return HttpResponse("用户名或者密码不正确！！")

    context = {}
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_week_read_num(blog_content_type)
    '''缓存设置，获取今日热门点击数据缓存'''
    today_hot_blogs = cache.get('today_hot_blogs')
    if today_hot_blogs is None:
        today_hot_blogs = get_today_hot(blog_content_type)
        cache.set('today_hot_blogs', today_hot_blogs, 3600)

    '''缓存设置，获取昨日热门点击数据缓存'''
    yesterday_hot_blogs = cache.get('yesterday_hot_blogs')
    if yesterday_hot_blogs is None:
        yesterday_hot_blogs = get_yesteroday_hot(blog_content_type)
        cache.set('yesterday_hot_blogs', yesterday_hot_blogs, 3600)

    '''缓存设置，获取本周热门点击数据缓存'''
    week_hot_blogs = cache.get('week_hot_blogs')
    if week_hot_blogs is None:
        week_hot_blogs = get_week_hot()
        cache.set('week_hot_blogs', week_hot_blogs, 3600)

    context = {
        'dates': dates,
        'read_nums': read_nums,
        'today_hot_blogs': get_today_hot(blog_content_type),
        'yesterday_hot_blogs': get_yesteroday_hot(blog_content_type),
        'week_hot_blogs': get_week_hot(),
    }


    if request.method == 'POST':
        login_form = Loginform(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        login_form = Loginform()

    context['login_form'] = login_form
    return render(request, 'login.html', context=context)

def login_for_medal(request):
    login_form = Loginform(request.POST)
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data = {
            'status': 'SUCCESS',
        }
    else:
        data = {
            'status': 'ERROR',
        }

    return JsonResponse(data)

def register(request):
    context = {}
    if request.method == 'POST':
        reg_form = Regform(request.POST, request=request)
        if reg_form.is_valid():
            '''获取用户模型字段值'''
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password_again = reg_form.cleaned_data['password']
            '''注册用户，创建用户'''
            user = User.objects.create_user(username=username, email=email, password=password_again)
            user.save()
            '''注册成功，清楚session'''
            if 'register_account_code' in request.session:
                del request.session['register_account_code']
            '''注册成功直接登录返回上级界面'''
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('index')))
        if 'register_account_code' in request.session:
            del request.session['register_account_code']
    else:
        reg_form = Regform()

    context['reg_form'] = reg_form
    return render(request, 'register.html', context=context)

def login_out(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('index')))

def user_info(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_week_read_num(blog_content_type)
    '''缓存设置，获取今日热门点击数据缓存'''
    today_hot_blogs = cache.get('today_hot_blogs')
    if today_hot_blogs is None:
        today_hot_blogs = get_today_hot(blog_content_type)
        cache.set('today_hot_blogs', today_hot_blogs, 3600)
    context = {
        'today_hot_blogs': today_hot_blogs,
    }
    return render(request, 'user_info.html', context=context)

def change_niname(request):
    if request.method == 'POST':
        comm_form = ChangeNinameform(request.POST, user=request.user)
        if comm_form.is_valid():
            niname_new = comm_form.cleaned_data['niname_new']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.niname = niname_new
            profile.save()
            return redirect(request.GET.get('from', reverse('index')))
    else:
        comm_form = ChangeNinameform()

    context = {
            'comm_form': comm_form,
            'page_title': '修改昵称',
            'form_title': '昵称修改',
            'submit_text': '保存',
            'back_url': request.GET.get('from', reverse('index')),
        }
    return render(request, 'forms.html', context=context)

def change_password(request):
    if request.method == 'POST':
        comm_form = ChangePasswordForm(request.POST, user=request.user)
        if comm_form.is_valid():
            user = request.user
            new_password = comm_form.cleaned_data['new_password']
            old_password = comm_form.cleaned_data['old_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(request.GET.get('from', reverse('index')))
    else:
        comm_form = ChangePasswordForm()

    context = {
            'comm_form': comm_form,
            'page_title': '修改密码',
            'form_title': '修改密码',
            'submit_text': '保存',
            'back_url': request.GET.get('from', reverse('index')),
        }
    return render(request, 'forms.html', context=context)

def find_password(request):
    if request.method == 'POST':
        comm_form = FindPasswordForm(request.POST, request=request)
        if comm_form.is_valid():
            email = comm_form.cleaned_data['email']
            new_password = comm_form.cleaned_data['new_password']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            if 'find_password_code' in request.session:
                del request.session['find_password_code']
            return redirect(request.GET.get('from', reverse('index')))
        if 'find_password_code' in request.session:
            del request.session['find_password_code']
    else:
        comm_form = FindPasswordForm()

    context = {
            'comm_form': comm_form,
            'page_title': '找回密码',
            'form_title': '找回密码',
            'submit_text': '提交',
            'back_url': request.GET.get('from', reverse('index')),
        }
    return render(request, 'find_password.html', context=context)

def bind_email(request):
    if request.method == 'POST':
        comm_form = BindEmailForm(request.POST, request=request)
        if comm_form.is_valid():
            email = comm_form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            if 'register_account_code' in request.session:
                del request.session['bind_email_code']
            return redirect(request.GET.get('from', reverse('index')))
        if 'register_account_code' in request.session:
            del request.session['bind_email_code']
    else:
        comm_form = BindEmailForm()

    context = {
            'comm_form': comm_form,
            'page_title': '绑定邮箱',
            'form_title': '绑定邮箱',
            'submit_text': '绑定',
            'back_url': request.GET.get('from', reverse('index')),
        }
    return render(request, 'bind_email.html', context=context)

def send_verification_mail(request):
    email = request.GET.get('email', '')
    send_code_for = request.GET.get('send_code_for', '')
    data = {}
    if email != '':
        #string.ascii_letters所有大小写字母，string.digits所有数字
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data['status'] = 'ERROR'
        else:
            request.session[send_code_for] = code
            request.session['send_code_time'] = now
            send_mail(
                '邮箱绑定',
                '验证码：%s' % code,
                '1214500255@qq.com',
                [email],
                fail_silently=False,
            )
            data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)