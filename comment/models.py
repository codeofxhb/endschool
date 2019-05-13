import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

class SendMail(threading.Thread):
    def __init__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            '',
            settings.EMAIL_HOST_USER,
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )

class Comment(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = RichTextUploadingField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)

    '''用于记录该条评论是回复那一条平评论，评论谁的。'''
    root_comment = models.ForeignKey('self', related_name='root_comments', null=True, on_delete=models.CASCADE)
    parent_comment = models.ForeignKey('self', related_name='parent_comments', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name='replies', null=True, on_delete=models.CASCADE)

    def send_email_for_comments_or_reply(self):
        """发送邮件通知"""
        context = {}
        if self.parent_comment is None:
            '''没有父评论，即代表当前评论为根评论'''
            email = self.content_object.get_email()
        else:
            '''存在父评论，代表有人回复你的评论'''
            email = self.reply_to.email
        if email != '':
            subject = '评论通知'
            # text = '%s\n<a href="%s">%s</a>' % (self.text, self.content_object.get_url(), "前往点击")
            context['comment_text'] = self.text
            context['url'] = self.content_object.get_url()
            text = render_to_string('comment/send_mail.html', context=context)
            send_mail_for_comments_or_reply = SendMail(subject, text, email)
            send_mail_for_comments_or_reply.start()

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']