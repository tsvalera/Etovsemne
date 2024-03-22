from django.urls import path
from .views import *


urlpatterns = [
   path('news/', NewsList.as_view(), name='post_list'),
   path('news/<int:pk>/', NewsDetail.as_view(), name='post_detail'),
   path('news/search/', SearchList.as_view(), name='post_search'),
   path('news/create/', PostCreate.as_view(), name='news_create'),
   path('article/create/', PostCreate.as_view(), name='article_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='news_update'),
   path('article/<int:pk>/update/', PostUpdate.as_view(), name='article_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),
   path('article/<int:pk>/delete/', PostDelete.as_view(), name='article_delete'),
]

