from django import template


register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter
def uglify(string):
    return ''.join([j.lower() if i % 2 == 0 else j.upper() for i,j in enumerate(string) ])