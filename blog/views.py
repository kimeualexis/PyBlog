from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post, Comment
from .forms import CommentForm


"""
def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})
    """


class PostListView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    ordering = ['-created']
    paginate_by = 2


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-created')


class PostDetailView(DetailView):
    model = Post


def detail(request, post_id):
    form = CommentForm(request.POST or None)
    post = get_object_or_404(Post, pk=post_id)
    if form.is_valid():
        comm = form.save(commit=False)
        comm.post = post
        comm.author = request.user
        comm.save()
    form = CommentForm()
    return render(request, 'blog/post_detail.html', {'form': form, 'post': post})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


"""
class CommentListView(ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = ''
    """


class CommentCreateView(CreateView):
    model = Comment
    fields = ['comment']

    """
    def get_success_url(self):
        return reverse('blog:post-detail')
        """

    def form_valid(self, form, **kwargs):
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.author = self.request.user
        form.instance.post = post
        # form.instance.post = self.request.post
        return super(CommentCreateView, self).form_valid(form)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment

    fields = ['comment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


def about(request):
    return render(request, 'blog/about.html')


