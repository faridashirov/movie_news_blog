from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Post
from .forms import PostForm

# Create your views here.
# def index(request):
#     posts = Post.objects.all()
#     return render(request, 'post_list.html', {'posts': posts})

class PostList(ListView):
    model = Post
    firld = ["post_header", "post_text", "image"]
    context_object_name = "posts"
    template_name = 'post_list.html'
    
    def get_queryset(self):
        return Post.objects.all().order_by("-post_date", "-post_time", "-id")
    

@method_decorator(login_required(login_url="/"), name="dispatch")
class UpdatePost(UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ["post_header", "post_text", "image"]

    def get_success_url(self):
        return reverse_lazy("blog:index")
    

@login_required(login_url="/")
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect("blog:index")

def post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'post.html', {"post": post})

@login_required(login_url="/")
def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, "new_post.html", {"form": form})