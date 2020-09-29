from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
from random import choice
from markdown2 import Markdown

class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title:', widget=forms.TextInput(attrs={
        'autocomplete': 'off'}))
    content = forms.CharField(widget=forms.Textarea, label='Content:')


def wiki_search(request):
    if request.method == 'POST':
        list_entries = util.list_entries()
        query = request.POST['q']
        if query in list_entries:
            #return HttpResponseRedirect(reverse('encyclopedia:wiki_page',args=[query]))
            return HttpResponseRedirect(reverse('encyclopedia:wiki_page',kwargs={'page':query}))
        else:
            sub_list = []
            for entry in list_entries:
                if query in entry:
                    sub_list.append(entry)
            return render(request,"encyclopedia/search.html", {
                "entries": sub_list
            })
        

def index(request):
    list_entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": list_entries
    })


def wiki_page(request, page):
    list_entries = util.list_entries()
    if page not in list_entries:
        return render(request,'encyclopedia/content.html',{
            "page":page
        })
    else:
    #conver md to html
        markdowner = Markdown()
        content_md = util.get_entry(page)
        content_html = markdowner.convert(content_md)

        return render(request,"encyclopedia/content.html", {
            "page": page,
            "content": content_html,
        })


def wiki_add(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            entries = util.list_entries()
            title = form.cleaned_data['title']
            if title not in entries:
                # handle save
                content = form.cleaned_data['content']
                markdowner = Markdown()
                content_html = markdowner.convert(content)
                util.save_entry(title,content)
                return render(request, "encyclopedia/content.html", {
                    "page": title,
                    "content": content_html
                })
            else:
                # print error
                error = "The {} entry has already existed!"
                return render(request,"encyclopedia/add.html",{
                    "form": form,
                    "error": error.format(title)
                })
    return render(request,"encyclopedia/add.html", {
        "form": NewEntryForm()
    })


def wiki_edit(request,page):
    if request.method == 'POST':
        #Save entry
        content = request.POST['content']
        util.save_entry(page,content)
        return HttpResponseRedirect(reverse('encyclopedia:wiki_page',kwargs={'page':page}))
    return render(request,"encyclopedia/edit.html", {
        "page": page,
        "content": util.get_entry(page)
    })


def wiki_random(request):
    entries = util.list_entries()
    markdowner = Markdown()
   
    if not len(entries):
        
        return render(request,'encyclopedia/content.html', {
            "page": entries[0]
        })
    else:
        page = choice(entries)
        content_md = util.get_entry(page)
        content_html = markdowner.convert(content_md)
        return render(request,'encyclopedia/content.html', {
            "page": page,
            "content": content_html,
            "isRandom": True
        })
