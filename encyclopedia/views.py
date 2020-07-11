import re

from markdown2 import markdown

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from . import util


def index(request):
    util.rand_list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title == "rand":
        entry = markdown(util.rand_list_entries())
        return render(request, "encyclopedia/entry.html", {
            "entry": entry,
            "title": title
        })

    result = util.get_entry(title)
    if result == None:
        entry = '<center><h1>No such entry!</h1></center>'
    else:
        entry = markdown(result)
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "title": title
    })

def search(request):
    if request.GET:
        req = request.GET['q']
        query = req.lower()

        res = util.search(query)
        if res == query:
            f = default_storage.open(f"entries/{res}.md")
            fr = f.read().decode("utf-8")
            entry = markdown(fr)
            return render(request, "encyclopedia/entry.html", {"entry": entry})

        return render(request, "encyclopedia/search.html", {
            "entries": util.search(query)
        })

def createNewPage(request):
    if request.POST:
        title = request.POST['title'].capitalize()
        content = request.POST['content']
        res = util.save_entry(title, content)
        if res == "success":
            r = util.get_entry(title)
            if r == None:
                entry = '<center><h1>No such entry!</h1></center>'
            else:
                entry = markdown(r)
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry,
                    "title": title
                })

        return render(request, "encyclopedia/entry.html", {
            "entry": f"<center><h1><a href='/wiki/{title}' style='font-size: 65px;'>{title}</a> Page Already exiest!</h1></center>"
        })

    return render(request, "encyclopedia/createPage.html")


def delete_entry(request, title):
    title = title.lower()
    util.delete_entry(title)

    return redirect("/")


def edit_entry(request):
    if request.POST:
        title = request.POST['title'].capitalize()
        content = request.POST['content']
        res = util.edit_entry(title, content)
        if res == "success":
            r = util.get_entry(title)
            if r == None:
                entry = '<center><h1>No such entry!</h1></center>'
            else:
                entry = markdown(r)
                return render(request, "encyclopedia/entry.html", {
                    "entry": entry,
                    "title": title
                })

    title = request.GET["q"]
    res = util.edit_entry_form(title)
    if res == None:
        return "er"

    return render(request, "encyclopedia/edit.html", {
        "content": res,
        "title": title
    })




