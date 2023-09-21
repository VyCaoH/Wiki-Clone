from django.shortcuts import render, redirect
from . import util
from django import forms
from random import choice
import markdown2
class NewForm(forms.Form):
    entry = forms.CharField()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def display_entry(request, title):
    content = util.get_entry(title)
    html_content = markdown2.markdown(content)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "error_message": "This page cannot be found"})
    return render(request, "encyclopedia/display.html", {
        "title": title,
        "content": html_content
    })
    
def search(request):
    if request.method == "GET":
        query = request.GET.get('q', '')
        entries = util.list_entries()
        result = []
        for entry in entries:
            if query.lower() == entry.lower():
                return redirect('display_entry', title=entry)
            elif query.lower() in entry.lower():
                result.append(entry)
    return render(request, "encyclopedia/search_result.html",  {
        "query": query, 
        "results": result
    })

            
            

def new(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title):
            return render(request, "encyclopedia/error2.html", {
                "error_message2": "A page with this name already exists in this space"
            })
        util.save_entry(title, content)
        return redirect('display_entry', title=title)
    return render(request, "encyclopedia/new.html")


def edit(request, title):
    content = util.get_entry(title)
    if request.method == "POST":
        new_content = request.POST.get('content')
        util.save_entry(title, new_content)
        return redirect('display_entry', title=title)
    return render(request, "encyclopedia/edit.html", {
                      "title": title, 
                      "content": content
                 })

def random(request):
    entries = util.list_entries()
    selected = choice(entries)
    return redirect('display_entry', title=selected)