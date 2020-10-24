import csv


def save_to_file(file_full_path, jobs):
    file = open(file_full_path, mode="w")
    writer = csv.writer(file)
    writer.writerow(["site", "title", "company", "location", "link"])
    for job in jobs:
        writer.writerow(list(job.values()))
    print(file)
