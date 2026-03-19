from django.urls import path
from . import views  # 从当前应用导入视图

urlpatterns = [
    # 主页
    path('index/', views.index, name='index'),  # 这里定义index/路径的处理
    path('detail/', views.detail, name='detail'), # 详情页
    path('goods/', views.goods, name='goods'),
    path('testcsrf/', views.testcsrf, name='testcsrf'),
    # path('test_filter/', views.test_filter, name='test_filter'),
    path('test/', views.test, name='test'),
]