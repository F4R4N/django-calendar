from django import template
from ..models import Event
 
register = template.Library()
 
@register.simple_tag
def total_events():
    return Event.objects.count()
