from markdown2 import markdown
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })
    
def entry(request, title):
    res = util.get_entry(title)
    if res == None:
        entry = '<center><h1>No such entry!</h1></center>'
    else:
        entry = markdown(res)
    
    return render(request, "encyclopedia/entry.html", {
      "entry": entry
    })

def q_entry(request, query):
    return render(request, "encyclopedia/search.html", {
      "entries": util.q_entry(query)
    })
