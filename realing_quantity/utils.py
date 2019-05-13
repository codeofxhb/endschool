import datetime
from .models import ReadNum, ReadDetail
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum


def realing_quantity_auto_add(request, object):
    '''获取ReadNum关联的模型，即Blog模型'''
    content_model = ContentType.objects.get_for_model(object)
    key = '%s_%s_read' % (content_model.model, object.pk)
    if not request.COOKIES.get(key):
        '''判断访问的博文是否已经存在阅读计数对象'''
        if ReadNum.objects.filter(content_type=content_model, object_id=object.pk).count():
            # 如果存在获取该计数对象，以便添加计数
            readnum = ReadNum.objects.get(content_type=content_model, object_id=object.pk)
        else:
            # 如果不存在则创建阅读计数对象
            readnum = ReadNum(content_type=content_model, object_id=object.pk)
        # 不管是否存在对应的计数对象，只要被访问，都进行计数
        readnum.read_num += 1
        readnum.save()

        date = timezone.now().date()
        '''判断ReadDetail模型中是否有存在该对象的日阅读量统计, created: 判断该对象是获取的还是创建的， False or True'''
        readDetail, created = ReadDetail.objects.get_or_create(content_type=content_model, object_id=object.pk, date=date)
        '''日阅读量计数'''
        readDetail.read_num += 1
        readDetail.save()
    return key

'''获取一周的阅读数'''
def get_week_read_num(content_type):
    today = timezone.now().date()
    read_nums = []
    dates = []
    # ---
    # read_details = ReadDetail.objects.filter(content_type=content_type, date=today)
    # result = read_details.aggregate(read_num_week_sum=Sum('read_num'))
    # read_nums.append(result['read_num_week_sum'] or 0)
    # ---
    for i in range(6, -1, -1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%m.%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        result = read_details.aggregate(read_num_week_sum=Sum('read_num'))
        read_nums.append(result['read_num_week_sum'] or 0)
    return dates, read_nums

'''今日热门点击'''
def get_today_hot(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num')
    '''切片器[]，[:7]取前7条记录'''
    return read_details[:7]

'''昨日热门点击'''
def get_yesteroday_hot(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num')
    return read_details[:7]
