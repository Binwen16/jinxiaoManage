from django.db import transaction
from number_precision import NP
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField

from app.models import *


class GoodsBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsBrand
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]


class GoodsUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = GoodsUnit
        read_only_fields = ['id']
        fields = ['name', 'remark', *read_only_fields]


class GoodsSerializer(serializers.ModelSerializer):
    class GoodsBalanceSerializer(serializers.ModelSerializer):
        class Meta:
            model = GoodsBalance
            read_only_fields = ['id']
            fields = ['total_quantity', 'delivery_quantity', 'warehousing_quantity', 'initial_quantity',
                      *read_only_fields]

    brand_name = CharField(source='brand.name', read_only=True, label='品牌')
    unit_name = CharField(source='unit.name', read_only=True, label='单位')

    class Meta:
        model = Goods
        read_only_fields = ['id', 'brand', 'unit', 'brand_name','unit_name']
        fields = ['brand', 'serial_number', 'model', 'specifications', 'price', 'unit', *read_only_fields]


class GoodsBalanceSerializer(serializers.ModelSerializer):
    good_brand = CharField(source='goods.brand.name', read_only=True, label='品牌')
    good_serial_number = CharField(source='goods.serial_number', read_only=True, label='系列号')
    good_model = CharField(source='goods.model', read_only=True, label='型号')
    good_specifications = CharField(source='goods.specifications', read_only=True, label='规格')
    good_price = CharField(source='goods.price', read_only=True, label='价格')
    unit_name = CharField(source='goods.unit.name', read_only=True, label='单位')

    class Meta:
        model = GoodsBalance
        fields = ['id', 'goods', 'good_brand',
                  'good_serial_number', 'good_model', 'good_price', 'good_specifications', 'unit_name',
                  'initial_quantity',
                  'warehousing_quantity', 'delivery_quantity', 'total_quantity']


class CashBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashBalance
        fields = '__all__'


def validate_foreign_key(self, model, instance, message):
    if instance:
        if not (instance := model.objects.filter(id=instance.id).first()):
            raise ValidationError(message)
    return instance


class ReceiptSerializer(serializers.ModelSerializer):
    """小票"""

    class ReceiptDetailsSerializer(serializers.ModelSerializer):
        """小票明细"""

        good_brand = CharField(source='goods.brand.name', read_only=True, label='品牌')
        good_serial_number = CharField(source='goods.serial_number', read_only=True, label='系列号')
        good_model = CharField(source='goods.model', read_only=True, label='型号')
        good_specifications = CharField(source='goods.specifications', read_only=True, label='规格')
        good_price = CharField(source='goods.price', read_only=True, label='价格')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位')

        class Meta:
            model = ReceiptDetails
            read_only_fields = ['id', 'good_brand', 'good_serial_number', 'good_model',
                                'good_specifications', 'good_price', 'unit_name', 'total_amount']
            fields = ['goods', 'sales_quantity', *read_only_fields]

        def validate_goods(self, instance):
            instance = validate_foreign_key(self, Goods, instance, message='产品不存在')
            if not instance:
                raise ValidationError(f'产品[{instance.brand}]未激活')
            return instance

        def validate_sales_quantity(self, value):
            if value <= 0:
                raise ValidationError('销售数量小于或等于零')
            return value

    drawer_name = CharField(source='drawer.name', read_only=True, label='创建人')
    payee_name = CharField(source='payee.name', read_only=True, label='收款人')
    consignor_name = CharField(source='consignor.name', read_only=True, label='发货人')
    sales_goods_items = ReceiptDetailsSerializer(
        source='sales_goods_set', many=True, label='小票明细')

    class Meta:
        model = Receipt
        read_only_fields = ['id', 'drawer_name', 'payee_name', 'consignor_name', 'total_amount']
        fields = ['number', 'drawer', 'drawer_name', 'consignor', 'payee', 'handle_time', 'customerName',
                  'state', 'sales_goods_items','consignor', *read_only_fields]

    def validate_state(self, value):
        if value != '未付款未发货' and value != '已收款' and value != '已发货':
            raise ValidationError('小票state错误')
        return value

    def validate_payee(self, value):
        return value

    def validate_consignor(self, value):
        return value

    @transaction.atomic
    def create(self, validated_data):
        sales_goods_items = validated_data.pop('sales_goods_set')
        sales_order = super().create(validated_data)
        total_sales_amount = 0
        # 创建小票明细
        sales_goods_set = []
        for sales_goods_item in sales_goods_items:
            sales_quantity = sales_goods_item['sales_quantity']
            # sales_price = sales_goods_item['goods'].id
            sales_price = Goods.objects.filter(id=sales_goods_item['goods'].id).first().price
            total_amount = NP.times(sales_quantity, sales_price)
            sales_goods_set.append(ReceiptDetails(
                sales_order=sales_order, goods=sales_goods_item['goods'], sales_quantity=sales_quantity,
                # sales_price=sales_price,
                total_amount=total_amount
            ))
            total_sales_amount = NP.plus(total_sales_amount, total_amount)
        else:
            ReceiptDetails.objects.bulk_create(sales_goods_set)

            sales_order.total_amount = total_sales_amount

        sales_order.save(update_fields=['total_amount'])
        return sales_order
    # @transaction.atomic
    def update(self, instance, validated_data):

        state = validated_data.get('state')
        payee = validated_data.get('payee')
        consignor = validated_data.get('consignor')
        print(validated_data)

        if state is not None and instance.state != state:
            instance.state = validated_data['state']
            validated_data['state'] = state

        if payee is not None and instance.payee != payee:
            instance.payee = validated_data['payee']
            validated_data['payee'] = payee

        if consignor is not None and instance.consignor != consignor:
            instance.consignor = validated_data['consignor']
            validated_data['consignor'] = consignor

        return super().update(instance, validated_data)



#
# class GoodsCountSerializer(serializers.ModelSerializer):
#     """货物盘点"""
#     operator = CharField(source='operator.name', read_only=True, label='操作人')
#
#     good_brand = CharField(source='goods.brand.name', read_only=True, label='品牌')
#     good_serial_number = CharField(source='goods.serial_number', read_only=True, label='系列号')
#     good_model = CharField(source='goods.model', read_only=True, label='型号')
#     good_specifications = CharField(source='goods.specifications', read_only=True, label='规格')
#     good_price = CharField(source='goods.price', read_only=True, label='价格')
#     unit_name = CharField(source='goods.unit.name', read_only=True, label='单位')
#
#     class Meta:
#         model = GoodsCount
#         fields = ['__all__']


class UserSerializer(serializers.ModelSerializer):
    """用户"""

    class Meta:
        model = User
        fields = '__all__'


class GoodsCountSerializer(serializers.ModelSerializer):
    """货物盘点"""

    class GoodsCountDetailsSerializer(serializers.ModelSerializer):
        """货物盘点明细明细"""

        good_brand = CharField(source='goods.brand.name', read_only=True, label='品牌')
        good_serial_number = CharField(source='goods.serial_number', read_only=True, label='系列号')
        good_model = CharField(source='goods.model', read_only=True, label='型号')
        good_specifications = CharField(source='goods.specifications', read_only=True, label='规格')
        good_price = CharField(source='goods.price', read_only=True, label='价格')
        unit_name = CharField(source='goods.unit.name', read_only=True, label='单位')

        class Meta:
            model = GoodsCountDetials
            read_only_fields = ['id', 'good_brand', 'good_serial_number', 'good_model',
                                'good_specifications', 'good_price', 'unit_name', 'book_goods', 'Profit_loss', 'remark']
            fields = ['goods', 'actual_goods', *read_only_fields]

        def validate_goods(self, instance):
            instance = validate_foreign_key(self, Goods, instance, message='产品不存在')
            if not instance:
                raise ValidationError(f'产品[{instance.brand}]未激活')
            return instance

        def validate_actual_goods(self, value):
            if value < 0:
                raise ValidationError('数量小于零')
            return value

    operator_name = CharField(source='operator.name', read_only=True, label='创建人')

    good_count_items = GoodsCountDetailsSerializer(
        source='good_count_set', many=True, label='盘点明细')

    class Meta:
        model = GoodsCount
        read_only_fields = ['id', 'operator_name']
        fields = ['numbers', 'operator', 'date', 'good_count_items', *read_only_fields]

    @transaction.atomic
    def create(self, validated_data):
        good_count_items = validated_data.pop('good_count_set')

        good_count = super().create(validated_data)

        book_goods = 0
        actual_goods = 0
        Profit_loss = 0

        # 创建货物盘点明细
        stock_check_goods = []
        for good_count_item in good_count_items:
            goods = good_count_item['goods']

            goodsbalance = GoodsBalance.objects.get(goods=goods)
            book_goods = goodsbalance.total_quantity
            actual_goods = good_count_item['actual_goods']
            Profit_loss = NP.minus(actual_goods, book_goods)

            stock_check_goods.append(GoodsCountDetials(
                good_count=good_count, goods=goods, book_goods=book_goods,
                actual_goods=actual_goods, Profit_loss=Profit_loss)
            )

        else:
            GoodsCountDetials.objects.bulk_create(stock_check_goods)

        return good_count


class CashCountSerializer(serializers.ModelSerializer):
    """现金盘点"""
    operator_name = CharField(source='operator.name', read_only=True, label='操作人')

    class Meta:
        model = CashCount
        read_only_fields = ['id', 'operator_name', 'book_cash', 'Profit_loss', 'remark']
        fields = ['numbers', 'operator', 'date', 'actual_cash', *read_only_fields]

    def create(self, validated_data):
        cash_items = validated_data
        book_cash = CashBalance.objects.order_by("id").last().cumulative or 0
        actual_cash = cash_items['actual_cash']
        operator = cash_items['operator']
        Profit_loss = NP.minus(actual_cash, book_cash)
        validated_data['Profit_loss'] = Profit_loss
        validated_data['book_cash'] = book_cash
        validated_data['operator'] = operator
        return super().create(validated_data)
