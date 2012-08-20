# coding=utf-8
__author__ = '4qwee'

from django.contrib import admin
from mazdai_app.models import *

class GoodsQuantityInline(admin.StackedInline):
    model = GoodsQuantity

    verbose_name = 'Магазин'

class PositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_editable = ('name',)
    ordering = ['id']
    inlines = [GoodsQuantityInline]

class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', )
    ordering = ['name']

admin.site.register(Position, PositionAdmin)
admin.site.register(Market, MarketAdmin)