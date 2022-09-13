from django.db import transaction
from django.shortcuts import render

# Create your views here.
from number_precision import NP
from rest_framework import status, request
from rest_framework.exceptions import APIException
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import RetrieveModelMixin, ListModelMixin, CreateModelMixin, DestroyModelMixin, \
    UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from app.Pagination import LimitedPagination, InfinitePagination
from app.models import GoodsBrand, GoodsUnit, Goods, GoodsBalance, Receipt, CashBalance, GoodsCount,\
    CashCount, User
from app.serializer import GoodsBrandSerializer, GoodsUnitSerializer, GoodsSerializer, GoodsBalanceSerializer, \
    ReceiptSerializer, CashBalanceSerializer, GoodsCountSerializer, CashCountSerializer, UserSerializer


class ValidationError(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '无效请求'
    default_code = 'invalid'


class GoodsBrandViewSet(ModelViewSet):
    """产品品牌"""

    serializer_class = GoodsBrandSerializer
    # permission_classes = [IsAuthenticated, GoodsCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsBrand.objects.all()


class GoodsUnitViewSet(ModelViewSet):
    """产品单位"""

    serializer_class = GoodsUnitSerializer
    # permission_classes = [IsAuthenticated, GoodsCategoryPermission]
    search_fields = ['name', 'remark']
    ordering_fields = ['id', 'name']
    queryset = GoodsUnit.objects.all()


class GoodsViewSet(ModelViewSet):
    """产品"""

    serializer_class = GoodsSerializer
    # permission_classes = [IsAuthenticated, GoodsPermission]
    filterset_fields = ['number', 'brand']
    search_fields = ['number', 'serial_number', 'remark', 'brand']
    ordering_fields = ['id', 'number']
    ordering = ['id']
    select_related_fields = ['brand', 'unit']
    prefetch_related_fields = ['goodbalances']
    queryset = Goods.objects.all()


from django_filters.rest_framework import DjangoFilterBackend


class GoodBalanceViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin, CreateModelMixin):
    """库存"""

    serializer_class = GoodsBalanceSerializer
    # permission_classes = [IsAuthenticated, InventoryPermission]
    filterset_fields = ['goods']
    search_fields = ['goods__number', 'goods__brand']
    ordering_fields = ['id', 'total_quantity']
    select_related_fields = ['goods', 'goods__unit', 'goods__brand']
    queryset = GoodsBalance.objects.all()

    pagination_class = InfinitePagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['id']
    prefetch_related_fields = []

    @property
    def user(self):
        return self.request.user

    @property
    def context(self):
        return self.get_serializer_context()

    # def get_queryset(self):
    #     queryset = super().get_queryset().filter(team=self.team)
    #     queryset = queryset.select_related(*self.select_related_fields)
    #     queryset = queryset.prefetch_related(*self.prefetch_related_fields)
    #     return queryset


class ReceiptViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin, DestroyModelMixin,
                     UpdateModelMixin):
    """销售单据"""

    serializer_class = ReceiptSerializer
    # permission_classes = [IsAuthenticated, SalesOrderPermission]
    # filterset_class = SalesOrderFilter
    search_fields = ['number', 'customerName', 'state', 'remark']
    ordering_fields = ['id', 'number', 'state', 'total_amount', 'handle_time']
    select_related_fields = ['payee', 'consignor', 'drawer']
    prefetch_related_fields = ['sales_goods_set', 'sales_goods_set__goods',
                               'sales_goods_set__goods__unit',
                               'sales_goods_set__goods__brand', ]
    queryset = Receipt.objects.all()

    pagination_class = LimitedPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-id']

    @property
    def user(self):
        return self.request.user

    @property
    def context(self):
        return self.get_serializer_context()

    # 修改小票 state 为已收款时，修改现金余额
    # 修改小票 state 为已发货时，修改库存余额
    @transaction.atomic
    def perform_update(self, serializer):
        sales_order = serializer.save()
        # print(sales_order.total_amount)
        # print(sales_order.state == '已发货')
        if sales_order and sales_order.state == '已收款':
            # 同步现金余额

            entry_name = '营业收入'
            opening_balance = CashBalance.objects.order_by("id").last().cumulative or 0
            debit_amount = 0
            credit_amount = sales_order.total_amount
            cumulative_before = CashBalance.objects.order_by("id").last().cumulative or 0
            # print(cumulative_before)
            cumulative = NP.plus(cumulative_before, credit_amount)
            CashBalance(
                entry_name=entry_name, opening_balance=opening_balance, debit_amount=debit_amount,
                credit_amount=credit_amount, cumulative=cumulative).save()

        if sales_order and sales_order.state == '已发货':
            # 同步库存, 流水
            inventory_flows = []
            for sales_goods in sales_order.sales_goods_set.all():
                inventory = GoodsBalance.objects.get(goods=sales_goods.goods)
                quantity_before = inventory.total_quantity
                quantity_deliver_before = inventory.delivery_quantity
                quantity_change = sales_goods.sales_quantity

                quantity_deliver_after = NP.plus(quantity_deliver_before, quantity_change)
                quantity_after = NP.minus(quantity_before, quantity_change)

                inventory.delivery_quantity = quantity_deliver_after
                inventory.total_quantity = quantity_after
                if inventory.total_quantity < 0:
                    raise ValidationError(f'产品[{inventory.goods.brand.name}]库存不足')
                # inventory.has_stock = inventory.total_quantity > 0
                inventory.save(update_fields=['delivery_quantity', 'total_quantity'])



class CashBalanceViewSet(GenericViewSet, RetrieveModelMixin, ListModelMixin):
    """现金"""

    serializer_class = CashBalanceSerializer
    # permission_classes = [IsAuthenticated, InventoryPermission]
    # filterset_fields = ['goods']
    search_fields = ['entry_name']
    ordering_fields = ['id', 'entry_name','data']
    queryset = CashBalance.objects.all()

    pagination_class = LimitedPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['id']
    prefetch_related_fields = []

    @property
    def user(self):
        return self.request.user

    @property
    def context(self):
        return self.get_serializer_context()


class GoodsCountViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """盘点单据"""

    serializer_class = GoodsCountSerializer
    # permission_classes = [IsAuthenticated, StockCheckPermission]
    # filterset_class = StockCheckOrderFilter
    search_fields = ['numbers', 'remark']
    ordering_fields = ['id', 'numbers', 'date']
    select_related_fields = ['operator']
    prefetch_related_fields = ['good_count_set', 'good_count_set__goods',
                               'good_count_set__unit', 'good_count_set__brand', ]
    queryset = GoodsCount.objects.all()

    pagination_class = LimitedPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-id']

    @transaction.atomic
    def perform_create(self, serializer):
        good_count = serializer.save()
        for stock_check_goods in good_count.good_count_set.all():
            goods = stock_check_goods.goods

            # 同步库存, 流水
            inventory = GoodsBalance.objects.get(goods=goods)
            quantity_before = inventory.total_quantity
            quantity_change = stock_check_goods.Profit_loss
            quantity_after = stock_check_goods.actual_goods

            inventory.total_quantity = quantity_after
            if inventory.total_quantity < 0:
                raise ValidationError(f'产品[{inventory.goods.brand}]库存不足')

            inventory.save(update_fields=['total_quantity'])


class CashCountViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """现金盘点"""

    serializer_class = CashCountSerializer
    # permission_classes = [IsAuthenticated, StockCheckPermission]
    # filterset_class = StockCheckOrderFilter
    search_fields = ['numbers', 'remark']
    ordering_fields = ['id', 'numbers', 'date']
    select_related_fields = ['operator']
    prefetch_related_fields = []
    queryset = CashCount.objects.all()

    pagination_class = LimitedPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-id']


class UserViewSet(GenericViewSet, ListModelMixin, RetrieveModelMixin, CreateModelMixin):
    """用户"""

    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated, StockCheckPermission]
    # filterset_class = StockCheckOrderFilter
    search_fields = ['name', 'username']
    ordering_fields = ['id', 'create_time']

    prefetch_related_fields = []
    queryset = User.objects.all()

    pagination_class = LimitedPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    ordering = ['-id']
