from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from django.urls import reverse
from realing_quantity.models import ReadNumExtendMethod, ReadDetail

class Blogtype(models.Model):
    typename = models.CharField(max_length=15)

    def __str__(self):
        return self.typename

class Blog(models.Model, ReadNumExtendMethod):
    title = models.CharField(max_length=30)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    blogtype = models.ForeignKey(Blogtype, on_delete=models.CASCADE)
    content = RichTextUploadingField()

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<标题: %s>" % self.title

    class Meta:
        ordering = ['-create_time']

'''
    def get_read_num(self):
        try:
            return self.readnum.read_num
        except exceptions.ObjectDoesNotExist as e:
            return 0
'''




'''
class ReadNum(models.Model):
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
    read_num = models.IntegerField(default=0)

    def __str__(self):
        return "<博文: %s, 阅读数: %s>" % (self.blog_id, self.read_num)
'''
