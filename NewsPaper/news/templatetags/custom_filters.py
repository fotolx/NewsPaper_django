import stop_words
from django import template

 
register = template.Library()

@register.filter(name='censor')
def censor(value):
    return " ".join([word[0] + "*"*(len(word)-2) + word[-1] if word.lower() in stop_words.filter_words else word for word in value.split()])