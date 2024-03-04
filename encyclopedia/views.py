from django.shortcuts import render
from markdown2 import Markdown

from . import util

def convert_md_to_html(title):
    content = util.get_entry(title)
    markdowner = Markdown()
    if content == None:
        return None
    else:
        return markdowner.convert(content)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        
    })

def entry(request, title):
    entry_file = convert_md_to_html(title)
    if entry_file == None:
        return render(request, "encyclopedia/error.html",{
            "message" : "This enntry does not exist!"
        })
    else:
        return render(request, "encyclopedia/entry.html",{
            "title": title,
            "content" : entry_file
        })
    
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        html_content = convert_md_to_html(entry_search)
        if html_content is not None:
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            all_entries = util.list_entries()
            recomendation = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recomendation.append(entry)
            return render(request, "encyclopedia/search.html", {
                "recomendation" : recomendation
            })