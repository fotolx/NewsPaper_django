from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Author(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    user_rating = models.IntegerField(default=0)
    
    def __str__(self):
        return f'{self.username}'

    def update_rating(self):
        author_rating = Post.objects.filter(author__exact=self).values('rating')
        author_comments = Comment.objects.filter(user__exact=User.objects.get(id__exact=self.id)).values('comment_rating')
        sum_of_author_comments = 0
        for i in author_comments:
            sum_of_author_comments += i['comment_rating']
        comments_to_author_articles = Comment.objects.filter(post__exact=Post.objects.filter(author__exact=self)[:1]).values('comment_rating')
        sum_of_comments_to_author_articles = 0
        for i in comments_to_author_articles:
            sum_of_comments_to_author_articles += i['comment_rating']
        self.user_rating = 3*author_rating[0]['rating']+sum_of_author_comments+sum_of_comments_to_author_articles
        self.save()


class Category(models.Model):
    name = models.CharField(unique=True, max_length=255, null=False)


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


    def like(self):
        self.rating += 1
        self.save()


    def dislike(self):
        if self.rating:
            self.rating -= 1
        self.save()


    def preview(self):
        return self.main_text[:124]+'...'

    # добавим абсолютный путь, чтобы после создания нас перебрасывало на страницу с новостью
    def get_absolute_url(self): 
        return f'/news/{self.id}'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete = models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.TextField()
    creation_date_time = models.DateTimeField()
    comment_rating = models.IntegerField(default=0)


    def like(self):
        self.comment_rating += 1
        self.save()


    def dislike(self):
        if self.comment_rating:
            self.comment_rating -= 1
        self.save()

# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(default='default_userpic.png', upload_to='images/profile/')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    # resizing images
    def save(self, *args, **kwargs):
        super().save()
        img = Image.open(self.avatar.path)
        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
