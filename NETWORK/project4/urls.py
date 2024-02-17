"""project4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path

from network.views import (
    index, login_view, logout_view,
    register, posts, post_detail, new_post,
    update_like, profile, profile_posts,
    new_own_post, follow_unfollow,
    follow_unfollow_button, update_post,
    following, following_posts,
)

urlpatterns = [
    path("", index, name="index"),
    path("posts/<int:page>", posts, name="Posts"),
    path("update_post/<int:postid>", update_post, name="Edit post"),
    path("following/<int:userid>/", following, name="following"),
    path("following_posts/<int:userid>/<int:pageid>", following_posts, name="Following posts"),
    path("new_post", new_post, name="New post"),
    path("new_own_post", new_own_post, name="New own post"),
    path("follow_unfollow", follow_unfollow, name="Follow and unfollow"),
    path("follow_unfollow_button", follow_unfollow_button, name="Follow_unfollow button"),
    path("update_like", update_like, name="update_like"),
    path("<int:userid>/", profile, name = "Profile"),
    path("<int:userid>/posts/<int:page>", profile_posts, name = "profile posts"),
    path("post/<int:post_id>", post_detail, name="Post details"),
    path("login", login_view, name="login"),
    path("logout", logout_view, name="logout"),
    path("register", register, name="register"),
    path("admin/", admin.site.urls, name="login"),
]
