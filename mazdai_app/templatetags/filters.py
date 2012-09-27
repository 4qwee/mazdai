from django import template
register = template.Library()

@register.filter(name='calculate_sum')
def calculate_sum(entry):
    return entry.quantity * entry.position.price

@register.filter(name='calculate_total_sum')
def calculate_total_sum(entries_list):
    total = 0

    for entry in entries_list:
        total += calculate_sum(entry)

    return total