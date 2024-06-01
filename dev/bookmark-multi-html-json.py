import json
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

source_folder = os.getenv('SOURCE_FOLDER')
destination_json = os.getenv('DESTINATION_JSON')

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
    soup = BeautifulSoup(html_content, 'html.parser')
    bookmarks = []

    current_folder = []
    
    for element in soup.recursiveChildGenerator():
        if element.name == 'h3':
            # This is a folder
            folder_name = element.get_text(strip=True)
            current_folder.append(folder_name)
            print(f"Entering folder: {'/'.join(current_folder)}")
        elif element.name == 'a':
            # This is a bookmark
            bookmark = {
                "url": element.get('href'),
                "description": element.get_text(strip=True),
                "icon": element.get('icon'),
                "add_date": element.get('add_date'),
                "last_modified": element.get('last_modified', "0"),
                "data_important": element.get('data-important'),
                "data_cover": element.get('data-cover'),
                "tags": element.get('tags'),
                "icon_uri": element.get('icon_uri'),
                "last_charset": element.get('last_charset'),
                "folder": '/'.join(current_folder)
            }
            print(f"Adding bookmark: {bookmark}")
            bookmarks.append(bookmark)
        elif element.name == 'dl':
            continue
        elif element.name == 'dt':
            continue
        elif element.name == 'p':
            if element.find_previous_sibling('h3'):
                # This is the end of a folder section
                if current_folder:
                    exited_folder = current_folder.pop()
                    print(f"Exiting folder: {exited_folder}")
            continue
        elif element.name is None:
            # This is likely text inside tags we are not interested in
            continue
        else:
            print(f"Unexpected tag: {element.name}")

    return bookmarks

# Function to convert a single HTML file to JSON
def convert_single_html_to_json(source_html):
    print(f"Parsing file: {source_html}")
    html_content = preprocess_html(source_html)
    # Extract bookmarks from HTML content
    bookmarks = extract_bookmarks(html_content)
    
    # Debugging: Print extracted bookmarks before writing to JSON
    #print(f"Extracted {len(bookmarks)} bookmarks:")
    #for bookmark in bookmarks:
    #    print(bookmark)
    
    return bookmarks

# Main function to process all HTML files in a folder
def process_folder(source_folder, destination_json):
    all_bookmarks = []

    # Iterate over all files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith('.html'):
            file_path = os.path.join(source_folder, filename)
            bookmarks = convert_single_html_to_json(file_path)
            all_bookmarks.extend(bookmarks)
    
    # Structure the bookmarks data
    bookmarks_data = {
        "bookmarks": all_bookmarks
    }
    
    # Write the bookmarks data to the JSON file
    with open(destination_json, 'w', encoding='utf-8') as json_file:
        json.dump(bookmarks_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"All bookmarks saved to: {destination_json}")
    print(f"Total number of bookmarks: {len(all_bookmarks)}")

# Example usage
if __name__ == "__main__":
    #source_folder = r'C:\tmp\BookmarkExports'  # Adjust this path as needed
    #destination_json = r'C:\tmp\all_bookmarks.json'  # Adjust this path as needed
    process_folder(source_folder, destination_json)
