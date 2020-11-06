import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import json
import time

jobs = []
total = 0


def scrape(start_url):
    """Prepare a website url and scrape all pages"""

    # Scrape all pages
    start = time.time()
    count_pages = 0
    while True:
        website_url = start_url.replace('st=0', 'st={}'.format(count_pages))
        try:
            parse(website_url)
        except TimeoutException:
            browser.quit()
            print('All data successfully scraped!')
            end = time.time()
            print('Time: {} minutes \n'.format(round((end - start) / 60), 1))
            break
        count_pages += 20

    # Store all jobs and total count
    data = {
        'total': total,
        'jobs': jobs
    }
    return json.dumps(data)


def parse(jobs_page):
    """Parse main jobs page and get all jobs URLs"""
    global total

    # Open first URL
    browser.get(jobs_page)

    # Waite or sleep till all page data loaded
    WebDriverWait(browser, 20).until(
        ec.presence_of_all_elements_located((By.CLASS_NAME, 'GXRRIBB-e-G'))
    )

    body = browser.page_source

    # Parse page html to extract jobs info
    soup = BeautifulSoup(body, 'html.parser')
    jobs_content = soup.select('.GXRRIBB-e-G')

    # Store the count of jobs located in this page
    total += len(jobs_content)

    # Get all jobs links (URLs) form jobs info (jobs_content variable)
    jobs_urls = []
    for job in jobs_content:
        job_header = job.select_one('h2 a')

        # Check that the job related to Google company
        # To make sure that the html structure will be the same
        company = job.select_one(
            'div.sr-content div.summary .secondary-text').get_text()
        if company != 'DeepMind':
            job_link = 'https://careers.google.com/jobs' \
                       + job_header.get('href')
            jobs_urls.append(job_link)

    parse_jobs(jobs_urls)


def parse_jobs(jobs_urls):
    """Parse all jobs data"""
    global jobs

    # Open jobs URLs one by one to get page html
    jobs_html = []
    for url in jobs_urls:
        browser.execute_script("window.open('{}', 'new_window')".format(url))
        browser.switch_to.window(browser.window_handles[1])

        # Waite till all page data loaded
        try:
            WebDriverWait(browser, 20).until(
                ec.element_to_be_clickable((By.CSS_SELECTOR, 'a.secondary-text'))
            )
        except TimeoutException:
            browser.close()
            browser.switch_to.window(browser.window_handles[0])
            continue
        '''
        WebDriverWait(browser, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.description-section p'))
        )
        '''

        jobs_html.append(browser.page_source)

        # Close the current windows and switch to the main window
        browser.close()
        browser.switch_to.window(browser.window_handles[0])

    # Parse all pages html to get jobs data
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

        job_dict = {
            'job_id': job_id,
            'title': job_title,
            'location': location,
            'intro': desc,
            'resps': resp,
            'quals': qual
        }

        jobs_list.append(job_dict)

    # Store the current jobs list with all scraped lists before
    jobs += jobs_list


if __name__ == '__main__':
    print('Start scraping all google jobs ...')

    # Prepare the URL
    base_url = 'https://careers.google.com/jobs'
    params = {
        't': 'sq',
        'li': '20',
        'st': '0',
        'jlo': 'all'
    }
    result = requests.get(url=base_url, params=params)
    url = result.url.replace('?', '#')

    print('Please, Do not close chrome driver. '
          'It will be closed automatically after finished.')
    print('This process maybe take more than 10 minutes')

    chrome_options = webdriver.ChromeOptions()
    # Set chrome in headless mode to hide the UI
    # chrome_options.add_argument('headless')

    # Creates and open a new instance of the chrome driver
    browser = webdriver.Chrome(chrome_options=chrome_options)

    data_json = scrape(url)
    print(data_json)
    with open('data.json', 'w') as file:
        json.dump(json.loads(data_json), file)
