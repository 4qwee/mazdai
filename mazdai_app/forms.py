# coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
import django.forms
from mazdai_app.models import Market
from mazdai_app.validators import max_sale_count_validator

class SaleForm(forms.Form):
    position_id = forms.IntegerField(widget=forms.HiddenInput)
    market_id = forms.ChoiceField(label='Магазин',
        choices=map(lambda market: (market.id, market.name), Market.objects.all()))
    count = forms.IntegerField(label='Количество', initial=1,
        widget=forms.TextInput(attrs={'size': '10'}), error_messages={'invalid': 'Неправильное значение!'})

    def is_valid(self):
        if super(SaleForm, self).is_valid():

            try:
                max_sale_count_validator(self.cleaned_data['position_id'], self.cleaned_data['market_id'],
                    self.cleaned_data['count'])

                return True
            except ValidationError as e:
                self._errors['count'] = self.error_class([e.messages[0]])

        return False

class MoveForm(SaleForm):
    def __init__(self, *args, **kwargs):
        super(MoveForm, self).__init__(*args, **kwargs)

        self.fields.keyOrder = ['position_id', 'market_id', 'to_market_id', 'count']

    market_id = forms.ChoiceField(label='Из магазина',
        choices=map(lambda market: (market.id, market.name), Market.objects.all()))
    to_market_id = forms.ChoiceField(label='В магазин',
        choices=map(lambda market: (market.id, market.name), Market.objects.all()))

    def is_valid(self):
        if super(MoveForm, self).is_valid():
            if self.cleaned_data['market_id'] == self.cleaned_data['to_market_id']:
                self._errors['count'] = self.error_class(['Магазины совпадают!'])
                return False
            else:
                return True

class CreditForm(SaleForm):
    comment = forms.CharField(label='Комментарий', widget=forms.Textarea(attrs={'cols': 28}))