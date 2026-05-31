from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import random
import string


def generate_verification_code(length=6):
    """生成随机验证码"""
    return ''.join(random.choices(string.digits, k=length))


class EmailVerifyRecord(models.Model):
    """邮箱验证码"""
    email = models.EmailField(verbose_name='邮箱')
    code = models.CharField(max_length=6, verbose_name='验证码')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    expire_time = models.DateTimeField(verbose_name='过期时间')

    class Meta:
        db_table = 'email_verify_record'
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.email} - {self.code}'

    def is_valid(self):
        from django.utils import timezone
        return timezone.now() < self.expire_time


# 这里没有自定义 User，只有 Profile 和 Address。Profile 与 User 是一对一关系。
# 额外创建 Profile 模型存储手机号、邮箱激活状态、昵称等信息。这样不会产生任何数据库冲突，原有商品数据完全不受影响
class Profile(models.Model):
    GENDER_CHOICES = [
        ('保密', '保密'),
        ('男', '男'),
        ('女', '女'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    mobile = models.CharField(
        max_length=11,
        unique=True,
        validators=[RegexValidator(r'^1[3-9]\d{9}$', '请输入有效的手机号')],
        blank=True,
        null=True,
        verbose_name='手机号'
    )
    email_active = models.BooleanField(default=False, verbose_name='邮箱是否激活')
    nickname = models.CharField(max_length=30, blank=True, verbose_name='昵称')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='保密', verbose_name='性别')
    birthday = models.DateField(null=True, blank=True, verbose_name='生日')

    class Meta:
        db_table = 'user_profile'
        verbose_name = '用户扩展信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.username


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='所属用户')
    receiver = models.CharField(max_length=30, verbose_name='收货人')
    mobile = models.CharField(max_length=11, verbose_name='手机号')
    province = models.CharField(max_length=50, verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    district = models.CharField(max_length=50, verbose_name='区')
    detail = models.CharField(max_length=100, verbose_name='详细地址')
    is_default = models.BooleanField(default=False, verbose_name='默认地址')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'address'
        verbose_name = '收货地址'
        verbose_name_plural = verbose_name
        ordering = ['-is_default', '-created_time']

    def __str__(self):
        return f'{self.receiver} - {self.mobile}'

    def get_full_address(self):
        return f'{self.province}{self.city}{self.district}{self.detail}'