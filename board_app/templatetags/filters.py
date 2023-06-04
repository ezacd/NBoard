from django import template

register = template.Library()


@register.filter()
def make_left(html):
    new = html.replace('>', ' style="text-align: left;">', 1)
    return new
