from django.urls import path
from .views import PostsList, PostDetail, SearchList, PostsAdd, PostEdit, PostDelete
 
 
urlpatterns = [
    path('', PostsList.as_view()), 
    path('<int:pk>', PostDetail.as_view()),
    path('search', SearchList.as_view()),
    path('add', PostsAdd.as_view()), 
    path('<int:pk>/edit/', PostEdit.as_view()),
    path('<int:pk>/delete/', PostDelete.as_view()),
]