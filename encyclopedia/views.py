from http.client import HTTPResponse
from django.shortcuts import render
import markdown2
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def wiki(request, title):
    searchparam = title.capitalize()
    if title.lower() not in list(map(lambda t: t.lower(), util.list_entries())):
        messages.error(request, 'Error: No such url found.')
        return HttpResponseRedirect(reverse("wiki:index"))
    page = util.get_entry(title)
    displaytitle = '# ' + title.capitalize()
    page = markdown2.markdown(page)
    displaytitle = markdown2.markdown(displaytitle)
    return render(request, "encyclopedia/entry.html", {
        "page": page, "searchparam": searchparam, "title": title, "displaytitle": displaytitle
    })


def search(request):
    if request.method == "GET":
        param = request.GET.get('q')
        if util.get_entry(param):
            return HttpResponseRedirect(reverse("wiki:wiki", args=[param]))
    error = f'No search results found for "{param}", sorry!'
    searchentries = []
    entries = util.list_entries()
    for entry in entries:
        if param.lower() in entry.lower():
            searchentries.append(entry)
    return render(request, "encyclopedia/search.html", {
        "searchentries": searchentries, "param": param, "error": error
    })


def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html")
    elif request.method == "POST":
        titledata = request.POST.get('titleform')
        contentdata = request.POST.get('contentform')
        link = f'<a href="/wiki/{titledata}">exists</a>'
        if titledata and contentdata:
            if titledata.lower() not in list(map(lambda t: t.lower(), util.list_entries())):
                util.save_entry(titledata, contentdata)
                messages.success(request, 'New entry added')
                return HttpResponseRedirect(reverse("wiki:index"))
        if link == '<a href="/wiki/">exists</a>':
            messages.error(
                request, f'Error: Did you forget to input a title?')
        else:
            messages.error(
                request, f'Error: Entry already {link}.')

        return HttpResponseRedirect(reverse("wiki:index"))


def edit(request, entry):
    if request.method == "GET":
        data = util.get_entry(entry)
        return render(request, "encyclopedia/edit.html", {"entry": entry, "data": data})
    elif request.method == "POST":
        edits = request.POST.get('contentform')
        if edits:
            util.save_entry(entry, edits)
            messages.success(request, 'Edited!')
            return HttpResponseRedirect(reverse("wiki:wiki", args=[entry]))
        messages.error(request, 'Error: Did you type anything?')
        return HttpResponseRedirect(reverse("wiki:wiki", args=[entry]))


def randompage(request):
    entries = util.list_entries()
    randomparam = random.choice(entries)
    return HttpResponseRedirect(reverse("wiki:wiki", args=[randomparam]))
