from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import os
import json
from bs4 import BeautifulSoup
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'html'}
app.config['JSON_FOLDER'] = 'json_files'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

if not os.path.exists(app.config['JSON_FOLDER']):
    os.makedirs(app.config['JSON_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
        elif element.name == None:
            # This is likely text inside tags we are not interested in
            continue
        else:
            print(f"Unexpected tag: {element.name}")

    return bookmarks

# Function to convert a single HTML file to JSON
def convert_html_to_json(source_html, destination_json):
    html_content = preprocess_html(source_html)
    # Extract bookmarks from HTML content
    bookmarks = extract_bookmarks(html_content)
    
    # Structure the bookmarks data
    bookmarks_data = {
        "bookmarks": bookmarks
    }
    
    # Write the bookmarks data to the JSON file
    with open(destination_json, 'w', encoding='utf-8') as json_file:
        json.dump(bookmarks_data, json_file, ensure_ascii=False, indent=4)
    
    return len(bookmarks), bookmarks_data

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            html_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(html_path)
            json_filename = f"{os.path.splitext(filename)[0]}.json"
            json_path = os.path.join(app.config['JSON_FOLDER'], json_filename)
            try:
                num_bookmarks, bookmarks_data = convert_html_to_json(html_path, json_path)
                flash(f'Successfully converted {num_bookmarks} bookmarks')
                return render_template('upload.html', num_bookmarks=num_bookmarks, success=True, log=bookmarks_data)
            except Exception as e:
                flash(f'Failed to convert file: {str(e)}')
                return render_template('upload.html', success=False, error=str(e))
    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['JSON_FOLDER'], filename), as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
