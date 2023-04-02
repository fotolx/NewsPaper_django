from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
# from django.core.paginator import Paginator
from .models import *
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .forms import UpdateUserForm, UpdateProfileForm
from NewsPaper.settings import EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_USE_SSL
from django.template.loader import render_to_string
from datetime import date


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'user_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    form_class = PostForm
    fields = '__all__'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
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
    
class PostsAdd(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'posts_add.html'
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 10
    fields = '__all__'

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['authors'] = Author.objects.all()
        context['types'] = Post.TYPES
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    
    def post(self, request, *args, **kwargs):
        # берём значения для новой публикации из POST-запроса отправленного на сервер
        author = request.POST['authors']
        type = request.POST['type']
        header = request.POST['header']
        main_text = request.POST['main_text']
        rating = request.POST['rating']
        category = request.POST['category']
        publications = Post.objects.filter(author=Author.objects.get(username=author)).filter(creation_date_time__date=date.today())
        if publications.count() >= 3:
            return render(request, 'too_many_publications.html')
        post = Post(author=Author.objects.get(username=author), type=type, header=header, 
        main_text=main_text, rating=rating)          # создаём новую публикацию
        post.save()                                  # и сохраняем
        post.category.set(category)                  # Добавляем категорию
        post.save()                                  # и сохраняем
        return super().get(request, *args, **kwargs) # отправляем пользователя обратно на GET-запрос.

class PostEdit(LoginRequiredMixin, UpdateView):
    template_name = 'post_edit.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
    # Author check called only in post edit context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name = 'authors').exists()
        return context
    
class PostDelete(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'

    # def handle_no_permission(self):
    #     return redirect('/')


class BecomeAnAuthor(LoginRequiredMixin, TemplateView):
    template_name = 'author_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.groups.filter(name='authors').exists():
            author_group = Group.objects.get(name='authors')
            author_group.user_set.add(self.request.user)
        return context
    

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-profile')

class SubscribeToCategory(LoginRequiredMixin, TemplateView):
    template_name = 'subscribe.html'
    model = UsersSubscribed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        UsersSubscribed.objects.create(user=self.request.user, category=Category.objects.get(pk=context['pk']))
        context['subscribed'] = Category.objects.get(pk=context['pk'])
        return context
    
class UnSubscribeToCategory(LoginRequiredMixin, TemplateView):
    template_name = 'unsubscribe.html'
    model = UsersSubscribed

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_subcription = UsersSubscribed.objects.get(user=self.request.user, category=Category.objects.get(pk=context['pk']))
        delete_subcription.delete()
        context['unsubscribed'] = Category.objects.get(pk=context['pk'])
        return context