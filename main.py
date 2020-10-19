from flask import Flask, render_template, request

app = Flask("SuperScrapper")


@app.route("/")
def home():
    return render_template("potato.html")


@app.route("/report")
def report():
    # print(request.args)
    word = request.args.get("word")
    return f"this is the report {word}"


app.run(host="0.0.0.0")
