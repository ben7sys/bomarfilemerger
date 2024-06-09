import json
from bs4 import BeautifulSoup
import os
from glob import glob
import time

# Function to preprocess the HTML content
def preprocess_html(file_path):
    encodings = ['utf-8', 'iso-8859-1', 'latin1']
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                html_content = file.read()
            return html_content.replace('\u00A0', ' ')
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to decode the file with the provided encodings: {file_path}")

# Function to extract bookmarks from HTML content
def extract_bookmarks(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')
    bookmarks = []

    for index, link in enumerate(links):
        bookmark = {
            "guid": "guid_{}".format(index),
            "title": link.text,
            "index": index,
            "dateAdded": int(time.time() * 1000000),
            "lastModified": int(time.time() * 1000000),
            "id": index + 1,
            "typeCode": 1,
            "tags": "",  # Assuming no tags are available in the HTML file
            "type": "text/x-moz-place",
            "uri": link.get('href'),
            "keyword": None,
            "postData": None,
            "icon_uri": link.get('icon'),
            "last_charset": None,
            "data-important": None,
            "data-cover": None
        }
        bookmarks.append(bookmark)

    return bookmarks

# Function to convert a single HTML file to JSON
def convert_single_html_to_json(source_html):
    print(f"Parsing file: {source_html}")
    html_content = preprocess_html(source_html)
    return extract_bookmarks(html_content)

# Function to convert all HTML files in a directory to JSON
def convert_directory_to_json(source_dir):
    all_bookmarks = []

    for html_file in glob(os.path.join(source_dir, '*.html')):
        all_bookmarks.extend(convert_single_html_to_json(html_file))

    return all_bookmarks

# Function to structure the JSON data according to the specification
def structure_json_data(bookmarks):
    root = {
        "guid": "root________",
        "title": "",
        "index": 0,
        "dateAdded": 1717168173249000,
        "lastModified": 1717291888206000,
        "id": 1,
        "typeCode": 2,
        "type": "text/x-moz-place-container",
        "root": "placesRoot",
        "children": [
            {
                "guid": "menu________",
                "title": "menu",
                "index": 0,
                "dateAdded": 1717168173249000,
                "lastModified": 1717291888206000,
                "id": 2,
                "typeCode": 2,
                "type": "text/x-moz-place-container",
                "root": "bookmarksMenuFolder",
                "children": bookmarks
            },
            {
                "guid": "toolbar_____",
                "title": "toolbar",
                "index": 1,
                "dateAdded": 1717168173249000,
                "lastModified": 1717291865592000,
                "id": 3,
                "typeCode": 2,
                "type": "text/x-moz-place-container",
                "root": "toolbarFolder"
            },
            {
                "guid": "unfiled_____",
                "title": "unfiled",
                "index": 2,
                "dateAdded": 1717168173249000,
                "lastModified": 1717291860894000,
                "id": 4,
                "typeCode": 2,
                "type": "text/x-moz-place-container",
                "root": "unfiledBookmarksFolder"
            },
            {
                "guid": "mobile______",
                "title": "mobile",
                "index": 3,
                "dateAdded": 1717168173249000,
                "lastModified": 1717287731744000,
                "id": 5,
                "typeCode": 2,
                "type": "text/x-moz-place-container",
                "root": "mobileFolder"
            }
        ]
    }
    return root

# Function to write bookmarks to a JSON file
def write_bookmarks_to_json(bookmarks, destination_json):
    structured_data = structure_json_data(bookmarks)
    with open(destination_json, 'w', encoding='utf-8') as json_file:
        json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

    print(f"Bookmarks saved to: {destination_json}")
    print(f"Number of bookmarks: {len(bookmarks)}")

# Main function to handle both single file and directory input
def main(source, destination_json):
    if os.path.isdir(source):
        print(f"Processing directory: {source}")
        bookmarks = convert_directory_to_json(source)
    else:
        print(f"Processing single file: {source}")
        bookmarks = convert_single_html_to_json(source)

    write_bookmarks_to_json(bookmarks, destination_json)

# Start the script
if __name__ == "__main__":
    source_html = r'C:\tmp\Test2'  # Adjust this path as needed
    destination_json = r'C:\tmp\Test2\dev_combined.json'  # Adjust this path as needed
    main(source_html, destination_json)
