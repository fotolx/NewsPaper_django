# from django.shortcuts import render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
# from django.core.paginator import Paginator
from .models import *
from .filters import PostFilter
from .forms import PostForm


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    form_class = PostForm

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['types'] = Post.TYPES
        context['form'] = PostForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        return super().get(request, *args, **kwargs)

    

class PostDetail(DetailView):
    # model = Post
    # template_name = 'post.html'
    # context_object_name = 'post'
    template_name = 'post.html'
    queryset = Post.objects.all()

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса 
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context
    
class PostsAdd(CreateView):
    model = Post
    template_name = 'posts_add.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    fields = '__all__'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['types'] = Post.TYPES
        return context
    
    def post(self, request, *args, **kwargs):
        # берём значения для новой публикации из POST-запроса отправленного на сервер
        author = request.POST['authors']
        type = request.POST['type']
        header = request.POST['header']
        main_text = request.POST['main_text']
        rating = request.POST['rating']
        category = request.POST['category']
        post = Post(author=Author.objects.get(username=author), type=type, header=header, 
        main_text=main_text, rating=rating)          # создаём новую публикацию
        post.save()                                  # и сохраняем
        post.category.set(category)                  # Добавляем категорию
        post.save()                                  # и сохраняем
        return super().get(request, *args, **kwargs) # отправляем пользователя обратно на GET-запрос.

class PostEdit(UpdateView):
    # model = Post
    template_name = 'post_edit.html'
    form_class = PostForm
    # context_object_name = 'post'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class PostDelete(DeleteView):
    # model = Post
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    # context_object_name = 'post'
    pass