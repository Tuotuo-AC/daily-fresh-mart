from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import Profile, Address

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150, label='用户名')
    email = forms.EmailField(label='邮箱')
    mobile = forms.CharField(
        max_length=11,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入有效的手机号')],
        label='手机号'
    )
    password = forms.CharField(widget=forms.PasswordInput, label='密码')
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='确认密码')
    verify_code = forms.CharField(max_length=6, label='验证码', required=False)

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('用户名已存在')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('邮箱已被注册')
        return email

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if Profile.objects.filter(mobile=mobile).exists():
            raise forms.ValidationError('手机号已被注册')
        return mobile

    def clean(self):
        cleaned_data = super().clean()
        pwd = cleaned_data.get('password')
        pwd2 = cleaned_data.get('password_confirm')
        if pwd and pwd2 and pwd != pwd2:
            raise forms.ValidationError('两次输入密码不一致')
        return cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(label='用户名/邮箱/手机号')
    password = forms.CharField(widget=forms.PasswordInput, label='密码')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'mobile', 'gender', 'birthday']
        labels = {
            'nickname': '昵称',
            'mobile': '手机号',
            'gender': '性别',
            'birthday': '生日',
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['user', 'created_time']
        labels = {
            'receiver': '收货人',
            'mobile': '手机号',
            'province': '省',
            'city': '市',
            'district': '区',
            'detail': '详细地址',
            'is_default': '设为默认地址',
        }