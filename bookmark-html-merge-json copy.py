import json
from bs4 import BeautifulSoup
import os
from glob import glob

"""
This Python script converts HTML bookmarks to JSON. It imports `json`, `BeautifulSoup`, `os`, and `glob`.

- `preprocess_html`: Reads HTML with various encodings, replaces non-breaking spaces.
- `extract_bookmarks`: Uses BeautifulSoup to find `<a>` tags, extracts attributes like `href`, `text`, `icon`, `add_date`, and `last_modified`.
- `convert_single_html_to_json`: Processes a single HTML file.
- `convert_directory_to_json`: Processes all HTML files in a directory.
- `write_bookmarks_to_json`: Saves bookmarks to JSON, prints counts of bookmarks, files, and folders.

The `main` function processes input as a directory or file and calls the appropriate functions. Example usage specifies source and destination paths.
"""


# Function to preprocess the HTML content
def preprocess_html(file_path):
    encodings = ['utf-8', 'iso-8859-1', 'latin1']  # Add more encodings if needed
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                html_content = file.read()
            # Replace non-breaking spaces with regular spaces
            return html_content.replace('\u00A0', ' ')
        except UnicodeDecodeError:
            continue
    raise UnicodeDecodeError(f"Unable to decode the file with the provided encodings: {file_path}")

# Function to extract bookmarks from HTML content
def extract_bookmarks(html_content):
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
    
    return bookmarks

# Function to convert a single HTML file to JSON
def convert_single_html_to_json(source_html):
    print(f"Parsing file: {source_html}")
    html_content = preprocess_html(source_html)
    # Extract bookmarks from HTML content
    return extract_bookmarks(html_content)

# Function to convert all HTML files in a directory to JSON
def convert_directory_to_json(source_dir):
    all_bookmarks = []
    
    # Iterate through all HTML files in the directory
    for html_file in glob(os.path.join(source_dir, '*.html')):
        all_bookmarks.extend(convert_single_html_to_json(html_file))
    
    return all_bookmarks

# Function to write bookmarks to a JSON file
def write_bookmarks_to_json(bookmarks, destination_json):
    # Structure the bookmarks data
    bookmarks_data = {
        "bookmarks": bookmarks
    }
    
    # Write the bookmarks data to the JSON file
    with open(destination_json, 'w', encoding='utf-8') as json_file:
        json.dump(bookmarks_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"Bookmarks saved to: {destination_json}")
    # print number of bookmarks
    print(f"Number of bookmarks: {len(bookmarks)}")
    # print number of files
    print(f"Number of files: {len(glob(os.path.join(source_html, '*.html')))}")
    # print number of folders
    print(f"Number of folders: {len(glob(os.path.join(source_html, '*/')))}")

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
    source_html = r'C:\tmp\BookmarkExports'  # Adjust this path as needed
    destination_json = r'C:\tmp\all_bookmarks.json'  # Adjust this path as needed
    main(source_html, destination_json)
