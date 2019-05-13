from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Blogtype
# from comment.models import Comment
from django.db.models import Count
from realing_quantity.utils import realing_quantity_auto_add
# from comment.forms import Commentform

# Create your views here.

# -----------------------------------------------获取传递给前端的所有数据--------------------------------------------------
def get_blogs(request, blogs_all, ):
    dates = Blog.objects.dates('create_time', 'day', order='DESC')
    blog_time_counts = {}
    for date in dates:
        blog_time_count = Blog.objects.filter(create_time__year=date.year, create_time__month=date.month, create_time__day=date.day).count()
        blog_time_counts[date] = blog_time_count

    # 对所有的博文对象进行每5篇分页
    paginator = Paginator(blogs_all, 7)
    # 从前台页面获取需要的页数
    page_num = request.GET.get('page_num')
    # 获取前台需要的页面的博文对象
    blogs = paginator.get_page(page_num)
    # 获取所有的分类对象以及获取某个分类的博文数量
    blogtypes = Blogtype.objects.all().annotate(blog_count=Count('blog'))
    # 获取当前所在页面
    current_page = blogs.number
    # 确定分页栏的显示范围,页面最小值为1
    page_range = list(range(max(current_page - 2, 1), current_page)) + list(
        range(current_page, min(current_page + 2, paginator.num_pages) + 1))

    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {
        'dates': dates,
        'paginator': paginator,
        'page_num': page_num,
        'blogs': blogs,
        'blogtypes': blogtypes,
        'current_page': current_page,
        'page_range': page_range,
        'blog_time_counts': blog_time_counts
    }

    return context

# ---------------------------------------------------博文列表处理方法-----------------------------------------------------
def blog_list(request):
    blogs_all = Blog.objects.all()
    context = get_blogs(request, blogs_all)

    return render(request, 'blog_list.html', context=context)


# ---------------------------------------------------博文详情处理方法-----------------------------------------------------
def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, id=blog_pk)
    # 阅读数统计， 自定义阅读数增长规则， 判断cookie是否存在， 只有该cookie不存在时才增加一次阅读数
    get_cookie = realing_quantity_auto_add(request, blog)

    blog_next = Blog.objects.filter(create_time__lt=blog.create_time).first()
    blog_previous = Blog.objects.filter(create_time__gt=blog.create_time).last()

    # blog_content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog_pk, parent_comment=None)
    '''comment_form初始化的数据'''
    # comment_form = Commentform(initial={
    #     'content_type': blog_content_type.model,
    #     'object_id': blog_pk,
    #     'reply_comment_id': 0,
    # })

    context = {
        'blog': blog,
        'blog_previous': blog_previous,
        'blog_next': blog_next,
        # 'comments': comments.order_by('-comment_time'),
        # 'comment_form': comment_form,
    }
    response = render(request, 'blog_detail.html', context=context)
    response.set_cookie(get_cookie, 'true')

    return response


# ---------------------------------------------------博文分类处理方法-----------------------------------------------------
def blog_type(request, blogtype_id):
    blogs_all = Blog.objects.filter(blogtype_id=blogtype_id)
    gettype = Blogtype.objects.get(id=blogtype_id)
    context = get_blogs(request, blogs_all)
    context['gettype'] = gettype

    return render(request, 'blog_type.html', context=context)


# -------------------------------------------------博文时间归档处理方法---------------------------------------------------
def blog_times(request, blog_year, blog_month, blog_day):
    blogs_all = Blog.objects.filter(create_time__year=blog_year, create_time__month=blog_month, create_time__day=blog_day)
    context = get_blogs(request, blogs_all)
    context['blog_year'] = blog_year
    context['blog_month'] = blog_month
    context['blog_day'] = blog_day

    return render(request, 'blog_times.html', context=context)

