from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="用户名")
    niname = models.CharField(max_length=20)

    def __str__(self):
        return '<Profile: %s for %s>' % (self.niname, self.user.username)

def get_niname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.niname
    else:
        return ''

def get_niname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.niname
    else:
        return self.username

def has_niname(self):
    return Profile.objects.filter(user=self).exists()

User.get_niname = get_niname
User.has_niname = has_niname
User.get_niname_or_username = get_niname_or_username