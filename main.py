from flask import Flask, render_template, request, redirect, send_file, send_from_directory
from indeed import get_jobs as indeed_get_jobs
from stackoverflow import get_jobs as stackoverflow_get_jobs
from exporter import save_to_file
import os

app = Flask("SuperScrapper")

db = {}

site_list = ["indeed", "stackoverflow"]


@app.route("/")
def home():
    return render_template("index.html", site_list=site_list)


@app.route("/report")
def report():
    word = ""
    checked_list = []
    total_jobs = []
    site_len = len(site_list)
    print(request.args, site_len)
    for arg in request.args:
        if arg == "word":
            word = request.args.get("word")
            for i, site in enumerate(site_list):
                print(i, site, request.args.get(site))
                if "on" == request.args.get(site):
                    checked_list.append(site_list[i])

    print(checked_list)

    if word:
        for checked in checked_list:
            word = word.lower()
            word_key = f"{checked}:{word}"
            fromDb = db.get(word_key)
            if fromDb:
                jobs = fromDb
                db[word_key] = jobs
            else:
                # @TODO change dynamic function name
                if checked == site_list[0]:
                    jobs = indeed_get_jobs(word)
                elif checked == site_list[1]:
                    jobs = stackoverflow_get_jobs(word)
                db[word_key] = jobs
                # print(jobs)

            total_jobs += jobs
            # print(total_jobs)

    else:
        return redirect("/")
    return render_template(
        "report.html", searchingBy=word, resultNumber=len(total_jobs), jobs=total_jobs, siteList=checked_list)


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
