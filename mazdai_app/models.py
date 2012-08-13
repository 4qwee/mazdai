# coding=utf-8
from django.db import models

class Position(models.Model):

    number = models.IntegerField(unique=True, max_length=5, verbose_name='Номер позиции')
    name = models.CharField(max_length=300, verbose_name='Имя')
    quantity = models.IntegerField(verbose_name='Количество')
    price = models.FloatField(verbose_name='Цена')
    description = models.TextField(blank=True, verbose_name='Описание')
