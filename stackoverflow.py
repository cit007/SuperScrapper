import requests
from bs4 import BeautifulSoup


def get_last_page(so_url):
    result = requests.get(so_url)
    so_soup = BeautifulSoup(result.text, "html.parser")
    pages = so_soup.find(
        "div", {"class": "s-pagination"}).find_all("a")
    # print(pages)

    # last page number
    last_page = pages[-2].get_text(strip=True)
    # print(last_page)
    return int(last_page)


def extract_jobs(so_url, last_page):
    jobs_list = []
    for page in range(last_page):
        print(f"# WEB SCRAPING SO PAGE : {page}")
        result = requests.get(so_url, {"pg": page+1})
        # print(result.text)
        soup = BeautifulSoup(result.text, "html.parser")
        jobs = soup.find_all("div", {"class": "-job"})
        # print(jobs)
        for job in jobs:
            job_info = extract_job(job)
            jobs_list.append(job_info)

    return jobs_list


def extract_job(job_html):
    # TITLE
    title = job_html.find("a", {"class": "s-link"})["title"]
    # print(title)

    # COMPANY
    company = job_html.find(
        "h3", {"class": "fc-black-700"}).find("span").getText(strip=True)
    # print(company)

    # LOCATION
    location = job_html.find(
        "h3", {"class": "fc-black-700"}).find("span", {"class": "fc-black-500"}).getText(strip=True)
    # print(location)

    # USEFUL NICO LEC
    # company, location = job_html.find(
    #     "h3", {"class": "fc-black-700"}).find_all("span", recursive=False)
    # print(company.getText(strip=True), location.getText(strip=True))

    # JOB_ID (detail page)
    job_id = job_html["data-jobid"]
    detail_page = f"https://stackoverflow.com/jobs/{job_id}"
    # print(job_id, detail_page)
    return {"site": "stackoverflow", "title": title, "company": company, "location": location, "link": detail_page}


def get_jobs(search_word):
    url = f"https://stackoverflow.com/jobs?q={search_word}"
    last_page = get_last_page(url)
    jobs_list = extract_jobs(url, last_page)
    return jobs_list
