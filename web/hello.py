# Startet einen Webserver auf Port 5000 und gibt bei einem GET-Request "Hello World!" zurück
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()