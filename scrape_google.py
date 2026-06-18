import requests
import json
import csv
import argparse
from urllib.parse import urlencode
import time

def get_jobs(location):
    """Get all jobs from Google Careers API for a specific location"""
    base_url = "https://careers.google.com/api/v3/search/"
    
    # Prepare the parameters
    params = {
        "location": location,
        "page": 1,
        "page_size": 20,
        "sort_by": "relevance"
    }
    
    jobs = []
    page = 1
    
    while True:
        # Update page number
        params["page"] = page
        
        # Make the request
        url = f"{base_url}?{urlencode(params)}"
        print(f"Fetching page {page}...")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://careers.google.com/jobs/results/"
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response: {response.text}")
            break
            
        try:
            data = response.json()
            job_listings = data.get("jobs", [])
            
            if not job_listings:
                print("No more jobs found.")
                break
                
            for job in job_listings:
                jobs.append({
                    'job_id': job.get("id"),
                    'title': job.get("title"),
                    'location': job.get("location"),
                    'company': job.get("company"),
                    'url': f"https://careers.google.com/jobs/results/{job.get('id')}",
                    'description': job.get("description", ""),
                    'qualifications': job.get("qualifications", ""),
                    'responsibilities': job.get("responsibilities", "")
                })
                
            print(f"Found {len(job_listings)} jobs on page {page}")
            page += 1
            time.sleep(1)  # Be nice to the server
            
        except json.JSONDecodeError:
            print("Error parsing JSON response")
            print(f"Response: {response.text}")
            break
            
    return jobs

def save_to_csv(jobs, filename='google_jobs.csv'):
    """Save jobs to a CSV file"""
    if not jobs:
        print("No jobs to save.")
        return
        
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=jobs[0].keys())
        writer.writeheader()
        writer.writerows(jobs)
    print(f"Saved {len(jobs)} jobs to {filename}")

if __name__ == '__main__':
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Fetch Google jobs for a specific location')
    parser.add_argument('--location', type=str, default="Michigan, USA",
                      help='Location to search for jobs (default: "Michigan, USA")')
    parser.add_argument('--output', type=str, default='google_jobs.csv',
                      help='Output CSV filename (default: google_jobs.csv)')
    
    args = parser.parse_args()
    
    print(f"Starting Google Jobs scraper for location: {args.location}")
    jobs = get_jobs(args.location)
    save_to_csv(jobs, args.output)
    print("Done!")
