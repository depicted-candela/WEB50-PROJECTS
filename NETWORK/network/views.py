from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
import json

from .models import User, Post, Follow
from .forms import PostForm
from .tools import (load_posts, user_posts,
                    profile_info, fo_unfo,
                    following_posts_tool)

## main page
def index(request, *args, **kwargs):
    return render(request, "index.html", context={'page': 1, 'edit': 0}, status=200)

## loading data for main page
def posts(request, page, *args, **kwargs):

    data = load_posts(page)

    data['username'] = request.user.username

    return JsonResponse(data)

def following(request, userid, *args, **kwargs):

    return render(request, "following.html",
                  context={'page': 1, 'edit': 0, 'userid': userid}, status=200)

@csrf_protect
def following_posts(request, userid, pageid, *args, **kwargs):

    data = following_posts_tool(pageid, userid)

    return JsonResponse(data)

## to create a post
@csrf_protect
def new_post(request, *args, **kwargs):

    ## To post the tweet in the dbase
    if request.method == "POST":

        form = PostForm(request.POST or None)
        
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            return redirect("index")

        else:
            return render(request, "create.html", context={'form': form})
    
    # To get the form to post
    else:

        form = PostForm()
        return render(request, "create.html", context={'form': form, 'user': request.user})


## page for profile
def profile(request, userid, *args, **kwargs):

    if request.method == 'GET':
        
        username = User.objects.get(id=userid)

        context = profile_info(username)

        context['page'] = 1

        return render(request, "profile.html", context, status=context['status'])


# to render all own posts
def profile_posts(request, userid, page, *args, **kwargs):

    if request.method == 'GET':

        return JsonResponse(user_posts(userid, n_page=page))


## to create a post
@csrf_protect
def new_own_post(request, *args, **kwargs):

    ## To post the tweet in the dbase
    if request.method == "GET":

        form = PostForm()
        username = request.GET.get("send_user_to_django")
        context = profile_info(username)
        context['form'] = form
        context['new_post'] = 1

        return render(request, "create_own_post.html", context, status=context['status'])
    
    # To get the form to post
    else:

        form = PostForm(request.POST or None)
        
        if form.is_valid():

            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()

            return HttpResponseRedirect(reverse("profile", args=(request.user.id,)))
    
        else:

            context = profile_info(request.user.username)
            context['form'] = form
            context['new_post'] = 1

            return render(request, "create_own_post.html", context, status=context['status'])


## to update likes of a post
@csrf_protect
def update_like(request, *args, **kwargs):

    user = request.user.id

    ## PUT method
    if request.method == "PUT":
        
        if request.accepts('text/html'):

            body = request.body.decode('utf-8')
            body = json.loads(body)
            
            likes = list(Post.objects.filter(id=body['postid']).values_list('likes'))
            likes = [o[0] for o in likes]

            post = Post.objects.get(id=body['postid'])

            if user in likes:
                post.likes.remove(user)
            else:
                post.likes.add(user)
            
            post.save()

            return JsonResponse(load_posts(body['page']))
    
    else:
        return JsonResponse(load_posts())


## to update a post
@csrf_protect
def update_post(request, postid, *args, **kwargs):

    ## To post the tweet in the dbase
    if request.method == 'GET':

        post = Post.objects.get(pk=postid)
        
        if post.user.username == request.user.username:
        
            form = PostForm(instance=post)
            return render(request, 'edit_post.html', context={'form': form, 'postid': postid, 'action': str(postid)})
        
        else:

            return HttpResponseRedirect(reverse("index"))

    ## PUT method to edit the tweet in the dbase
    else:

        post = get_object_or_404(Post, pk=postid)
        form = PostForm(request.POST, instance=post)

        if form.is_valid():
            form.save()
        else:
            form = PostForm(instance=post)

        return HttpResponseRedirect(reverse("index"))


## to put follow or unfollow in the button
@csrf_protect
def follow_unfollow_button(request, *args, **kwargs):

    ## To change the follow_unfollow button
    if request.method == "GET":
        
        return JsonResponse(fo_unfo(request.user.id))


## to follow and unfollow
@csrf_protect
def follow_unfollow(request, *args, **kwargs):

    ## PUT method

    if request.accepts('text/html'):

        user = request.user.id
        body = request.body.decode('utf-8')
        body = json.loads(body)
        following = body['following']

        f_u = list(Follow.objects.filter(follower=user).values_list('following'))
        f_u = [o[0] for o in f_u]

        follow = Follow.objects.get(follower=user)

        if following in f_u:
            follow.following.remove(following)
        else:
            follow.following.add(following)
        
        follow.save()
        return JsonResponse(load_posts())

## page to see details of a tweet
def post_detail(request, post_id, *args, **kwargs):
    """ REST API Endpoint: dynamic view
    Consume by JavaScript or Swift or Java or iOS/Android
    return json data
    """
    data = {
            'id': post_id,
        }

    try:
        obj = Post.objects.get(id=post_id)
        data['text'] = obj.text
        return render(request, "post.html", context={}, status=200)
    except:
        data['message'] = 'Post does not exists'
        return JsonResponse(data, status=404)

def login_view(request):

    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "login.html", {
                "message": "Invalid username and/or password."
            })
    else:

        return render(request, "login.html")


def logout_view(request):
    
    logout(request)

    return HttpResponseRedirect(reverse("index"))


def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:

            user = User.objects.create_user(username, email, password)
            user.save()

        except IntegrityError:

            return render(request, "register.html", {
                "message": "Username already taken."
            })
        
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    
    else:

        return render(request, "register.html")
