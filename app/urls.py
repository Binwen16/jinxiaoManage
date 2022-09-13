from django.urls import re_path, path, include
from rest_framework.routers import DefaultRouter

from app.views import GoodsBrandViewSet, GoodsUnitViewSet, ReceiptViewSet, GoodsCountViewSet, CashCountViewSet, \
    GoodsViewSet, GoodBalanceViewSet, CashBalanceViewSet, UserViewSet

router = DefaultRouter()

router.register('goods_brand', GoodsBrandViewSet, 'goods_brand')
router.register('goods_units', GoodsUnitViewSet, 'goods_unit')
router.register('sales_orders', ReceiptViewSet, 'sales_order')
router.register('goods_count', GoodsCountViewSet, 'goods_count')
router.register('cash_count', CashCountViewSet, 'cash_count')
router.register('goods', GoodsViewSet, 'goods')
router.register('goods_balance', GoodBalanceViewSet, 'goods_balance')
router.register('cash_balance', CashBalanceViewSet, 'cash_balance')
router.register('staff', UserViewSet, 'staff')

urlpatterns = [
    path('', include(router.urls)),

    # path('article_detail/', views.article_detail.as_view()),

]
