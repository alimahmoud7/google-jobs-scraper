import requests
from selenium import webdriver

from bs4 import BeautifulSoup
from time import sleep
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver = '/media/bluehat7/Ali Only/Freelancing/google jobs scraper/chromedriver'
browser = webdriver.Chrome(executable_path=chrome_driver)

data = {}


def prepare():
    """Prepare a website url"""
    url = 'https://careers.google.com/jobs'
    params = {
        't': 'sq',
        'st': '0',
        'jlo': 'all'
    }

    result = requests.get(url, params)
    return result.url.replace('?', '#')


def parse(website):
    """Parse google jobs data"""
    browser.get(website)

    # sleep(20)
    WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'GXRRIBB-e-G'))
    )

    body = browser.page_source
    # browser.close()

    soup = BeautifulSoup(body, 'html.parser')
    jobs = soup.select('.GXRRIBB-e-G')
    print(len(jobs))
    data['total'] = len(jobs)

    jobs_urls = []
    for job in jobs:
        job_header = job.select('h2 a')[0]
        job_link = 'https://careers.google.com/jobs' + job_header.get('href')
        jobs_urls.append(job_link)

    parse_jobs(jobs_urls)


def parse_jobs(jobs_urls):
    """Parse jobs by its urls"""
    jobs = []

    for i in range(len(jobs_urls)):
        browser.execute_script("window.open('{}', 'new_window')".format(jobs_urls[i]))
        browser.switch_to.window(browser.window_handles[1])

        if i == 0:
            WebDriverWait(browser, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.secondary-text'))
            )
        else:
            WebDriverWait(browser, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.description-section p'))
            )

        jobs.append(browser.page_source)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    job_dict = {}
    jobs_arr = []
    for job in jobs:
        soup = BeautifulSoup(job, 'html.parser')
        job_id = soup.find('div', attrs={'itemtype': 'http://schema.org/JobPosting'}).get('id')
        job_title = soup.select_one('div.card-company-job-details > h1 a.title.text').get_text()
        location = soup.select_one('div.card-company-job-details .details-panel > a').get_text()

        desc = soup.select_one('div.detail-item .description-section.text.with-benefits').get_text()
        resp_qual = soup.select('div.detail-item .description-section .GXRRIBB-S-c .description-content')
        resp = resp_qual[0].get_text()
        qual = resp_qual[1].get_text()
        '''
        print(job_id)
        print(job_title)
        print(location)
        print(desc)
        print(resp)
        print(qual)
        print('\n============================================\n')
        '''
        job_dict['job_id'] = job_id
        job_dict['job_title'] = job_title
        job_dict['location'] = location
        job_dict['introduction'] = desc
        job_dict['responsibilities'] = resp
        job_dict['qualifications'] = qual
        jobs_arr.append(job_dict.copy())
        job_dict.clear()

    data['jobs'] = jobs_arr
    data_json = json.dumps(data)
    print(data_json)


if __name__ == '__main__':
    url = prepare()
    print(url)
    parse(url)

