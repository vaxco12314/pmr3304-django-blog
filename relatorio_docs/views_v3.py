from django.urls import reverse_lazy
from django.views import generic
from .models import Post
from .forms import PostForm


class PostListView(generic.ListView):
    model = Post
    template_name = 'blog/post_list.html'


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'


class PostDeleteView(generic.DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('post_list')
