# Список всех команд, запускаемых в Django shell
```python3 manage.py makemigrations```
```python3 manage.py migrate```
```python3 manage.py shell```
```from news.models import *```

## Создать двух пользователей (с помощью метода User.objects.create_user).
```user1 = User.objects.create_user(username='user1', password='user1pass')```
```user2 = User.objects.create_user(username='user2', password='user2pass')```
```user3 = User.objects.create_user(username='user3', password='user3pass')```

## Создать два объекта модели Author, связанные с пользователями.
```author1 = Author.objects.create(username=user1)```
```author2 = Author.objects.create(username=user2)```
```author3 = Author.objects.create(username=user3)```

## Добавить 4 категории в модель Category.
```category1 = Category.objects.create(name='Спорт')```
```category2 = Category.objects.create(name='Культура')```
```category3 = Category.objects.create(name='Экономика')```
```category4 = Category.objects.create(name='Наука')```

## Добавить 2 статьи и 1 новость.
```article1 = Post.objects.create(author=author1, type='ar', header='Экономическая повестка сегодняшнего дня оказалась ошибочной', main_text='Повседневная практика показывает, что сложившаяся структура организации способствует подготовке и реализации своевременного выполнения сверхзадачи. Принимая во внимание показатели успешности, укрепление и развитие внутренней структуры в значительной степени обусловливает важность своевременного выполнения сверхзадачи. Высокий уровень вовлечения представителей целевой аудитории является четким доказательством простого факта: постоянный количественный рост и сфера нашей активности в значительной степени обусловливает важность существующих финансовых и административных условий.')```

```article2 = Post.objects.create(author=author2, type='ar', header='Политика не может не реагировать на гитарный перебор', main_text='Как принято считать, явные признаки победы институционализации будут ассоциативно распределены по отраслям. Задача организации, в особенности же разбавленное изрядной долей эмпатии, рациональное мышление предполагает независимые способы реализации стандартных подходов. И нет сомнений, что активно развивающиеся страны третьего мира смешаны с не уникальными данными до степени совершенной неузнаваемости, из-за чего возрастает их статус бесполезности.')```

```news1 = Post.objects.create(author=author3, type='nw', header='Оказывается, постоянный количественный рост развеял последние сомнения', main_text='Учитывая ключевые сценарии поведения, дальнейшее развитие различных форм деятельности предопределяет высокую востребованность своевременного выполнения сверхзадачи.')```

## Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
```setCategory1 = PostCategory.objects.create(post=article1, category=category3)```
```setCategory2 = PostCategory.objects.create(post=article1, category=category4)```
```setCategory3 = PostCategory.objects.create(post=article2, category=category3)```
```setCategory4 = PostCategory.objects.create(post=news1, category=category3)```
```setCategory5 = PostCategory.objects.create(post=news1, category=category4)```

## Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
```comment1 = Comment.objects.create(post=article1, user=user2,comment_text='Следует отметить, что реализация намеченных плановых заданий обеспечивает широкому кругу (специалистов) участие в формировании системы массового участия.',creation_date_time=datetime.now())```

```comment2 = Comment.objects.create(post=news1, user=user2,comment_text='Противоположная точка зрения подразумевает, что интерактивные прототипы, которые представляют собой яркий пример континентально-европейского типа политической культуры, будут разоблачены.',creation_date_time=datetime.now())```

```comment3 = Comment.objects.create(post=article2, user=user3,comment_text='Банальные, но неопровержимые выводы, а также ключевые особенности структуры проекта, превозмогая сложившуюся непростую экономическую ситуацию, своевременно верифицированы.',creation_date_time=datetime.now())```

```comment4 = Comment.objects.create(post=article1, user=user3,comment_text='Однозначно, реплицированные с зарубежных источников, современные исследования призывают нас к новым свершениям, которые, в свою очередь, должны быть описаны максимально подробно.',creation_date_time=datetime.now())```

```comment5 = Comment.objects.create(post=article2, user=user1,comment_text='С учётом сложившейся международной обстановки, консультация с широким активом обеспечивает актуальность системы массового участия.',creation_date_time=datetime.now())```

## Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
```article1.like()```
```article2.like()```
```news1.like()```
```news1.dislike()```
```comment1.like()```
```comment2.like()```
```comment3.like()```
```comment4.like()```
```comment5.like()```

## Обновить рейтинги пользователей.
```author1.update_rating()```
```author2.update_rating()```
```author3.update_rating()```

## Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
```
bestuser = sorted(Author.objects.all().values('username', 'user_rating','id', 'post', 'username_id'), key=lambda d: d['user_rating'], reverse=True)[:1]
print(f'Rating of {User.objects.get(id=bestuser[0]["username"])} is {bestuser[0]["user_rating"]}.')
```

## Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье.
```
print(f'Дата добавления статьи: {articledata.creation_date_time}',
f'Имя пользователя: {articledata.author.username.username}',
f'Рейтинг: {articledata.rating}',
f'Заголовок статьи: {articledata.header}',
f'Превью статьи: {articledata.preview()}',
sep='\n')
```

## Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
```
commentslist = Comment.objects.filter(post=articledata.id).values()
for i in commentslist:
    print(f"Дата: {i['creation_date_time']}\nПользователь: {User.objects.get(id=i['user_id']).username}\nРейтинг: {i['comment_rating']}\nТекст: {i['comment_text']}\n")
```