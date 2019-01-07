from django.urls import path
from . import views
from .views import (PostListView, PostDetailView,
                    PostCreateView, PostUpdateView,
                    PostDeleteView, UserPostListView,
                    CommentCreateView)


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blog-index'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('create_new/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='post-comment'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]
