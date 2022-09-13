from django.contrib import admin

# Register your models here.
from app import models


class goodsadmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'specifications', 'serial_number')
    search_fields = ('brand__name', 'model')


# class saleadmin(admin.ModelAdmin):
#     style_display = {'goods', 'checkbox_inline'}
#     filter_horizontal = ['goods']


admin.site.register(models.GoodsUnit)
admin.site.register(models.GoodsBrand)
admin.site.register(models.Goods, goodsadmin)
admin.site.register(models.CashBalance)
admin.site.register(models.GoodsBalance)
admin.site.register(models.User)
admin.site.register(models.Receipt)
admin.site.register(models.ReceiptDetails)
admin.site.register(models.CashCount)
admin.site.register(models.GoodsCount)
