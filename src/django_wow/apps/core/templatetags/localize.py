from django import template
register = template.Library()


@register.simple_tag(name='localize')
def localize(obj, locale, gender=None):
    if gender:
        return getattr(obj.get(locale=locale), gender.slug.lower()).replace('\n\r', '<br/>\n')

    return obj.get(locale=locale)


@register.filter(name='div')
def div(value, arg):
    return int(value / arg)


@register.simple_tag
def relative_url(value, field_name, urlencode=None):

    url = f'{field_name}={value}'
    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(lambda p: p.split('=')[0] != field_name, querystring)
        encoded_querystring = '&'.join(filtered_querystring)
        return f'?{encoded_querystring}&{url}'
    else:
        return f'?{url}'
