import requests
from bs4 import BeautifulSoup

LIMIT = 50


def extract_indeed_pages(url):
    indeed_result = requests.get(url)

    indeed_soup = BeautifulSoup(indeed_result.text, "html.parser")

    pagination = indeed_soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:
        pages.append(int(link.find("span").string))

    # delete last one[next] from pages
    # pages = pages[0:-1]

    max_page = pages[-1]

    return max_page


def extract_indeed_jobs(url, last_page):
    jobs_list = []
    for page in range(last_page):
        print(f"# WEB SCRAPING INDEED PAGE : {page}")
        page_url = f"{url}&start={page * LIMIT}"
        result = requests.get(page_url)
        soup = BeautifulSoup(result.text, "html.parser")
        jobs = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        # print(jobs)

        for job in jobs:
            job_info = extract_job(page_url, job)
            # print(job_info)
            jobs_list.append(job_info)

    return jobs_list


def extract_job(page_url, job_html):
    # TITLE
    title = job_html.find("h2", {"class": "title"}).find("a")["title"]

    # COMPANY
    company = job_html.find("span", {"class": "company"})
    if company == None:
        company = "None"
    else:
        company_anchor = company.find("a")
        if company_anchor != None:
            company = (company_anchor.getText()).strip()
        else:
            company = (company.getText()).strip()

    # LOCATION
    location = job_html.find("div", {"class": "recJobLoc"})["data-rc-loc"]

    # JOB_ID (detail page)
    job_id = job_html["data-jk"]
    # detail_page = f"{page_url}&vjk={job_id}"
    detail_page = f"https://www.indeed.com/viewjob?jk={job_id}"

    return {"title": title, "company": company, "location": location, "link": detail_page}


def get_jobs(search_word):
    indeed_url = f"https://www.indeed.com/jobs?q={search_word}&limit={LIMIT}"
    last_indeed_page = extract_indeed_pages(indeed_url)
    indeed_jobs = extract_indeed_jobs(indeed_url, last_indeed_page)
    return indeed_jobs
