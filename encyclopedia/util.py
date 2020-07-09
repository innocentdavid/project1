import re
import random

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    _, filenames = default_storage.listdir("entries")

    for filename in filenames:
        if filename.endswith(".md"):
            res = list(sorted(re.sub(r"\.md$", "", filename)))
            #print(res)
  
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

def q_entry(query):
    """
    Returns a list of all names of encyclopedia entries.
    """
    query = query.lower()
    _, filenames = default_storage.listdir("entries")
        
    result = list(sorted(re.sub(r"\.md$", "", filename) for filename in filenames if filename.endswith(".md")))
    
    files=[]
    for filename in result:
        if query == filename:
            return filename
        if re.findall(f"{query}", filename):
            t=filename
            files.append(t)
    #print(files)
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
    
def delete_entry(title):
    """
    DELETE an encyclopedia entry, given its title.
    """
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
        return "deleted"
    return "already deleted"


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
