# coding=utf-8
from django.core.exceptions import ValidationError
from mazdai_app.models import *

def max_sale_count_validator(position_id, market_id, value):

    quantity = GoodsQuantity.objects.get(position__id=position_id, market__id=market_id).quantity

    if value > quantity:
        raise ValidationError('Число больше, чем имеется в наличии')