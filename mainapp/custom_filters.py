from django import template
register = template.Library()

@register.filter(name='attr')
def attr(ob, val):
    try:
        return ob[int(val)]
    except:
        return getattr(ob, val)