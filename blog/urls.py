from django.urls import path
from . import views

app_name = "blog"
urlpatterns = [
    path('', views.PostList.as_view(), name='index'),
    path('<int:post_id>/', views.post, name='post'),
    path('new_post/', views.new_post, name="new_post"),
    path('update/<int:pk>/', views.UpdatePost.as_view(), name="update_post"), 
    path('delete/<int:pk>/', views.delete_post, name="delete_post"), 
]