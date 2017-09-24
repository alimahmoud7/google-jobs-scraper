import requests
from selenium import webdriver

from bs4 import BeautifulSoup
from time import sleep
from pprint import pprint
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_driver = '/media/bluehat7/Ali Only/Freelancing/google jobs scraper/chromedriver'
browser = webdriver.Chrome(executable_path=chrome_driver)


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

    job_json = {}
    data = []
    jobs_urls = []
    for job in jobs:
        job_id = job.get('id')
        job_header = job.select('h2 a')[0]
        job_title = job_header.get('title')
        job_link = 'https://careers.google.com/jobs' + job_header.get('href')
        print(job_link)
        jobs_urls.append(job_link)
        # print(job_title)
        job_json['job_id'] = job_id
        job_json['job_title'] = job_title
        data.append(job_json.copy())
        job_json.clear()

    parse_jobs(jobs_urls)
    print(data)


def parse_jobs(jobs_urls):
    """Parse jobs by its urls"""
    jobs = []

    for link in jobs_urls:
        # browser.execute_script('''window.open("{}","_blank");'''.format(jobs_urls[0]))
        browser.execute_script("window.open('{}', 'new_window')".format(link))
        browser.switch_to.window(browser.window_handles[1])

        WebDriverWait(browser, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.description-section p'))
        )

        jobs.append(browser.page_source)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    for job in jobs:
        soup = BeautifulSoup(job, 'html.parser')
        job_id = soup.find('div', attrs={'itemtype': 'http://schema.org/JobPosting'}).get('id')
        title = soup.select_one('div.card-company-job-details > h1 a.title.text').get_text()
        location = soup.select_one('div.card-company-job-details .details-panel > a').get_text()

        '''
        if not title or not location:
            browser.get(jobs_urls[i])
            WebDriverWait(browser, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a.secondary-text'))
            )
            re_job = browser.page_source
            browser.close()
            soup = BeautifulSoup(re_job, 'html.parser')
            title = soup.select_one('div.card-company-job-details > h1 a.title.text').get_text()
            location = soup.select_one('div.card-company-job-details .details-panel > a').get_text()
        '''

        desc = soup.select_one('div.detail-item .description-section.text.with-benefits').get_text()
        resp_qual = soup.select('div.detail-item .description-section .GXRRIBB-S-c .description-content')
        resp = resp_qual[0].get_text()
        qual = resp_qual[1].get_text()
        print(job_id)
        print(title)
        print(location)
        print(desc)
        print(resp)
        print(qual)
        print('\n============================================\n')


if __name__ == '__main__':
    url = prepare()
    print(url)
    parse(url)

