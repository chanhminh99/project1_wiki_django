from django.urls import path

from . import views

app_name = "encyclopedia"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>", views.wiki_page, name="wiki_page"),
    path("search",views.wiki_search,name="wiki_search"),
    path("add",views.wiki_add, name="wiki_add"),
    path("editPage/<str:page>",views.wiki_edit, name="wiki_edit"),
    path("randomPage",views.wiki_random,name="wiki_random")
    
]
