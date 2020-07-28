from django import template

"""To be a valid tag library, the module must 
contain a module-level variable named register 
that is a template.Library instance"""

register = template.Library()


"""The Library.filter() method takes two arguments:

The name of the filter – a string.
The compilation function – a Python function (not the name of the function as a string).
You can use register.filter() as a decorator instead:"""

@register.filter
def has_relationship(obj, args):
    return obj.has_relationship(args)

@register.filter
def has_request(obj, args):
    return obj.has_request(args)
