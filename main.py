from flask import Flask, render_template, request, redirect, send_file, send_from_directory
from indeed import get_jobs as indeed_get_jobs
from stackoverflow import get_jobs as stackoverflow_get_jobs
from exporter import save_to_file
from config import config
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
    export_param = ""

    word = request.args.get("word")
    maxPage = request.args.get("maximum")

    # ----- set maximum page of config from input-------
    config.max = maxPage
    print(f"input maximum page ..... {config.max}")

    for i, site in enumerate(site_list):
        print(i, site, request.args.get(site))
        if "on" == request.args.get(site):
            checked_list.append(site_list[i])

    print(checked_list)

    if word:
        for checked in checked_list:
            word = word.lower()

            word_key = f"{checked}:{word}:{maxPage}"
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

        for checked in checked_list:
            export_param += f"&{checked}=on"
        export_param += f"&maximum={maxPage}"
        print(export_param)

    else:
        return redirect("/")
    return render_template(
        "report.html", searchingBy=word, resultNumber=len(total_jobs), jobs=total_jobs, siteList=checked_list, exportParam=export_param)


@app.route("/export")
def export():
    try:
        checked_list = []
        total_jobs = []

        print(f"export.....{request.args}")
        word = request.args.get("word")
        maxPage = request.args.get("maximum")
        if not word:
            print(f"not exist word: {word}")
            raise Exception()

        for i, site in enumerate(site_list):
            print(i, site, request.args.get(site))
            if "on" == request.args.get(site):
                checked_list.append(site_list[i])

        for checked in checked_list:
            word = word.lower()
            word_key = f"{checked}:{word}:{maxPage}"
            jobs = db.get(word_key)

            total_jobs += jobs

        if not total_jobs:
            print("##### NOT EXIST JOB INFO FOR EXPORT #####")
            raise Exception()
        else:
            filename = f"{word}.csv"
            filepath = f"export"
            file_full_path = os.path.join(filepath, filename)

            # save file
            save_to_file(file_full_path, total_jobs)

            # print(file_full_path)
            return send_file(file_full_path, as_attachment=True)
            # return send_from_directory(filepath, filename, as_attachment=True)

    except:
        print("##### EXPORT EXCEPTION #####")
        return redirect("/")


app.run(host="0.0.0.0")
