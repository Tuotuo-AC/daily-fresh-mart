from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from .forms import RegisterForm, LoginForm, ProfileForm, AddressForm
from .models import Profile, Address, EmailVerifyRecord, generate_verification_code

# ---------- 发送验证码视图 ----------
def send_verify_code(request, email=None, send_type='register'):
    """发送邮箱验证码（API视图）

    Args:
        request: HTTP请求对象
        email: 直接传入的邮箱（可选）
        send_type: 'register' 或 'forget'
    """
    if email is None:
        email = request.GET.get('email', '').strip()

    if not email:
        return JsonResponse({'status': 'error', 'msg': '邮箱不能为空'})

    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, email):
        return JsonResponse({'status': 'error', 'msg': '邮箱格式不正确'})

    # 根据类型判断是否检查邮箱已注册
    if send_type == 'register':
        if User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'msg': '该邮箱已被注册'})
    elif send_type == 'forget':
        if not User.objects.filter(email=email).exists():
            return JsonResponse({'status': 'error', 'msg': '该邮箱未注册'})

    # 生成并发送验证码
    success, msg = _generate_and_send_code(email, send_type)

    if success:
        return JsonResponse({'status': 'success', 'msg': msg})
    else:
        return JsonResponse({'status': 'error', 'msg': msg})


def _generate_and_send_code(email, send_type='register'):
    """生成验证码并发送（内部函数）"""
    # 删除该邮箱之前的验证码
    EmailVerifyRecord.objects.filter(email=email).delete()

    # 生成6位验证码
    code = generate_verification_code(6)

    # 保存验证码（10分钟有效）
    EmailVerifyRecord.objects.create(
        email=email,
        code=code,
        expire_time=timezone.now() + timedelta(minutes=10)
    )

    # 根据类型设置不同的邮件主题
    if send_type == 'register':
        subject = '天天生鲜 - 注册验证码'
        message = f'您的注册验证码是：{code}\n请在10分钟内完成注册。\n\n如果这不是您的操作，请忽略此邮件。'
    else:
        subject = '天天生鲜 - 找回密码验证码'
        message = f'您正在找回密码，验证码是：{code}\n请在10分钟内完成操作。\n\n如果这不是您的操作，请忽略此邮件。'

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
        print(f"\n{'='*50}")
        print(f"📧 邮件已发送到: {email}")
        print(f"🔑 验证码是: {code}")
        print(f"{'='*50}\n")
        return True, '验证码已发送到邮箱'
    except Exception as e:
        print(f"\n{'='*50}")
        print(f"📧 邮件发送失败，但验证码仍可用: {email}")
        print(f"🔑 验证码是: {code}")
        print(f"❌ 错误: {e}")
        print(f"{'='*50}\n")
        return True, '验证码已生成（邮件发送失败，请查看控制台）'


# ---------- 注册视图 ----------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            verify_code = cd.get('verify_code', '').strip()

            # 验证验证码
            if not verify_code:
                return render(request, 'user/register.html', {
                    'form': form,
                    'error': '请输入验证码'
                })

            email = cd['email']
            verify_record = EmailVerifyRecord.objects.filter(
                email=email,
                code=verify_code
            ).order_by('-created_time').first()

            if not verify_record:
                return render(request, 'user/register.html', {
                    'form': form,
                    'error': '验证码错误'
                })

            if not verify_record.is_valid():
                verify_record.delete()
                return render(request, 'user/register.html', {
                    'form': form,
                    'error': '验证码已过期，请重新获取'
                })

            # 验证码正确，创建用户
            user = User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password']
            )

            Profile.objects.create(
                user=user,
                mobile=cd['mobile'],
                email_active=True
            )

            # 删除已使用的验证码
            verify_record.delete()

            return render(request, 'user/register_success.html', {'email': user.email})
    else:
        form = RegisterForm()
    return render(request, 'user/register.html', {'form': form})

# ---------- 激活视图 ----------
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user and default_token_generator.check_token(user, token):
        user.profile.email_active = True
        user.profile.save()
        return render(request, 'user/activation_success.html')
    else:
        return render(request, 'user/activation_failed.html')

# ---------- 登录视图 ----------
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # 支持用户名、邮箱、手机号登录
            user = None
            if '@' in username:
                try:
                    user_obj = User.objects.get(email=username)
                    user = authenticate(username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            elif username.isdigit():
                try:
                    profile = Profile.objects.get(mobile=username)
                    user = authenticate(username=profile.user.username, password=password)
                except Profile.DoesNotExist:
                    pass
            else:
                user = authenticate(username=username, password=password)

            if user:
                if user.profile.email_active:
                    login(request, user)
                    next_url = request.GET.get('next', reverse('index'))  # 假设你有个 'index' 路由
                    return redirect(next_url)
                else:
                    return render(request, 'user/login.html', {'form': form, 'error': '邮箱未激活，请先激活'})
            else:
                return render(request, 'user/login.html', {'form': form, 'error': '用户名或密码错误'})
    else:
        form = LoginForm()
    return render(request, 'user/login.html', {'form': form})

# ---------- 登出视图 ----------
def user_logout(request):
    logout(request)
    return redirect('index')   # 返回首页，请确保有 'index' 路由

# ---------- 忘记密码 ----------
def forget_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if not email:
            return render(request, 'user/forget_password.html', {'error': '请输入邮箱'})

        try:
            user = Profile.objects.get(user__email=email)
        except Profile.DoesNotExist:
            return render(request, 'user/forget_password.html', {'error': '该邮箱未注册'})

        _generate_and_send_code(email, send_type='forget')
        return render(request, 'user/forget_password.html', {'success': True, 'email': email})

    return render(request, 'user/forget_password.html')

# ---------- 重置密码 ----------
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        verify_code = request.POST.get('verify_code', '').strip()
        password = request.POST.get('password', '').strip()
        password_confirm = request.POST.get('password_confirm', '').strip()

        if not all([email, verify_code, password, password_confirm]):
            return render(request, 'user/reset_password.html', {'error': '请填写所有字段', 'email': email})

        if password != password_confirm:
            return render(request, 'user/reset_password.html', {'error': '两次密码输入不一致', 'email': email})

        if len(password) < 6:
            return render(request, 'user/reset_password.html', {'error': '密码长度不能少于6位', 'email': email})

        try:
            verify_record = EmailVerifyRecord.objects.filter(
                email=email,
                code=verify_code,
                expire_time__gt=timezone.now()
            ).order_by('-created_time').first()

            if not verify_record:
                return render(request, 'user/reset_password.html', {'error': '验证码已过期，请重新获取', 'email': email})

            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()

            verify_record.delete()

            return render(request, 'user/reset_password_success.html')

        except User.DoesNotExist:
            return render(request, 'user/reset_password.html', {'error': '用户不存在', 'email': email})

    email = request.GET.get('email', '')
    return render(request, 'user/reset_password.html', {'email': email})

# ---------- 个人中心 ----------
@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('user:profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'user/profile.html', {'form': form})

# ---------- 地址列表 ----------
@login_required
def address_list(request):
    addresses = request.user.addresses.all()
    return render(request, 'user/address_list.html', {'addresses': addresses})

# ---------- 新增地址 ----------
@login_required
def address_add(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            if not request.user.addresses.exists():
                addr.is_default = True
            addr.save()
            return redirect('user:address_list')
    else:
        form = AddressForm()
    return render(request, 'user/address_form.html', {'form': form, 'title': '新增地址'})

# ---------- 编辑地址 ----------
@login_required
def address_edit(request, pk):
    addr = request.user.addresses.get(pk=pk)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=addr)
        if form.is_valid():
            form.save()
            return redirect('user:address_list')
    else:
        form = AddressForm(instance=addr)
    return render(request, 'user/address_form.html', {'form': form, 'title': '编辑地址'})

# ---------- 删除地址 ----------
@login_required
def address_delete(request, pk):
    addr = request.user.addresses.get(pk=pk)
    addr.delete()
    return redirect('user:address_list')

# ---------- 设为默认地址 ----------
@login_required
def set_default_address(request, pk):
    request.user.addresses.update(is_default=False)
    addr = request.user.addresses.get(pk=pk)
    addr.is_default = True
    addr.save()
    return redirect('user:address_list')