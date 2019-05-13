from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class Loginform(forms.Form):
    username_or_email = forms.CharField(label='用户名或邮箱', required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名'}))
    password = forms.CharField(label='密码', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))

    '''验证数据，验证或者清理提交的数据'''
    def clean(self):
        username_or_email = self.cleaned_data['username_or_email']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username_or_email, password=password)

        if user is None:
            if User.objects.filter(email=username_or_email).exists():
                username = User.objects.get(email=username_or_email).username
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    self.cleaned_data['user'] = user
                    return self.cleaned_data
            raise forms.ValidationError('用户名或者密码不正确')
        else:
            self.cleaned_data['user'] = user
        return self.cleaned_data

class Regform(forms.Form):
    username = forms.CharField(label='用户名', max_length=10, min_length=3, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入用户名（3-10个字符）'}))
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入注册邮箱'}))
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': '请填写收到的验证码完成注册'}))
    password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入密码'}))
    password_again = forms.CharField(label='确认密码', min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '确认密码'}))
    '''验证各个数据'''

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(Regform, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已注册')
        return email

    def clean_password_again(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError('密码不一致')
        return password_again

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

    def clean(self):
        code = self.request.session.get('register_account_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

class ChangeNinameform(forms.Form):
    niname_new = forms.CharField(label='新的昵称', max_length=20, widget=forms.TextInput({'class': 'form-control', 'placeholder': '请输入新的昵称'}))
    
    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangeNinameform, self).__init__(*args, **kwargs)

    def clean(self):
        if self.user.is_authenticated:
            self.cleaned_data['user'] = self.user
        else:
            raise forms.ValidationError('用户尚未登录！')
        return self.cleaned_data

    def clean_niname_new(self):
        niname_new = self.cleaned_data.get('niname_new', '').strip()
        if niname_new == '':
            raise forms.ValidationError('新的昵称不能为空')
        return niname_new

class BindEmailForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入正确的邮箱'}))
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '点击发送验证码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(BindEmailForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request.user.is_authenticated:
            self.cleaned_data['user'] = self.request.user
        else:
            raise forms.ValidationError('用户尚未登录！')

        # if self.request.user.email != '':
        #     raise forms.ValidationError('该用户已绑定邮箱')

        code = self.request.session.get('bind_email_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')

        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('该邮箱已被绑定')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        return verification_code

class FindPasswordForm(forms.Form):
    email = forms.EmailField(label='邮箱', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '请输入注册账号的邮箱'}))
    verification_code = forms.CharField(label='验证码', required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请填写收到的验证码完成验证'}))
    new_password = forms.CharField(label='密码', min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新密码'}))

    def __init__(self, *args, **kwargs):
        if 'request' in kwargs:
            self.request = kwargs.pop('request')
        super(FindPasswordForm, self).__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('该用户不存在')
        return email

    def clean_verification_code(self):
        verification_code = self.cleaned_data.get('verification_code', '').strip()
        if verification_code == '':
            raise forms.ValidationError('验证码不能为空')
        code = self.request.session.get('find_password_code', '')
        verification_code = self.cleaned_data.get('verification_code', '')
        if not (code != '' and code == verification_code):
            raise forms.ValidationError('验证码不正确')
        return verification_code

class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(label='原密码', min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入原密码'}))
    new_password = forms.CharField(label='新密码', min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请输入新密码'}))
    confirm_password = forms.CharField(label='确认密码', min_length=6, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请确认新密码'}))

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

    def clean(self):
        new_password = self.cleaned_data.get('new_password', '')
        confirm_password = self.cleaned_data.get('confirm_password', '')
        if new_password != confirm_password or new_password == '':
            raise forms.ValidationError('两次输入的密码不一致')
        return self.cleaned_data

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password', '')
        if not self.user.check_password(old_password):
            raise forms.ValidationError('密码错误')
        return old_password