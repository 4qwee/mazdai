# coding=utf-8
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import datetime
from django.utils.datastructures import MultiValueDictKeyError, SortedDict
import simplejson
from mazdai_app.forms import *
from mazdai_app.models import *
from mazdai_app.utils import get_datatables_records


#lists
def get_positions_list(request):
    querySet = Position.objects.all()
    columnIndexNameMap = {0: 'id', 1: 'name', 2: 'description', 3: 'price'}#not all columns
    searchableColumns = ['name', 'description']
    jsonTemplatePath = 'json_positions.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

def get_sales_list(request):
    querySet = SaleEntry.objects.all()
    columnIndexNameMap = {0: 'date', 1: 'position__name', 2: 'quantity', 3: 'market__name'}
    searchableColumns = ['position__name', 'market__name']
    jsonTemplatePath = 'json_sales.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

def get_moves_list(request):
    querySet = MoveEntry.objects.all()
    columnIndexNameMap = {0: 'date', 1: 'position__name', 2: 'quantity', 3: 'market__name', 4: 'market_to__name'}
    searchableColumns = ['position__name', 'market__name', 'market_to__name']
    jsonTemplatePath = 'json_moves.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

def get_credits_list(request):
    querySet = CreditEntry.objects.all()
    columnIndexNameMap = {0: 'id', 1: 'is_active', 2: 'date', 3: 'position__name', 4: 'quantity', 5: 'comment',
                          6: 'market__name'}
    searchableColumns = ['position__name', 'market__name', 'comment']
    jsonTemplatePath = 'json_credits.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

def get_orders_list(request):
    querySet = OrderEntry.objects.all()
    columnIndexNameMap = {0: 'id', 1: 'is_active', 2: 'date', 3: 'position__name', 4: 'quantity', 5: 'market__name'}
    searchableColumns = ['position__name', 'market__name']
    jsonTemplatePath = 'json_orders.txt'

    return get_datatables_records(request, querySet, columnIndexNameMap, searchableColumns, jsonTemplatePath)

def default(request):
    markets = Market.objects.all().order_by('name')
    start_markets_column = 4
    non_sortable_columns = ', '.join(map(lambda i: str(i), range(start_markets_column, markets.count() + start_markets_column)))

    return render_to_response('default.html',
        dict(saleForm=SaleForm(), markets=markets, non_sortable_columns=non_sortable_columns, moveForm=MoveForm(),
        creditForm=CreditForm(), orderForm=OrderForm()),
        RequestContext(request))

#post handlers & lists

def handle_form(request, formClass, handler):
    form = formClass(request.POST)

    if form.is_valid():
        handler(form)

        response = simplejson.dumps({'success': True})
    else:
        response = simplejson.dumps({'success': False, 'html': '<br/>'.join(map(lambda error_list: error_list.as_text(), form.errors.values()))})

    if request.is_ajax:
        return HttpResponse(response, content_type='application/javascript')

    return HttpResponseRedirect('/')

def sales(request):
    if request.method == 'POST':

        def custom_handler(form):
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

        return handle_form(request, SaleForm, custom_handler)
    else:
        return render_to_response('sales_list.html')

def moves(request):
    if request.method == 'POST':

        def custom_handler(form):
            position_id_ = form.cleaned_data['position_id']
            from_market_id_ = form.cleaned_data['market_id']
            to_market_id_ = form.cleaned_data['to_market_id']
            count_ = form.cleaned_data['count']

            goods_quantity_from = GoodsQuantity.objects.get(position__id=position_id_, market__id=from_market_id_)
            goods_quantity_from.quantity -= count_
            goods_quantity_from.save()

            goods_quantity_to = GoodsQuantity.objects.get(position__id=position_id_, market__id=to_market_id_)
            goods_quantity_to.quantity += count_
            goods_quantity_to.save()

            move_entry = MoveEntry(position=Position.objects.get(id=position_id_), date=datetime.datetime.now(),
                quantity=count_, market=Market.objects.get(id=from_market_id_),  market_to=Market.objects.get(id=to_market_id_))
            move_entry.save()

        return handle_form(request, MoveForm, custom_handler)

    else:
        return render_to_response('moves_list.html')

def credits(request):
    if request.method == 'POST':

        def custom_handler(form):
            position_id_ = form.cleaned_data['position_id']
            market_id_ = form.cleaned_data['market_id']
            count_ = form.cleaned_data['count']
            comment_ = form.cleaned_data['comment']

            position = Position.objects.get(id=position_id_)
            market = Market.objects.get(id=market_id_)

            goods_quantity = GoodsQuantity.objects.get(position=position, market=market)
            goods_quantity.quantity -= count_
            goods_quantity.save()

            entry = CreditEntry(position=position, market=market, date=datetime.datetime.now(), quantity=count_,
                comment=comment_)
            entry.save()

        return handle_form(request, CreditForm, custom_handler)
    else:
        return render_to_response('credits_list.html', {'credit_form': IdForm()}, RequestContext(request))

def orders(request):
    if request.method == 'POST':

        def custom_handler(form):
            position_id_ = form.cleaned_data['position_id']
            market_id_ = form.cleaned_data['market_id']
            count_ = form.cleaned_data['count']

            position = Position.objects.get(id=position_id_)
            market = Market.objects.get(id=market_id_)

            entry = OrderEntry(position=position, market=market, date=datetime.datetime.now(), quantity=count_)
            entry.save()

        return handle_form(request, OrderForm, custom_handler)
    else:
        return render_to_response('orders_list.html', {'order_form': IdForm()}, RequestContext(request))

def credits_tool(request):
    if request.method == 'POST':

        def custom_handler(form):
            credit_entry = CreditEntry.objects.get(id=form.cleaned_data['id_'])
            credit_entry.is_active = False
            credit_entry.save()

            sale_entry = SaleEntry(position=credit_entry.position, date=datetime.datetime.now(),
                quantity=credit_entry.quantity, market=credit_entry.market)
            sale_entry.save()

        return handle_form(request, IdForm, custom_handler)

def orders_tool(request):
    if request.method == 'POST':

        def custom_handler(form):
            order_entry = OrderEntry.objects.get(id=form.cleaned_data['id_'])
            order_entry.is_active = False
            order_entry.save()

            goods_quantity = GoodsQuantity.objects.get(position=order_entry.position, market=order_entry.market)
            goods_quantity.quantity += order_entry.quantity
            goods_quantity.save()

            #todo add entry

        return handle_form(request, IdForm, custom_handler)


def sales_report(request):
    try:
        day = int(request.GET['d'])
        month = int(request.GET['m'])
        year = int(request.GET['y'])

        entries = SaleEntry.objects.filter(date__day=day, date__month=month, date__year=year)
        grouped_entries = SortedDict()

        for entry in entries:
            if not grouped_entries.has_key(entry.market.name):
                grouped_entries[entry.market.name] = []

            grouped_entries[entry.market.name].append(entry)

        return render_to_response('sales_report.html', {'date': datetime.date(year, month, day), 'grouped_entries':grouped_entries})
    except MultiValueDictKeyError:
        return HttpResponseBadRequest('<h1>400 Bad Request</h1>')