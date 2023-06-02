from django import template
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag(takes_context=True)
def is_admin(context):
    if str(context['user']) == 'AnonymousUser':
        return False
    else:
        return User.objects.get(username=context['user']).is_superuser
