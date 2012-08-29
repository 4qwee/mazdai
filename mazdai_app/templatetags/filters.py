from django import template
register = template.Library()

@register.filter(name='calculate_sum')
def calculate_sum(sale_entry):
    return sale_entry.quantity * sale_entry.position.price

@register.filter(name='calculate_total_sum')
def calculate_total_sum(entries_list):
    total = 0

    for entry in entries_list:
        total += calculate_sum(entry)

    return total