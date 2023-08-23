from django.shortcuts import render
import markdown2
from markdown2 import Markdown
from . import util
import secrets 
from django.http import HttpResponseRedirect
from django.urls import reverse
from django import forms

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Entry Title" , widget=forms.TextInput(attrs={"class": "form-control", }))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class": "form-control"}))
    edit = forms.BooleanField(initial = False , widget = forms.HiddenInput(), required = False)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,entry):
    markdowner = Markdown()
    entry_page = util.get_entry(entry)
    if entry_page is None:
        return render(request,"encyclopedia/nonExistingEntry.html",{
            "entryTitle" : entry
        })
    else:
        return render(request,"encyclopedia/entry.html",{
            "entryTitle" : entry,
            "entry" : markdowner.convert(entry_page)
        })

def random_entry(request):
    entries = util.list_entries()
    random_entry = secrets.choice(entries)
    return HttpResponseRedirect(reverse("entry",kwargs={"entry": random_entry}))

def new_entry(request):
    if request.method=="POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            if(util.get_entry(title) is None or form.cleaned_data["edit"] == True ):  # Entry Does Not Exist
                util.save_entry(title,content)
                return HttpResponseRedirect(reverse(entry, kwargs={"entry": title}))
            else:   # Entry Exist
                return render(request,"encyclopedia/existing_entry.html",{
                    "title" : title,
                    "form" : form
                })    
        else:   # Form is Invalid
            return render(request,"encyclopedia/new_entry.html",{
                "form" : form,
                "existing" : False
            })
    else:
        return render(request,"encyclopedia/new_entry.html",{
                "form" : NewEntryForm(),
                "existing" : False
            })
            
def edit(request,entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request,"encyclopedia/nonExistingEntry.html",{
            "entryTitle"  : entry
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["edit"].initial = True
        form.fields["content"].initial = entryPage
        return render(request,"encyclopedia/new_entry.html",{
            "form" : form,
            "edit" : form.fields["edit"].initial, 
            "entryTitle" : form.fields["title"].initial
        })
        
def search_entry(request):
    markdowner = Markdown()
    entries = util.list_entries()
    search_key = request.GET.get("q", "")
    for entry in entries:
        if search_key.upper() == entry.upper():
            entry_page = util.get_entry(search_key)
            return render(request,"encyclopedia/entry.html",{
            "entryTitle" : search_key,
            "entry" : markdowner.convert(entry_page)
        })

    if search_key in entries:
        return redirect(get_entry, search_key)
    else:
        search_pages = [entry for entry in entries if search_key.lower() in entry.lower()]
        if search_pages != []:
            return render(request, "encyclopedia/index.html", {
                "entries":search_pages,
                "entryTitle" : search_key,
                "search" : True
                })
        else:
            return render(request,"encyclopedia/nonExistingEntry.html",{
                "entryTitle" : search_key
            })

