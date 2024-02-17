from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

from markdown2 import Markdown
from . import util

import secrets

class newEntry(forms.Form):
    error_css_class = 'error-field'
    required_css_class = 'required_field'
    title = forms.CharField(widget=forms.TextInput(attrs = {'class': 'col-xs-4',
    'placeholder': "Title of the Entry"}))
    description = forms.CharField(widget=forms.Textarea(attrs = {'class' : 'form-control col-md-8 col-lg-8',
    'rows': 3}))

class editEntry(forms.Form):
    error_css_class = 'error-field'
    required_css_class = 'required_field'
    description = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control col-md-8 col-lg-8',
    'rows': 3}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):

    markdowner = Markdown()

    '''To extract content from "/entries"'''
    item = util.get_entry(name)
    
    '''If not exists in "/entries", then show a page of error'''
    if not item:
        return render(request, 'encyclopedia/error.html',
            {"message": name}
        )
    
    return render(request, 'encyclopedia/entry.html',
        {"name": name, "html": markdowner.convert(item)}
    )

def search(request):
    
    name = request.GET.get('q')

    '''To extract content from "/entries"'''
    item = util.get_entry(name)
    
    '''If not exists in "/entries", then show a page of error'''
    if not item:

        entries = util.matched_entries(name)

        return render(request, 'encyclopedia/matching_entries.html',
            {"entries": entries}
        )

    '''Extracting html from .md'''
    markdowner = Markdown()
    
    return render(request, 'encyclopedia/entry.html',
        {"name": name, "html": markdowner.convert(item)}
    )

def add(request):
    
    '''Posting a text as an entry'''
    if request.method == "POST":
 
        '''Variable for the form class'''
        form = newEntry(request.POST)

        if form.is_valid():
            
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']

            desc = "# " + title + "\n" + desc

            if not util.get_entry(title):

                util.save_entry(title, desc)

                return HttpResponseRedirect(reverse('entry',
                    kwargs={"name": title}))
            else:
                return render(request, 'encyclopedia/error.html',
                {"exists": title}
                )
    else:
        return render(request, "encyclopedia/add.html",
        {"form": newEntry()})


def edit(request):
    
    '''Posting a text as an entry'''
    if request.method == "GET":
 
        '''Variable for the form class'''

        title = request.GET.get('title')

        entry = util.get_entry(title)

        form = editEntry()

        form.fields["description"].initial = entry

        return render(request, 'encyclopedia/edit.html',
        {"title": title, "form": form})

    else:

        '''Variable for the form class'''
        form = newEntry(request.POST)

        if form.is_valid():
            
            title = form.cleaned_data['title']
            desc = form.cleaned_data['description']

            util.save_entry(title, desc)

            return HttpResponseRedirect(reverse('entry',
                kwargs={"name": title}))

def random(request):
    title = secrets.choice(util.list_entries())
    return HttpResponseRedirect(reverse('entry',
        kwargs={"name": title}))