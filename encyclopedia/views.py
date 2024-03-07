from django.shortcuts import render
from markdown2 import Markdown
import random
from django.http import HttpResponseRedirect
from django.http import HttpResponseNotAllowed
from . import util
from django.urls import reverse


# Function to convert Markdown content to HTML
def convert_md_to_html(title):
    # Retrieve content from the utility function based on the provided title
    content = util.get_entry(title)
    markdowner = Markdown()  # Initialize Markdown instance
    if content == None:  # If content does not exist for the given title
        return None
    else:
        return markdowner.convert(content)  # Convert Markdown content to HTML

# View function for the index page
def index(request):
    # Render the index.html template with a list of encyclopedia entries
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

# View function for displaying an encyclopedia entry
def entry(request, title):
    # Convert Markdown content to HTML for the given title
    entry_file = convert_md_to_html(title)
    if entry_file == None:  # If entry does not exist
        return render(request, "encyclopedia/error.html", {
            "message" : "This entry does not exist!"
        })
    else:
        # Render the entry.html template with the title and content
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content" : entry_file
        })
    
# View function for searching encyclopedia entries
def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']  # Retrieve search query from POST request
        html_content = convert_md_to_html(entry_search)  # Convert search query to HTML
        if html_content is not None:  # If search query returns a result
            return render(request, "encyclopedia/entry.html", {
                "title": entry_search,
                "content": html_content
            })
        else:
            # Find partial matches for the search query
            all_entries = util.list_entries()
            recomendation = []
            for entry in all_entries:
                if entry_search.lower() in entry.lower():
                    recomendation.append(entry)
            # Render the search.html template with recommended entries
            return render(request, "encyclopedia/search.html", {
                "recomendation" : recomendation
            })
        
# View function for creating a new encyclopedia page
def new_page(request):
    if request.method == "GET":
        # Render the new_page.html template for creating a new page
        return render(request,"encyclopedia/new_page.html")
    else:
        title       = request.POST['title']  # Retrieve title from POST request
        content     = request.POST['content']  # Retrieve content from POST request
        title_exist = util.get_entry(title)  # Check if title already exists
        if title_exist is not None:  # If title already exists
            return render(request, "encyclopedia/error.html",{
                "message": "This title entry already exist"
            })
        else:
            util.save_entry(title, content)  # Save new entry
            html_content = convert_md_to_html(title)  # Convert content to HTML
        # Render the entry.html template with the new page
        return render(request,"encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })
    
# View function for editing an encyclopedia page
def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']  # Retrieve title from POST request
        content = util.get_entry(title)  # Retrieve content based on the provided title
        # Render the edit.html template with the title and content for editing
        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content" : content
        })

# View function for saving an edited encyclopedia page
def save_edit(request):
    if request.method == "POST":
        title = request.POST['title']  # Retrieve title from POST request
        content = request.POST['content']  # Retrieve content from POST request
        util.save_entry(title, content)  # Save the edited entry
        html_content = convert_md_to_html(title)  # Convert content to HTML
        # Render the entry.html template with the updated content
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": html_content
        })

# View function for displaying a random encyclopedia page
def random_page(request):
    all_entries = util.list_entries()  # Get all encyclopedia entries
    random_entry = random.choice(all_entries)  # Choose a random entry
    html_content = convert_md_to_html(random_entry)  # Convert content to HTML
    # Render the entry.html template with the randomly selected entry
    return render(request, "encyclopedia/entry.html", {
        "title": random_entry,
        "content": html_content
    })

def delete_page(request):
    all_entries = util.list_entries()
    return render(request, "encyclopedia/delete_page.html",{
        "all_entries": all_entries
    })

def delete_entry(request):
    if request.method == 'GET':
        title = request.GET.get('title', None)
        if title:
            # Delete the entry
            util.delete_entry(title)
            # Redirect to the index page or another appropriate page
            return HttpResponseRedirect(reverse('index'))
        else:
            # Handle case where title parameter is missing
            return render(request, "encyclopedia/error.html", {
                "message": "Title parameter is missing."
            })
    else:
        # Handle non-GET requests
        return HttpResponseNotAllowed(['GET'])