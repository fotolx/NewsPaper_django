from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)
    pass

    def update_rating(self):
        author_rating = Post.objects.filter(author__exact=self).values('rating')
        # print(author_rating[0]['rating'])

        author_comments = Comment.objects.filter(user__exact=User.objects.get(id__exact=self.id)).values('comment_rating')
        # print(author_comments)
        sum_of_author_comments = 0
        for i in author_comments:
            sum_of_author_comments += i['comment_rating']
        # print(sum_of_author_comments)

        comments_to_author_articles = Comment.objects.filter(post__exact=Post.objects.filter(author__exact=self)[:1]).values('comment_rating')
        # print(comments_to_author_articles)
        sum_of_comments_to_author_articles = 0
        for i in comments_to_author_articles:
            sum_of_comments_to_author_articles += i['comment_rating']
        # print(sum_of_comments_to_author_articles)

        # print('user_rating =', 3*author_rating[0]['rating']+sum_of_author_comments+sum_of_comments_to_author_articles)
        self.user_rating = 3*author_rating[0]['rating']+sum_of_author_comments+sum_of_comments_to_author_articles
        self.save()
        pass


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, null=False)
    pass

class Post(models.Model):
    author = models.ForeignKey(Author, null=False, on_delete = models.CASCADE)
    article = 'ar'
    news = 'nw'
    TYPES = [
        (article, 'Статья'),
        (news, 'Новость'),
    ]
    type = models.CharField(max_length = 2, 
                                choices = TYPES, 
                                default = news)
    creation_date_time = models.DateTimeField(auto_now_add = True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    header = models.CharField(max_length=255, null=False)
    main_text = models.TextField()
    rating = models.IntegerField(default=0)
    pass

    def like(self):
        self.rating += 1
        self.save()
        pass

    def dislike(self):
        if self.rating:
            self.rating -= 1
        self.save()
        pass

    def preview(self):
        return self.main_text[:124]+'...'
        pass

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)
    pass

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.TextField()
    creation_date_time = models.DateTimeField()
    comment_rating = models.IntegerField(default=0)
    pass

    def like(self):
        self.comment_rating += 1
        self.save()
        pass

    def dislike(self):
        if self.comment_rating:
            self.comment_rating -= 1
        self.save()
        pass

# User.objects.create_user(username='user1', password='user1pass')
# author1 = Author.objects.create(username='user1')
# user1 = User.objects.get(username='user1')
# category1 = Category.objects.create(name='Спорт')
# category2 = Category.objects.create(name='Культура')
# category3 = Category.objects.create(name='Экономика')
# category4 = Category.objects.create(name='Наука')
# article2 = Post.objects.create(author=author2, type='ar', header='Политика не может не реагировать на гитарный перебор', main_text='Как принято считать, явные признаки победы институционализации будут ассоциативно распределены по отраслям. Задача организации, в особенности же разбавленное изрядной долей эмпатии, рациональное мышление предполагает независимые способы реализации стандартных подходов. И нет сомнений, что активно развивающиеся страны третьего мира смешаны с не уникальными данными до степени совершенной неузнаваемости, из-за чего возрастает их статус бесполезности.')
# news1 = Post.objects.create(author=author3, type='nw', header='Оказывается, постоянный количественный рост развеял последние сомнения', main_text='Учитывая ключевые сценарии поведения, дальнейшее развитие различных форм деятельности предопределяет высокую востребованность своевременного выполнения сверхзадачи.')
# setCategory5 = PostCategory.objects.create(post=news1, category=category4)
# comment5 = Comment.objects.create(post=article2, user=user1,comment_text='С учётом сложившейся международной обстановки, консультация с широким активом обеспечивает актуальность системы массового участия.',creation_date_time=datetime.now())

# article1 = Post.objects.get(id='1')
# article2 = Post.objects.get(id='2')
# news1 = Post.objects.get(id='3')

# author1 = Author.objects.get(id='1')
# author2 = Author.objects.get(id='2')
# author3 = Author.objects.get(id='3')

# Post.objects.filter(author__exact=author1).values('rating')
# Comment.objects.filter(user__exact=User.objects.get(id__exact=author1.id)).values('comment_rating')
# Comment.objects.filter(post__exact=)
# Comment.objects.all().values('post', 'rating')
# Comment.objects.filter(post__exact=Post.objects.filter(author__exact=author1)[:1]).values('comment_rating')

# bestuser = sorted(Author.objects.all().values('username', 'user_rating','id', 'post', 'username_id'), key=lambda d: d['user_rating'], reverse=True)[:1]

# Author.objects.all().values()

# print(f'Rating of {User.objects.get(id=bestuser[0]["username"])} is {bestuser[0]["user_rating"]}.')

bestarticle = sorted(Post.objects.all().values('rating','id'), key=lambda d: d['rating'], reverse=True)[:1]
articledata = Post.objects.get(id=bestarticle[0]['id'])
print(f'Дата добавления статьи: {articledata.creation_date_time}',
f'Имя пользователя: {articledata.author.username.username}',
f'Рейтинг: {articledata.rating}',
f'Заголовок статьи: {articledata.header}',
f'Превью статьи: {articledata.preview()}',
sep='\n')

commentslist = Comment.objects.filter(post=articledata.id).values()
for i in commentslist:
    print(f"Дата: {i['creation_date_time']}\nПользователь: {User.objects.get(id=i['user_id']).username}\nРейтинг: {i['comment_rating']}\nТекст: {i['comment_text']}\n")
