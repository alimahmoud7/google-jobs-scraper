import requests
from selenium import webdriver

from bs4 import BeautifulSoup
from time import sleep
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

chrome_driver = '/media/bluehat7/Ali Only/Freelancing/google jobs scraper/chromedriver'
browser = webdriver.Chrome(executable_path=chrome_driver)

data = {}
jobs = []
total = 0


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
    global total
    browser.get(website)

    # sleep(20)
    WebDriverWait(browser, 30).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, 'GXRRIBB-e-G'))
    )

    body = browser.page_source
    # browser.close()

    soup = BeautifulSoup(body, 'html.parser')
    jobs_content = soup.select('.GXRRIBB-e-G')
    print(len(jobs_content))
    total += len(jobs_content)

    jobs_urls = []
    for job in jobs_content:
        job_header = job.select('h2 a')[0]
        google = job.select_one('div.sr-content div.summary .secondary-text').get_text()
        if google == 'Google':
            job_link = 'https://careers.google.com/jobs' + job_header.get('href')
            jobs_urls.append(job_link)

    parse_jobs(jobs_urls)


def parse_jobs(jobs_urls):
    """Parse jobs by its urls"""
    global jobs
    jobs_html = []

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

        jobs_html.append(browser.page_source)
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    job_dict = {}
    jobs_list = []
    for job in jobs_html:
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
        jobs_list.append(job_dict.copy())
        job_dict.clear()

    jobs += jobs_list


if __name__ == '__main__':

    # Scrape all pages
    count_pages = 0
    while True:
        print(count_pages)
        url = prepare()
        url = url.replace('st=0', 'st={}'.format(count_pages))
        print(url)
        try:
            parse(url)
        except TimeoutException:
            browser.close()
            break

        count_pages += 20

    browser.close()
    data['total'] = total
    data['jobs'] = jobs
    data_json = json.dumps(data)
    print(data_json)

