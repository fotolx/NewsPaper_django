from django.forms import BooleanField, ModelForm
from .models import Post
 
 
# Создаём модельную форму
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'category', 'header', 'main_text', 'rating']