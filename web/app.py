from flask import Flask, request, render_template, send_file
import json
from bs4 import BeautifulSoup
import os
from glob import glob

app = Flask(__name__)

# Renders the index.html template, returns the rendered index.html template
@app.route('/')
def index():
    return render_template('index.html')

# Converts the source file or directory to JSON format and saves it as 'bookmarks.json',  returns the JSON file as an attachment, raises KeyError if the 'source' parameter is not provided in the request form
@app.route('/convert', methods=['POST'])
def convert():
    uploaded_files = request.files.getlist("file")
    destination = 'bookmarks.json'  # Default destination

    all_bookmarks = []

    for file in uploaded_files:
        # Save file to a temporary location
        temp_path = os.path.join("tmp", file.filename)
        file.save(temp_path)

        if temp_path.endswith('.html'):
            bookmarks = convert_single_html_to_json(temp_path)
            all_bookmarks.extend(bookmarks)
        else:
            bookmarks = convert_directory_to_json(temp_path)
            all_bookmarks.extend(bookmarks)

        os.remove(temp_path)  # Clean up the temporary file

    write_bookmarks_to_json(all_bookmarks, destination)
    return send_file(destination, as_attachment=True)


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

if __name__ == "__main__":
    app.run(debug=True)