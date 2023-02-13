from django_filters import FilterSet # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post
 
 
# создаём фильтр
class PostFilter(FilterSet):
    class Meta:
        model = Post
        fields = {'author': ['exact'],
        'header': ['icontains'],
        'creation_date_time': ['gt']
        } 

   