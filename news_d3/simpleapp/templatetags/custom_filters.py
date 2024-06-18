from django import template


register = template.Library()
censor_list = ['почти', 'хорошего', 'честность', 'главного']
CURRENCIES_SYMBOLS = {
   'rub': 'Р',
   'usd': '$',
}

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(price, code='rub'):
   """
   # value: значение, к которому нужно применить фильтр
   code: код валюты
   """
   postfix = CURRENCIES_SYMBOLS[code]
   # Возвращаемое функцией значение подставится в шаблон.
   return f'{price} {postfix}'

@register.filter
def lower(value):
    return value.lower()


@register.filter
def replace(value):
    words = value.split(' ')
    result = []
    for word in words:
        if word in censor_list:
            result.append(word[0] + "*" * (len(word)-2) + word[-1])
        else:
            result.append(word)
    return " ".join(result)

