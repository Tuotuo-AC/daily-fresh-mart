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
from .forms import RegisterForm, LoginForm, ProfileForm, AddressForm
from .models import Profile, Address

# ---------- 注册视图 ----------
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # 创建 User 对象
            user = User.objects.create_user(
                username=cd['username'],
                email=cd['email'],
                password=cd['password']
            )
            # 创建对应的 Profile
            profile = Profile.objects.create(
                user=user,
                mobile=cd['mobile'],
                email_active=False
            )
            # 发送激活邮件
            current_site = get_current_site(request)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            activation_link = f'http://{current_site.domain}/user/activate/{uid}/{token}/'
            subject = '天天生鲜 - 激活您的账户'
            message = f'请点击以下链接激活账户：\n{activation_link}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            return render(request, 'user/register_done.html', {'email': user.email})
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