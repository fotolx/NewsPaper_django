import stop_words
from django import template

 
register = template.Library()

@register.filter(name='censor')
def censor(value):
    return " ".join(["*"*len(word) if word.lower() in stop_words.filter_words else word for word in value.split()])
    