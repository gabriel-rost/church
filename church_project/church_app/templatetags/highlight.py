import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
def highlight(text, query):
    if not text or not query:
        return text

    pattern = re.compile(re.escape(query), re.IGNORECASE)
    highlighted = pattern.sub(
        r'<mark>\g<0></mark>',
        text
    )
    return mark_safe(highlighted)