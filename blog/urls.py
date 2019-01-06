from django.urls import path
from . import views
from .views import (PostListView, PostDetailView,
                    PostCreateView, PostUpdateView, PostDeleteView)


app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='blog-index'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('create_new/', PostCreateView.as_view(), name='post-create'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]
