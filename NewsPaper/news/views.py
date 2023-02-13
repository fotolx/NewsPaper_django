# from django.shortcuts import render
from django.views.generic import ListView, DetailView
# from django.core.paginator import Paginator
from .models import *
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')

    # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса 
    # (привет, полиморфизм, мы скучали!!!)
    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context