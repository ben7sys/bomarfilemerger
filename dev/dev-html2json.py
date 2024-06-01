import json
from bs4 import BeautifulSoup

# Variables for source and destination files
source_html = r'C:\tmp\BookmarkExports\2023-04-17.html'  # Source HTML file with raw string literal
destination_json = r'C:\tmp\bookmarks.json'    # Destination JSON file with raw string literal

# Function to preprocess the HTML content
def preprocess_html(html_content):
    # Replace non-breaking spaces with regular spaces
    return html_content.replace('\u00A0', ' ')

# Function to extract bookmarks and convert them to JSON
def convert_bookmarks_to_json(source_html, destination_json):
    # Read the HTML file
    with open(source_html, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Preprocess the HTML content
    html_content = preprocess_html(html_content)
    
    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Find all <A> tags which represent links/bookmarks
    links = soup.find_all('a')
    
    bookmarks = []
    
    # Extract data from each <A> tag
    for link in links:
        bookmark = {
            "url": link.get('href'),
            "description": link.text,
            "icon": link.get('icon'),
            "add_date": link.get('add_date'),
            "last_modified": link.get('last_modified', "0")  # Default to "0" if not present
        }
        bookmarks.append(bookmark)
    
    # Structure the bookmarks data
    bookmarks_data = {
        "bookmarks": bookmarks
    }
    
    # Write the bookmarks data to the JSON file
    with open(destination_json, 'w', encoding='utf-8') as json_file:
        json.dump(bookmarks_data, json_file, ensure_ascii=False, indent=4)

# Call the function to convert bookmarks
convert_bookmarks_to_json(source_html, destination_json)