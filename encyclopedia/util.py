import os
import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

def change_permissions_recursive(path, mode):
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in [os.path.join(root, d) for d in dirs]:
            os.chmod(dir, mode)
    
    for file in [os.path.join(root, f) for f in files]:
            os.chmod(file, mode)
            
# change_permissions_recursive('./entries', 0o777)

def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
  
    rest = list(sorted(re.sub(r"\.md$", "", filename) 
                for filename in filenames if filename.endswith(".md")))
    return rest
    
def rand_list_entries():
    """
    Returns a random list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
    result = list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")))
    r =random.choice(result)

    try:
        f = default_storage.open(f"entries/{r}.md")
        
        return f.read().decode("utf-8")
          
    except FileNotFoundError:
        return None

def search(query):
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")
        
    result = list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")))
    for filename in result:
        fn = filename.lower()
        if query == fn:
            return fn

        if re.findall(f"{query}", fn):
            files=[]
            files.append(fn.capitalize())
            return files
                
def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        return "already_exists"
        #default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))
    return "success"
    
def edit_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown
    content. If an existing entry with the same title already exists,
    it is replaced.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        default_storage.save(filename, ContentFile(content))
        return "success"
    
def delete_entry(title):
    """
    DELETE an encyclopedia entry, given its title.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        return "deleted"
    return "already deleted"

def edit_entry_form(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        
        return f.read().decode("utf-8")
          
    except FileNotFoundError:
        return None

def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title. If no such
    entry exists, the function returns None.
    """
    try:
        f = default_storage.open(f"entries/{title}.md")
        
        return f.read().decode("utf-8")
          
    except FileNotFoundError:
        return None
