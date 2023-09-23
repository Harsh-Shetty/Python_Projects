from django.urls import path  # copied from default urls.py in Project
from .views import (PostListView,
                    PostDetailView, 
                    PostCreateView, 
                    PostUpdateView,
                    UserPostListView,
                    PostDeleteView)
from . import views  # . represents current directory i.e blog

# copied template from default urls.py in Project
urlpatterns = [  # INCLUDE (mention) this file (blog.urls) in Projects/urls.py so that the project looks for these in here.
    path(
        "", PostListView.as_view(), name="blog-home"
    ), # Path to HOME PAGE. Empty path ("") i.e localhost:8000/blog (/blog coming from Project/urls.py).
    #Grab 'PostListView class' from views.py. Name of path is blog-home. as_view() is a method which
    # tells Django to access this as view (WEB PAGE).
    #<> handles variables
    path("user/<str:username>", UserPostListView.as_view(), name="user-posts"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    # Primary key expected is integer. eg: post/1/ for 1st Post
    path("post/create_post/", PostCreateView.as_view(), name="post-create"),
    path("post/<int:pk>/update", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete", PostDeleteView.as_view(), name="post-delete"),
    path(
        "about/", views.about, name="blog-about"
    )
]