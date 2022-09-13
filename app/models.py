from django.db import models


# Create your models here.

class GoodsBrand(models.Model):
    """产品品牌"""

    name = models.CharField(max_length=64, verbose_name='品牌')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'tb_goods_brand'
        verbose_name = '产品品牌'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsUnit(models.Model):
    """产品单位"""

    name = models.CharField(max_length=64, verbose_name='名称')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'tb_goods_unit'
        verbose_name = '产品单位'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Goods(models.Model):
    """产品"""
    brand = models.ForeignKey('GoodsBrand', on_delete=models.DO_NOTHING, null=True,
                              related_name='goods_set', verbose_name='产品品牌')
    serial_number = models.CharField(max_length=32, verbose_name='序列号')
    model = models.CharField(max_length=32, verbose_name='型号')
    specifications = models.CharField(max_length=32, verbose_name='规格')
    price = models.FloatField(default=0, verbose_name='单价')
    unit = models.ForeignKey('GoodsUnit', on_delete=models.DO_NOTHING, null=True,
                             related_name='goods_set', verbose_name='产品单位')

    class Meta:
        db_table = 'tb_goods'
        verbose_name = '产品'
        verbose_name_plural = verbose_name


class GoodsBalance(models.Model):
    """库存余额"""

    goods = models.ForeignKey('Goods', on_delete=models.CASCADE, related_name='goodbalances', verbose_name='产品')
    initial_quantity = models.FloatField(default=0, verbose_name='期初数量')
    warehousing_quantity = models.FloatField(default=0, verbose_name='入库数量')
    delivery_quantity = models.FloatField(default=0, verbose_name='出库数量')
    total_quantity = models.FloatField(default=0, verbose_name='可用数量')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='备注')

    class Meta:
        db_table = 'tb_goods_balance'
        verbose_name = '库存余额'
        verbose_name_plural = verbose_name


class CashBalance(models.Model):
    """现金余额"""
    data = models.DateField(verbose_name='时间', default='2022-09-02')
    entry_name = models.CharField(max_length=32, default="营业收入", verbose_name='项目')
    opening_balance = models.FloatField(max_length=32, verbose_name='期初余额')
    debit_amount = models.FloatField(max_length=32, verbose_name='借方发生额')
    credit_amount = models.FloatField(max_length=32, verbose_name='贷方发生额')
    cumulative = models.FloatField(max_length=32, verbose_name='累计')

    class Meta:
        db_table = 'tb_cash_balance'
        verbose_name = '现金余额'
        verbose_name_plural = verbose_name


class Receipt(models.Model):
    """小票"""

    number = models.CharField(max_length=32, verbose_name='小票编号')
    customerName = models.CharField(max_length=32, null=True, verbose_name='客户名称')
    handle_time = models.DateField(verbose_name='处理时间')
    payee = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='sales1_orders',
                              verbose_name='收款人')
    consignor = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, blank=True,
                                  related_name='sales2_orders', verbose_name='发货人')
    drawer = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='sales3_orders',
                               verbose_name="下单人")
    state = models.CharField(max_length=32, default="未付款未发货", verbose_name='小票状态')
    total_amount = models.FloatField(null=True, verbose_name='销售总金额')

    class Meta:
        db_table = 'tb_receipt'
        verbose_name = '小票'
        verbose_name_plural = verbose_name


class ReceiptDetails(models.Model):
    """小票明细"""

    sales_order = models.ForeignKey('Receipt', on_delete=models.CASCADE,
                                    related_name='sales_goods_set', verbose_name='小票')
    goods = models.ForeignKey('Goods', on_delete=models.DO_NOTHING, related_name='sales_goods_set', verbose_name='产品')
    sales_quantity = models.FloatField(verbose_name='销售数量')
    total_amount = models.FloatField(verbose_name='总金额')

    class Meta:
        db_table = 'tb_receipt_details'
        verbose_name = '小票明细'
        verbose_name_plural = verbose_name


class User(models.Model):
    """用户"""

    Part_CHOICES = (
        ("man", "男"),
        ('woman', '女')

    )

    Roles_CHOICES = (
        ("sale", "销售"),
        ("cashier", "出纳"),
        ("goodsmanager", "库管")

    )

    username = models.CharField(max_length=32, verbose_name='用户名')
    password = models.CharField(max_length=256, verbose_name='密码')
    name = models.CharField(max_length=64, verbose_name='名称')
    phone = models.CharField(max_length=32, null=True, blank=True, verbose_name='手机号')
    email = models.CharField(max_length=256, null=True, blank=True, verbose_name='邮箱')
    sex = models.CharField(max_length=32, choices=Part_CHOICES, verbose_name='性别')
    roles = models.CharField(max_length=32, choices=Roles_CHOICES, verbose_name='角色')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        db_table = 'tb_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name


class CashCount(models.Model):
    """现金盘点"""

    numbers = models.CharField(max_length=32, verbose_name='现金盘点编号')
    date = models.DateField(verbose_name='处理时间')
    operator = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='cash_count',
                                 verbose_name='处理人')
    book_cash = models.FloatField(max_length=32, verbose_name='账面现金')
    actual_cash = models.FloatField(max_length=32, verbose_name='实有现金')
    Profit_loss = models.FloatField(max_length=32, verbose_name='盈亏')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='盈亏说明')

    class Meta:
        db_table = 'tb_cash_count'
        verbose_name = '现金盘点'
        verbose_name_plural = verbose_name


class GoodsCount(models.Model):
    """货物盘点"""

    numbers = models.CharField(max_length=32, verbose_name='货物盘点编号')
    date = models.DateField(verbose_name='处理时间')
    operator = models.ForeignKey('User', on_delete=models.DO_NOTHING, null=True, blank=True, related_name='goods_count',
                                 verbose_name='处理人')

    class Meta:
        db_table = 'tb_goods_count'
        verbose_name = '货物盘点'
        verbose_name_plural = verbose_name


class GoodsCountDetials(models.Model):
    good_count = models.ForeignKey('GoodsCount', on_delete=models.CASCADE,
                                   related_name='good_count_set', verbose_name='货物盘点明细')
    goods = models.ForeignKey('Goods', on_delete=models.DO_NOTHING, related_name='goods_count', verbose_name='产品')
    book_goods = models.FloatField(max_length=32, verbose_name='账面数量')
    actual_goods = models.FloatField(max_length=32, verbose_name='实有数量')
    Profit_loss = models.FloatField(max_length=32, verbose_name='盈亏')
    remark = models.CharField(max_length=256, null=True, blank=True, verbose_name='盈亏说明')
