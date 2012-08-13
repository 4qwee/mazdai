__author__ = '4qwee'

from django.contrib import admin
from mazdai_app.models import Position

class PositionAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')
    list_editable = ('name',)
    ordering = ['number']

admin.site.register(Position, PositionAdmin)