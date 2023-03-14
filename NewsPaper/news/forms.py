from django.forms import ModelForm
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from .models import Profile
from django import forms
from django.contrib.auth.models import User
 
# Создаём модельную форму
class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'type', 'category', 'header', 'main_text', 'rating']


class BasicSignupForm(SignupForm): 
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
    

class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email']


class UpdateProfileForm(forms.ModelForm):
    avatar = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}))
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']