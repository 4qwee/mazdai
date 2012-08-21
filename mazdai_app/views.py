# coding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from mazdai_app.models import *
from mazdai_app.utils import get_datatables_records
from django import forms

def default(request):
    return render_to_response('default.html', {'form':SaleForm(), 'markets':Market.objects.all().order_by('name')}, RequestContext(request))

def get_positions_list(request):
    querySet = Position.objects.all()
    columnIndexNameMap = { 0: 'id', 1: 'name', 2: 'description'}#not all columns
    searchableColumns = ['name', 'description']
    jsonTemplatePath = 'json_positions.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

def get_sales_list(request):
    querySet = SaleEntry.objects.all()
    columnIndexNameMap = { 0: 'date', 1: 'position.name', 2: 'quantity'}
    searchableColumns = ['position.name']
    jsonTemplatePath = 'json_sales.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

class SaleForm(forms.Form):
    number = forms.IntegerField(max_value=99999)
    count = forms.IntegerField(max_value=999, label='Количество')

def sales(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)

        if form.is_valid():
            position = Position.objects.get(id=form.cleaned_data['number'])
            count_ = form.cleaned_data['count']
            position.quantity -= count_
            position.save()

            entry = SaleEntry(position=position, date=datetime.datetime.now(), quantity=count_)
            entry.save()

        return HttpResponseRedirect('/')
    else:
        return render_to_response('sales_list.html', {'entries': SaleEntry.objects.all()})