from django.db import models

# Create your models here.
from django.db import models

# 商品分类表
# 模型类 对应了一张表
class GoodsCategory(models.Model):
    # 分类的名称 max_length 最大长度，字符串类型必须定义
    cag_name = models.CharField(max_length=30)
    # 分类的样式
    cag_css = models.CharField(max_length=20)
    # 分类的图片
    cag_img = models.ImageField(upload_to='cag')

# 商品表
# 模型类
class GoodsInfo(models.Model):
    # 商品名字
    goods_name = models.CharField(max_length=100)
    # 商品的价格
    goods_price = models.IntegerField(default=0)
    # 商品的描述
    goods_desc = models.CharField(max_length=2000)
    # 商品图片
    goods_img = models.ImageField(upload_to='goods')
    # 所属的分类
    goods_cag = models.ForeignKey('GoodsCategory', on_delete=models.CASCADE)


