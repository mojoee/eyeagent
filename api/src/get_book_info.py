import urllib.request
import json
import textwrap

def call_google_api(ISBN):
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    with urllib.request.urlopen(base_api_link + ISBN) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text) # deserializes decoded_text to a Python object
    volume_info = obj["items"][0]
    authors = volume_info["volumeInfo"].get("authors", "Unknown")
    pageCount = volume_info["volumeInfo"].get("pageCount", "Unknown")
    if "searchInfo" not in volume_info:
        textSnippet = ""
    else:
        textSnippet = volume_info["searchInfo"].get("textSnippet", "Unknown")

    # displays title, summary, author, domain, page count and language
    print("\nTitle:", volume_info["volumeInfo"]["title"])
    print("\nSummary:\n")
    print(textwrap.fill(textSnippet, width=65))
    print("\nAuthor(s):", ",".join(authors))
    print("\nPublic Domain:", volume_info["accessInfo"]["publicDomain"])
    print("\nPage count:", pageCount)
    print("\nLanguage:", volume_info["volumeInfo"]["language"])
    print("\n***")
    return obj