from django_filters import FilterSet # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, Author
 
 
# создаём фильтр
class PostFilter(FilterSet):
    # date_field = Post.DateTimeField(required=False, widget=DateInput(attrs={'type': 'datetime-local'}),
                                    #  initial=datetime.date.today(), localize=True)
    # Здесь в мета классе надо предоставить модель и указать поля, по которым будет фильтроваться (т.е. подбираться) 
    # информация о товарах
    class Meta:
        model = Post
        # поля, которые мы будем фильтровать (т.е. отбирать по каким-то критериям, имена берутся из моделей)
        fields = ('author',
        'header',
        'creation_date_time',
        ) 
        # fields = {'author__username': ['exact'],
        # 'header': ['icontains'],
        # 'creation_date_time': ['gt']
        # } 
        # fields = ('author__username', # 'author__username__first_name' Имя автора
        # 'header',
        # 'creation_date_time'
        # )
   