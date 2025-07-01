from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

# Create your views here.
# def index(request):
#     posts = Post.objects.all()
#     return render(request, 'post_list.html', {'posts': posts})

class PostList(ListView):
    context_object_name = "posts"
    model = Post
    template_name = 'post_list.html'

class UpdatePost(UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ["post_header", "post_text"]

    def get_success_url(self):
        return reverse_lazy("blog:index")
    
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("blog:index")

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {"post": post})

def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, "new_post.html", {"form": form})