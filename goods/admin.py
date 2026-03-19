from django.contrib import admin

# Register your models here.
from goods.models import GoodsInfo

class GoodsInfoAdmin(admin.ModelAdmin):
    # 需要显示的字段
    list_display = ['id','goods_name','goods_price','goods_desc']
    # 每页显示的数量
    list_per_page = 10
    actions_on_top = False
    actions_on_bottom = True
    # 在界面上显示搜索，列表里是搜索依赖的字段
    search_fields = ['id','goods_name']

admin.site.register(GoodsInfo,GoodsInfoAdmin)