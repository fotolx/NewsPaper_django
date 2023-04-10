from django.contrib import admin
from .models import *

class AuthorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Author._meta.get_fields()]

class CategoryAdmin(admin.ModelAdmin):
    # categories = Category._meta.get_fields()
    # list_display = [field.name for field in categories]
    list_display = ('name', 'userssubscribed', '_users', )

    @admin.display(description='Users list',)
    def	_users(self, row):
        return ', '.join([x.username for x in row.user.all()])

    @admin.display(description='Subscribers count',)
    def userssubscribed(self, row):
        return f'{row.userssubscribed_set.all().count()}' 
    
    # def user(self, user):
    #     groups = []
    #     for group in user.groups.all():
    #         groups.append(group.name)
    #     return ' '.join(groups)
        # group.short_description = 'Groups'

class PostAdmin(admin.ModelAdmin):
    fields = Post._meta.get_fields()  # При наличии этой строки падает на редактировании
    # list_display = [field.name for field in Post._meta.get_fields()]
    # list_display = ('header', 'author',  'creation_date_time',  )
    list_display = ('id', 'post_author', 'type', 'postcategory', 'post_header', 'post_text', 'rating', 'comment', 'creation_date_time',  )
    # list_display = [field.name for field in Post._meta.get_fields() if not field.many_to_many]

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

class CommentAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Comment._meta.get_fields()]

class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.get_fields()]

class UsersSubscribedAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UsersSubscribed._meta.get_fields()]

# Register your models here.
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UsersSubscribed, UsersSubscribedAdmin)