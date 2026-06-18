# Google Jobs Scraper

<a href='https://ko-fi.com/X1Y420V5V4' target='_blank'><img height='36' style='border:0px;height:36px;' src='https://storage.ko-fi.com/cdn/kofi5.png?v=6' border='0' alt='Buy Me a Coffee at ko-fi.com' /></a>

### About the project

This script fetches all the jobs from Google Careers for a specific location and saves them to a CSV file for easy filtering and analysis.

### How to Run the Program

1. Download and Install [Python 3](https://www.python.org/) (version 3.7 or higher recommended)
2. Install requirements
```bash
pip install -r requirements.txt
```
3. Run the scraper with your desired options:

```bash
# Use default location (Michigan, USA)
python scrape_google.py

# Specify a different location
python scrape_google.py --location "San Francisco, CA, USA"

# Specify both location and output file
python scrape_google.py --location "London, UK" --output "google_jobs_london.csv"

# Get help on available options
python scrape_google.py --help
```

The script will:
- Fetch all available jobs for the specified location
- Save them to the specified CSV file (default: `google_jobs.csv`)
- Show progress as it fetches each page

### Command Line Options

- `--location`: Location to search for jobs (default: "Michigan, USA")
- `--output`: Output CSV filename (default: `google_jobs.csv`)

### Finding Location Names
To get the correct location names for your search, visit the [Google Careers website](https://www.google.com/about/careers/applications/jobs) and:
1. Use the location filter in the search sidebar
2. Note the exact location names as they appear in the dropdown
3. Use these exact names when running the script

For example, if you see "New York, NY, USA" in the dropdown, use that exact format when specifying the location.

### Structure of CSV output 
The CSV file will contain the following columns:
- `job_id`: Unique identifier for the job posting
- `title`: Job title
- `location`: Job location
- `company`: Company name
- `url`: Direct link to the job posting
- `description`: Job description
- `qualifications`: Required qualifications
- `responsibilities`: Job responsibilities

### Features
- Direct API access for reliable data fetching
- CSV output for easy filtering in Excel/Google Sheets
- Progress tracking during fetching
- Rate limiting to be respectful to Google's servers
- Command-line options for location and output file

### Customization
You can modify the script to:
- Add or remove fields from the CSV output
- Add additional filtering options
- Change the default location or output filename
- Add more command-line options

### Contributing
If you'd like to contribute to the project, please fork this repository, make your changes, and submit a pull request. Feel free to report issues or suggest improvements.
