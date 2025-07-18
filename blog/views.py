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
    context_object_name = "posts"
    model = Post
    template_name = 'post_list.html'

@method_decorator(login_required(login_url="/"), name="dispatch")
class UpdatePost(UpdateView):
    model = Post
    template_name = "update_post.html"
    fields = ["post_header", "post_text"]

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
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("/")
    else:
        form = PostForm()

    return render(request, "new_post.html", {"form": form})


def loginview(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("blog:index")
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error_message": error_message})
    return render(request, "login.html")

def signupview(request):
    if request.method == "POST":
        username = request.POST.get("username").strip()
        password = request.POST.get("password")
        confirm_password = request.POST["confirm_password"]

        if not username or not password or not confirm_password:
            return render(request, "signup.html", {
                "error_message": "All fields are required."
            })
        
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error_message": "User  already exists"
            })


        if password == confirm_password:
            user = User.objects.create_user(username = username, password = password)
            user.save()
            login(request, user)
            return redirect("blog:index")
        else:
            error_message = "Passwords do not match!"
            return render(request, "signup.html", {"error_message": error_message})

    return render(request, "signup.html")


def logoutview(request):
    logout(request)
    return redirect("blog:index")