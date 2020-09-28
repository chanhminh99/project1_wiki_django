from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki_page(request, page):
    return render(request,"encyclopedia/content.html", {
        "page": page,
        "content": util.get_entry(page),
    })

