from django import template
from django.utils.safestring import mark_safe
import markdown

register = template.Library()

@register.filter
def convert_markdown(value):
    """
    Converte uma string Markdown em HTML usando a biblioteca markdown.
    """
    # Use 'extensions' para habilitar recursos avançados (como tabelas ou syntax highlighting)
    # Exemplo: extensions=['fenced_code', 'tables']
    html = markdown.markdown(value, extensions=['extra'])
    return mark_safe(html)