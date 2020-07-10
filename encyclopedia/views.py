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


def createNewPage(request):
    if request.POST:
        title = request.POST['title'].capitalize()
        content = request.POST['content']
        res = util.save_entry(title, content)
        if res == "success":
            return render(request, "encyclopedia/entry.html", {
                "entry": f"{title}'s page has been created successfully!"
            })
        return render(request, "encyclopedia/entry.html", {
            "entry": f"{title} => Already exiest!"
        })

    return render(request, "encyclopedia/createPage.html")


def delete_entry(request, title):
    title = title.lower()
    util.delete_entry(title)

    return redirect("/")


def entry(request, title):
    if title == "rand":

        res = util.rand_list_entries()
        entry = markdown(res)

        return render(request, "encyclopedia/entry.html", {
            "entry": entry
        })

    res = util.get_entry(title)
    if res == None:
        entry = '<center><h1>No such entry!</h1></center>'
    else:
        entry = markdown(res)

    return render(request, "encyclopedia/entry.html", {
        "entry": entry
    })


def q_entry(request):
    if request.GET:
        req = request.GET['q']
        query = req.lower()

        res = util.q_entry(query)
        if res == query:
            f = default_storage.open(f"entries/{res}.md")
            fr = f.read().decode("utf-8")
            entry = markdown(fr)
            return render(request, "encyclopedia/entry.html", {"entry": entry})

        return render(request, "encyclopedia/search.html", {
            "entries": util.q_entry(query)
        })

    return "error"
    # return redirect(url_for('index'))
