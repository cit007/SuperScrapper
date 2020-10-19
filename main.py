from flask import Flask

app = Flask("SuperScrapper")


@app.route("/")
def home():
    return "Hello!"


@app.route("/contact")
def contact():
    return "Contact me!"


app.run(host="0.0.0.0")
