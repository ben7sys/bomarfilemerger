# bomarfilemerger

 - Mehrere HTML Dateien von verschiedenen Browsern in einem Ordner
 - Alle Bookmarks in eine HTML-Datei konsolidieren

## Plan
1. Stelle sicher, dass alle Bookmarks HTML Dateien in einem Ordner zu einer Datei zusammengeführt werden
    - Beispiel: Ein Ordner mit Bookmarks von verschiedenen Browsern, verschiedene Erstellungszeiträume, mehrere 100 Stück. 
    - Führe alle Bookmark-HTML-Dateien in eine einzige HTML-Datei zusammen.

2. Erstelle ein Script, denke Schritt für Schritt.
    - Berücksichtige dass der Quellordner auch Unterordner haben könnte in denen sich .html-Dateien befinden
    - Der Quell und Zielname soll als Variable im Script definiert werden können

3. überprüfe das Skript auf Fehler, versuche sinnvolle Verbesserungen und Ergänzungen zu finden.

4. Implementiere ein Fehlerbehandlungssystem mit Konsolen Ausgabe

## Usage

git clone
create and activate conda/venv
pip install beautifulsoup4

### bookmark-html-merge-html
Bookmark HTML liest alle HTML Dateien aus einem Pfad verbindet Sie zu einer HTML Datei.
```
python bookmark-html-merge-html
```


python bookmarkfilemerger.py /pfad/zum/quellordner /pfad/zur/ziel/datei.html


# Weitere Ideen:
Bookmarks sollen automatisch sortiert, beschriftet, beschrieben, getaggt werden (powered bei LLM)

1. Bookmarks werden aus einer Datei extrahiert
    - zu Beachten: die HTML dateien enthalten Daten wie Beschriftung/Beschreibung/Notizen
2. Bookmarks werden in ein ein file oder db geschrieben: (noch unsicher) nosql/json/yaml
3. Duplikate werden entfernt
4. Einzelne Bookmarks können an ein LLM gesendet werden für Tagging und verbessern von Beschriftung/Beschreibung/Notizen
