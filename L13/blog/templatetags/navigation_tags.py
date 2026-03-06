from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_url(context, pattern_name):
    try:
        current = context.request.resolver_match
    except AttributeError:
        return ''
    if not current:
        return ''
    if current.view_name == pattern_name:
        return 'active'
    if current.namespace and f"{current.namespace}:{current.url_name}" == pattern_name:
        return 'active'
    return ''
