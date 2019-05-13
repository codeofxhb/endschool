import datetime
from django.utils import timezone
from django.shortcuts import render
from realing_quantity.utils import get_week_read_num, get_today_hot, get_yesteroday_hot
from blog.models import Blog
from django.contrib.contenttypes.models import ContentType
from django.db.models import Sum
from django.core.cache import cache

'''
本周热门点击
'''
def get_week_hot():
    today = timezone.now().date()
    week = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
                .filter(read_details__date__lte=today, read_details__date__gt=week) \
                .values('id', 'title') \
                .annotate(read_num_sum=Sum('read_details__read_num')) \
                .order_by('-read_num_sum')
    return blogs[:7]

def index(request):
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
    return render(request, 'index.html', context=context)

