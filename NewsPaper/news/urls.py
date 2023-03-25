from django.urls import path
from .views import PostsList, PostDetail, SearchList, PostsAdd, PostEdit, PostDelete, SubscribeToCategory, UnSubscribeToCategory
 
urlpatterns = [
    path('', PostsList.as_view()), 
    path('<int:pk>', PostDetail.as_view(), name='details'),
    path('search', SearchList.as_view(), name='search'),
    path('add', PostsAdd.as_view()), 
    path('<int:pk>/edit/', PostEdit.as_view(), name='edit_post'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='delete_post'),
    path('<int:pk>/subscribe/', SubscribeToCategory.as_view(), name = 'subscribe'),
    path('<int:pk>/unsubscribe/', UnSubscribeToCategory.as_view(), name = 'unsubscribe'),
]