from django.shortcuts import render_to_response
from django.template.context import RequestContext
from mazdai_app.models import Position
from mazdai_app.utils import get_datatables_records

def default(request):
    return render_to_response('default.html', locals(), context_instance = RequestContext(request))

def get_positions_list(request):
    querySet = Position.objects.all()
    columnIndexNameMap = { 0: 'number', 1: 'name', 2: 'quantity', 3: 'description'}
    searchableColumns = ['number', 'name', 'description']
    jsonTemplatePath = 'json_positions.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)