from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    # Use get so that if key is missing, it returns None. If you do
    # dictionary[key] it will raise a KeyError then.
    # http://stackoverflow.com/questions/8000022/django-template-how-to-lookup-a-dictionary-value-with-a-variable
    #
    # {{ mydict|get_item:item.NAME }}
    return dictionary.get(key)
