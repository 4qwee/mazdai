# coding=utf-8
from django.db import models

class Position(models.Model):

    name = models.CharField(max_length=300, verbose_name='Имя')
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание')

class SaleEntry(models.Model):

    position = models.ForeignKey(Position)
    date = models.DateTimeField(verbose_name='Дата')