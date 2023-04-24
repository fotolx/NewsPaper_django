from django.contrib import admin
from .models import *

def nullfy_comment_rating(modeladmin, request, queryset): 
    queryset.update(comment_rating=0)
nullfy_comment_rating.short_description = 'Обнулить рейтинг'

def nullfy_post_rating(modeladmin, request, queryset): 
    queryset.update(rating=0)
nullfy_post_rating.short_description = 'Обнулить рейтинг'


class AuthorAdmin(admin.ModelAdmin):
    # fields_admin = Author._meta.get_fields()
    # list_display = [field.name for field in Author._meta.get_fields()]
    list_display = ('username', 'fio', 'user_rating', 'post',)
    list_filter = ('user_rating',)
    # fields = ('username', 'user_rating', )
    
    def fio(self, row):
        return f'{row.username.first_name} {row.username.last_name}'

    @admin.display(description='Posts count')
    def post(self, row):
        return row.post_set.all().count()

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'userssubscribed', '_users', )
    list_filter = ('name',)

    @admin.display(description='Users list',)
    def	_users(self, row):
        return ', '.join([x.username for x in row.user.all()])

    @admin.display(description='Subscribers count',)
    def userssubscribed(self, row):
        return f'{row.userssubscribed_set.all().count()}' 

class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'post_author', 'type', 'postcategory', 'post_header', 'post_text', 'rating', 'comment', 'creation_date_time',  )
    list_filter = ('type', 'category', 'rating', 'creation_date_time')
    search_fields = ('type', 'header', 'main_text', )
    actions = [nullfy_post_rating]

    @admin.display(description='Category',)
    def postcategory(self, row):
        return ', '.join([x.name for x in row.category.all()])
    
    @admin.display(description='Comments count',)
    def comment(self, row):
        return row.comment_set.all().count()

    @admin.display(description='author',)
    def post_author(self, row):
        return f'{row.author} ({row.author.username.first_name} {row.author.username.last_name})'
    
    @admin.display(description='Main text',)
    def post_text(self, row):
        return f'{row.main_text[:20]}...'
    
    @admin.display(description='Header',)
    def post_header(self, row):
        return f'{row.header[:10]}...'
    

class PostCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PostCategory._meta.get_fields()]
    list_filter = ('category', )

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]
    list_filter = ('user', 'comment_rating')
    actions = [nullfy_comment_rating]

class ProfileAdmin(admin.ModelAdmin):
    # fields_admin = Profile._meta.get_fields()
    # list_display = [field.name for field in Profile._meta.get_fields()]
    list_display = ('id', 'fio', 'user', 'avatar', 'bio',)
    list_filter = ('avatar', 'bio',)

    def fio(self, row):
        return f'{row.user.first_name} {row.user.last_name}'

class UsersSubscribedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UsersSubscribed._meta.get_fields()]
    list_filter = ('user', 'category',)

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UsersSubscribed, UsersSubscribedAdmin)