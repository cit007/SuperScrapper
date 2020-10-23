from flask import Flask, render_template, request, redirect, send_file, send_from_directory
from scrapper import get_jobs
from exporter import save_to_file
import os

app = Flask("SuperScrapper")

db = {}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/report")
def report():
    # print(request.args)
    word = request.args.get("word")
    # print(jobs)
    if word:
        word = word.lower()
        fromDb = db.get(word)
        if fromDb:
            jobs = fromDb
            db[word] = jobs
        else:
            jobs = get_jobs(word)
            db[word] = jobs
    else:
        return redirect("/")
    return render_template(
        "report.html", searchingBy=word, resultNumber=len(jobs), jobs=jobs)


@app.route("/export")
def export():
    try:
        word = request.args.get("word")
        print(word)
        if not word:
            print(f"not exist word: {word}")
            raise Exception()

        word = word.lower()
        jobs = db.get(word)
        if not jobs:
            print("##### NOT EXIST JOB INFO FOR EXPORT #####")
            raise Exception()
        else:
            filename = f"{word}.csv"
            filepath = f"export"
            file_full_path = os.path.join(filepath, filename)

            # save file
            save_to_file(file_full_path, jobs)

            print(file_full_path)
            return send_file(file_full_path, as_attachment=True)
            # return send_from_directory(filepath, filename, as_attachment=True)

    except:
        print("##### EXPORT EXCEPTION #####")
        return redirect("/")


app.run(host="0.0.0.0")
