from django import forms, template

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css):
    existing = field.field.widget.attrs.get('class', '')
    classes = f"{existing} {css}".strip()
    attrs = {**field.field.widget.attrs, 'class': classes}
    return field.as_widget(attrs=attrs)


@register.filter(name='is_checkbox')
def is_checkbox(bound_field):
    return isinstance(bound_field.field.widget, forms.CheckboxInput)
