# coding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from mazdai_app.models import *
from mazdai_app.utils import get_datatables_records
from django import forms

def default(request):
    markets = Market.objects.all().order_by('name')
    non_sortable_columns = ', '.join(map(lambda i: str(i), range(3, markets.count() + 3)))

    return render_to_response('default.html', {'form':SaleForm(), 'markets': markets, 'non_sortable_columns':non_sortable_columns}, RequestContext(request))

def get_positions_list(request):
    querySet = Position.objects.all()
    columnIndexNameMap = { 0: 'id', 1: 'name', 2: 'description'}#not all columns
    searchableColumns = ['name', 'description']
    jsonTemplatePath = 'json_positions.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

def get_sales_list(request):
    querySet = SaleEntry.objects.all()
    columnIndexNameMap = { 0: 'date', 1: 'position__name', 2: 'quantity', 3:'market__name'}
    searchableColumns = ['position__name', 'market__name']
    jsonTemplatePath = 'json_sales.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

class SaleForm(forms.Form):
    position_id = forms.IntegerField(max_value=99999)
    market_id = forms.ChoiceField(label='Магазин', choices=map(lambda market: (market.id, market.name), Market.objects.all()))
    count = forms.IntegerField(max_value=999, label='Количество', initial=1, widget=forms.TextInput(attrs={'size':'10'}))


def sales(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)

        if form.is_valid():
            position_id_ = form.cleaned_data['position_id']
            market_id_ = form.cleaned_data['market_id']
            count_ = form.cleaned_data['count']

            position = Position.objects.get(id=position_id_)
            market = Market.objects.get(id=market_id_)

            goods_quantity = GoodsQuantity.objects.get(position=position, market=market)
            goods_quantity.quantity -= count_
            goods_quantity.save()

            entry = SaleEntry(position=position, date=datetime.datetime.now(),
                quantity=count_, market=market)
            entry.save()

        return HttpResponseRedirect('/')
    else:
        return render_to_response('sales_list.html', {'entries': SaleEntry.objects.all()})