# coding=utf-8
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mazdai_app.models import Position
from mazdai_app.utils import get_datatables_records
from django import forms

def default(request):
    form = SaleForm()
    return render_to_response('default.html', locals(), context_instance = RequestContext(request))

def get_positions_list(request):
    querySet = Position.objects.all()
    columnIndexNameMap = { 0: 'number', 1: 'name', 2: 'quantity', 3: 'description'}
    searchableColumns = ['number', 'name', 'description']
    jsonTemplatePath = 'json_positions.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

class SaleForm(forms.Form):
    number = forms.IntegerField(max_value=99999)
    count = forms.IntegerField(max_value=999, label='Количество')

def sales(request):
    if request.method == 'POST':
        form = SaleForm(request.POST)

        if form.is_valid():
            position = Position.objects.get(number=form.cleaned_data['number'])
            position.quantity -= form.cleaned_data['count']
            position.save()

    return HttpResponseRedirect('/')