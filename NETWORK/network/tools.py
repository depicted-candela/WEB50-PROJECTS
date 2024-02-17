from django.forms.models import model_to_dict
from functools import reduce
from operator import or_
from django.core import serializers
from django.db.models import Q
from django.core.paginator import Paginator

from .models import Post, User, Follow

import json

## tools for load all posts
def load_posts(n_page=1):

    paging = Paginator(Post.objects.all(), 10)
    page = paging.get_page(n_page)


    info = dict()

    info['has_previous'] = page.has_previous()
    info['has_next'] = page.has_next()
    try:
        info['previous_page_number'] = page.previous_page_number()
    except:
        info['previous_page_number'] = None
    info['number'] = page.number
    info['num_pages'] = page.paginator.num_pages
    try:
        info['next_page_number'] = page.next_page_number()
    except:
        info['next_page_number'] = None

    objs = page.object_list
    objs = [model_to_dict(i) for i in objs]
    
    posts_list = [{'likes': len(i['likes']), 'user': json.dumps(str(User.objects.get(id=i['user']))), 'id': i['id'], 'text': i['text'], 'image': json.dumps(str(i['image'])), 'date': i['posting_time']} for i in objs]

    data = {
        'response': posts_list,
        'paging': info
    }

    return data

## tools for load all posts
def following_posts_tool(n_page=1, userid=1):

    paging = Paginator(Post.objects.all(), 10)
    page = paging.get_page(n_page)

    following = Follow.objects.filter(follower=userid)

    # Using serializers
    person_dict_list = serializers.serialize('python', following)

    f_u = person_dict_list[0]['fields']['following']

    conditional = reduce(or_, [Q(user=i) for i in f_u])

    paging = Paginator(Post.objects.filter(conditional), 10)
    
    page = paging.get_page(n_page)

    info = dict()

    info['has_previous'] = page.has_previous()
    info['has_next'] = page.has_next()
    try:
        info['previous_page_number'] = page.previous_page_number()
    except:
        info['previous_page_number'] = None
    info['number'] = page.number
    info['num_pages'] = page.paginator.num_pages
    try:
        info['next_page_number'] = page.next_page_number()
    except:
        info['next_page_number'] = None

    objs = page.object_list
    objs = [model_to_dict(i) for i in objs]
    
    posts_list = [{'likes': len(i['likes']), 'user': json.dumps(str(User.objects.get(id=i['user']))), 'id': i['id'], 'text': i['text'], 'image': json.dumps(str(i['image'])), 'date': i['posting_time']} for i in objs]

    data = {
        'response': posts_list,
        'paging': info
    }

    return data

## posts for a certain user
def user_posts(user, n_page=1):

    objs = Post.objects.filter(user=user)
    paging = Paginator(Post.objects.filter(user=user), 10)

    page = paging.get_page(n_page)

    info = dict()
    info['has_previous'] = page.has_previous()
    info['has_next'] = page.has_next()
    
    try:
        info['previous_page_number'] = page.previous_page_number()
    except:
        info['previous_page_number'] = None

    info['number'] = page.number
    info['num_pages'] = page.paginator.num_pages
    
    try:
        info['next_page_number'] = page.next_page_number()
    except:
        info['next_page_number'] = None

    objs = page.object_list
    
    try:
        len(objs)
    except:
        objs = model_to_dict(objs)
        posts_list = [{'likes': len(objs['likes']), 'user': json.dumps(str(User.objects.get(id=objs['user']))), 'id': objs['id'], 'text': objs['text'], 'image': json.dumps(str(objs['image']))}]
    else:
        objs = [model_to_dict(i) for i in objs]
        posts_list = [{'likes': len(i['likes']), 'user': json.dumps(str(User.objects.get(id=i['user']))), 'id': i['id'], 'text': i['text'], 'image': json.dumps(str(i['image']))} for i in objs]

    data = {
        'response': posts_list,
        'paging': info
    }

    return data

def count_followers_following(user):

    following = list(Follow.objects.filter(follower=user).values_list('following'))
    following = [fi[0] for fi in following]

    other_accounts = list(Follow.objects.filter(~Q(follower=user)).values_list('follower', 'following'))

    followers = [fe[0] for fe in other_accounts if fe[1]==user]
    both = {'followers':followers, 'following': following}

    return both

def profile_info(username):
    try:

        user_info = User.objects.get(username=username)

    except:

        usern = username
        userid = 0
        exists = 0
        status = 404
        followers = []
        following = []

    else:

        usern = user_info.username
        userid = user_info.id
        exists = 1
        status = 200
        f_u = count_followers_following(user_info.id)
        followers = f_u['followers']
        following = f_u['following']

    context = {
        'username': usern,
        'userid': userid,
        'exists': exists,
        'followers': len(followers),
        'following': len(following),
        'status': status
    }

    return context

def fo_unfo(user):

    following = list(Follow.objects.filter(follower=user).values_list('following'))
    following = [fi[0] for fi in following]

    other_accounts = list(Follow.objects.filter(~Q(follower=user)).values_list('follower', 'following'))

    followers = [fe[0] for fe in other_accounts if fe[1]==user]

    f = {'following':following, 'followers':followers}

    return f