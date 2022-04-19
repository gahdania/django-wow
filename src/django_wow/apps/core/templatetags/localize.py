from django import template
register = template.Library()


@register.simple_tag(name='localize')
def localize(obj, locale, gender=None):
    if gender:
        return getattr(obj.get(locale=locale), gender.slug.lower())

    return obj.get(locale=locale)


@register.filter(name='div')
def div(value, arg):
    return int(value / arg)


@register.simple_tag(name='sortfield')
def sortfield(name, value):
    states = ('asc', 'desc', 'none')
    ret_val = 'asc'
    try:
        ret_val = states[states.index(value) + 1]
    except ValueError:
        ret_val = 'asc'
    except IndexError:
        ret_val = 'asc'
    finally:
        return f"{name}={ret_val}"

