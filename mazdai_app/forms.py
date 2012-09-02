# coding=utf-8
from django import forms
from django.core.exceptions import ValidationError
import django.forms
from mazdai_app.models import Market
from mazdai_app.validators import max_sale_count_validator

class SaleForm(forms.Form):
    position_id = forms.IntegerField(max_value=99999)
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