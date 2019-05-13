from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Blog, Blogtype

# Create your views here.

def get_blogs(request, blogs_all, ):
    dates = Blog.objects.dates('create_time', 'day', order='DESC')
    # 对所有的博文对象进行每5篇分页
    paginator = Paginator(blogs_all, 3)
    # 从前台页面获取需要的页数
    page_num = request.GET.get('page_num')
    # 获取前台需要的页面的博文对象
    blogs = paginator.get_page(page_num)
    # 获取所有的分类对象
    blogtypes = Blogtype.objects.all()
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
    }
    return context

def blog_list(request):
    # 后去所有的博文对象
    blogs_all = Blog.objects.all()
    context = get_blogs(request, blogs_all)

    return render(request, 'templates/blog_list.html', context=context)

def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, id=blog_pk)

    blog_next = Blog.objects.filter(create_time__lt=blog.create_time).first()
    blog_previous = Blog.objects.filter(create_time__gt=blog.create_time).last()

    context = {
        'blog': blog,
        'blog_previous': blog_previous,
        'blog_next': blog_next,
    }
    return render(request, 'templates/blog_detail.html', context=context)

def blog_type(request, blogtype_id):
    dates = Blog.objects.dates('create_time', 'day', order='DESC')
    blogs_all = Blog.objects.filter(blogtype_id=blogtype_id)
    paginator = Paginator(blogs_all, 3)
    page_num = request.GET.get('page_num', 1)
    blogs = paginator.get_page(page_num)

    gettype = Blogtype.objects.get(id=blogtype_id)
    blogtypes = Blogtype.objects.all()
    current_page = blogs.number
    # 确定分页栏的显示范围,页面最小值为1
    page_range = list(range(max(current_page - 2, 1), current_page)) + list(
        range(current_page, min(current_page + 2, paginator.num_pages) + 1))
    if page_range[0]-1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 返回给页面的参数内容
    context = {
        'blogs': blogs,
        'paginator': paginator,
        'page_num': page_num,
        'gettype': gettype,
        'blogtypes': blogtypes,
        'current_page': current_page,
        'page_range': page_range,
        'dates': dates,
    }
    return render(request, 'templates/blog_type.html', context=context)

def blog_times(request, blog_year, blog_month, blog_day):
    blogs_all = Blog.objects.filter(create_time__year=blog_year, create_time__month=blog_month, create_time__day=blog_day)
    dates = Blog.objects.dates('create_time', 'day', order='DESC')
    page_num = request.GET.get('page_num', 1)
    paginator = Paginator(blogs_all, 3)
    blogs = paginator.get_page(page_num)
    blogtypes = Blogtype.objects.all()
    current_page = blogs.number
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
        'blog_year': blog_year,
        'blog_month': blog_month,
        'blog_day': blog_day,
        'dates': dates,
        'page_num': page_num,
        'paginator': paginator,
        'blogs': blogs,
        'blogtypes': blogtypes,
        'page_range': page_range,
    }

    return render(request, 'templates/blog_times.html', context=context)

