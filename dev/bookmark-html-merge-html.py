# source_folder = 'C:\tmp\BookmarkExports'
# output_file = 'C:\tmp\BookmarkMerged.html'

## Script funktioniert NOCH NICHT
## Aktuelles Problem: Die Output-Datei wird zwar erstellt, enthält aber nur 2 Zeilen (DOCTYPE NETSCAPE, HTML, Title)

import os
from bs4 import BeautifulSoup
import logging

def setup_logging(log_file):
    """
    Sets up the logging configuration.
    
    Parameters:
    log_file (str): The path to the log file.
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def extract_bookmarks_from_html(html_file):
    """
    Extracts the bookmarks section from an HTML file.
    
    Parameters:
    html_file (str): The path to the HTML file.
    
    Returns:
    BeautifulSoup: A BeautifulSoup object containing the bookmarks section, or None if an error occurs.
    """
    try:
        with open(html_file, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
        # Assuming the bookmarks are within the first <DL> tag inside the <body>
        bookmarks_section = soup.find('dl')
        return bookmarks_section
    except Exception as e:
        logging.error(f"Error extracting bookmarks from {html_file}: {e}")
        return None

def merge_bookmarks_html(source_folder, output_file):
    """
    Merges bookmarks from multiple HTML files into a single HTML file.
    
    Parameters:
    source_folder (str): The path to the folder containing the source HTML files.
    output_file (str): The path to the output HTML file.
    """
    logging.info("Starting the merging process.")
    all_bookmarks = BeautifulSoup(
        '<!DOCTYPE NETSCAPE-Bookmark-file-1>'
        '<HTML>'
        '<HEAD>'
        '<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">'
        '<TITLE>Bookmarks</TITLE>'
        '</HEAD>'
        '<BODY><H1>Bookmarks</H1><DL></DL></BODY>'
        '</HTML>',
        'html.parser'
    )
    body = all_bookmarks.find('body')
    main_dl = body.find('dl')

    for root, dirs, files in os.walk(source_folder):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                logging.info(f"Processing file: {file_path}")
                bookmarks_section = extract_bookmarks_from_html(file_path)
                if bookmarks_section:
                    for child in bookmarks_section.find_all(['dt', 'dl']):
                        main_dl.append(child)
                else:
                    logging.error(f"Failed to process file: {file_path}")

    try:
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(all_bookmarks))
        logging.info(f"Bookmarks merged successfully into {output_file}")
    except Exception as e:
        logging.error(f"Error writing to output file {output_file}: {e}")

# Setup logging
log_file = 'merge_bookmarks.log'
setup_logging(log_file)

# Define the source folder and output file paths
source_folder = 'C:\tmp\BookmarkExports'
output_file = os.path.join('C:', 'tmp', 'BookmarkMerged.html')

# Call the function to merge bookmarks
merge_bookmarks_html(source_folder, output_file)
