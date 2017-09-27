# Google Jobs Scraper

### About the project
>> Simply, The script scrapes all the jobs from all the pages (first to final available page) located on [https://careers.google.com/jobs](https://careers.google.com/jobs#t=sq&li=20&st=0&jlo=all) and return the result as a JSON string, Then you will have a JSON file contains all scraped data.

### How to Run the Program

1. Download and Install [Python 3](https://www.python.org/)
2. Install requirements
```
pip install requests beautifulsoup4 selenium
```
3. Download [Chrome Driver](https://sites.google.com/a/chromium.org/chromedriver/downloads) for your OS
4. Edit `scrape_google.py` file to change the path of chrome driver
```
# Path of chrome driver
chrome_driver = 'path/to/chromedriver'
```
5. Finally, Run `scrape_google.py`
```
python scrape_google.py
```

**Note:** For Windows users, Please check [this video](https://drive.google.com/open?id=0BzTpKjilS_t0WU5sOGV3TS01d0U)

### Structure of JSON output 
```
{
  "total": "total_count",
  "jobs": [
    {
      "job_id": "id1",
      "title": "title1",
      "location": "location1", 
      "intro": "introduction1", 
      "resps": "responsibilities1",
      "quals": "qualifications1"
    },
    {
      "job_id": "id2",
      "title": "title2",
      "location": "location2", 
      "intro": "introduction2", 
      "resps": "responsibilities2",
      "quals": "qualifications2"
    },
    ...
  ]
}
```

