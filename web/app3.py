from flask import Flask, render_template, request, redirect, send_file, flash, url_for
import os
import json
from bs4 import BeautifulSoup

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.secret_key = 'supersecretkey'
ALLOWED_EXTENSIONS = {'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_bookmarks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        bookmarks = []
        for link in soup.find_all('a'):
            bookmarks.append({
                'title': link.get_text(),
                'url': link.get('href')
            })
    return bookmarks

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = file.filename
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        bookmarks = parse_bookmarks(file_path)
        json_path = file_path.rsplit('.', 1)[0] + '.json'
        with open(json_path, 'w', encoding='utf-8') as json_file:
            json.dump(bookmarks, json_file, indent=4)
        return render_template('index.html', bookmarks=bookmarks, json_path=json_path)
    else:
        flash('Invalid file type')
        return redirect(request.url)

@app.route('/download/<path:filename>', methods=['GET', 'POST'])
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
