from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(max_length=100, label='Title:', widget=forms.TextInput(attrs={
        'autocomplete': 'off'}))
    content = forms.CharField(widget=forms.Textarea, label='Content:')


def index(request):
    list_entries = util.list_entries()
    if request.method == 'GET':
        query = request.GET.get('q', False)
        if query:      
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

        else:
            return render(request, "encyclopedia/index.html", {
                "entries": list_entries
            })


def wiki_page(request, page):
    return render(request,"encyclopedia/content.html", {
        "page": page,
        "content": util.get_entry(page),
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
                util.save_entry(title,content)
                return render(request, "encyclopedia/content.html", {
                    "page": title,
                    "content": content
                })
            else:
                # print error
                error = "The {} has already existed!"
                return render(request,"encyclopedia/add.html",{
                    "form": form,
                    "error": error.format(title)
                })
    return render(request,"encyclopedia/add.html", {
        "form": NewEntryForm()
    })

