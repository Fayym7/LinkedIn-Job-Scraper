# Libraries
import time
import pandas as pd
import json   
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
from selenium.webdriver.chrome.service import Service
from urllib.parse import urlparse, parse_qs

# Function to extract job data from a given LinkedIn URL
def get_job_data(url):
    driver.get(url)                                   #Initializing the webpage based on the URL
    time.sleep(2)
    print('Entering jobs one by one')
    job_listings = []
    try: 
        # Wait until the jobs list block is fully loaded
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'jobs-search__results-list'))
        )
        # Click on the 'Date Posted' filter and select 'Past 1 week'
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form[1]/ul/li[2]/div/div/button'))
        ).click()  
        time.sleep(0.5)                                # Slight delay to ensure the filter is applied
        driver.find_element(By.ID, 'f_TPR-2').click()  # Select 'Past 1 week' option
        time.sleep(0.5)
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable(driver.find_element(By.XPATH, '/html/body/div[1]/section/div/div/div/form[1]/ul/li[2]/div/div/div/button'))
        ).click()                                      # Apply the selected filter
        time.sleep(3)                                  # Wait for the page to refresh with filtered results

        # Get the list of job postings
        jobs_block = driver.find_element(By.CLASS_NAME,'jobs-search__results-list')
        jobs_list = jobs_block.find_elements(By.TAG_NAME, 'li')

        for j, job in enumerate(jobs_list, start=1):
            if j > 50:                                  # Limit to the first 50 jobs for demonstration
                break
            try:
                # Click on the job link to load the details
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable(job.find_element(By.TAG_NAME, 'a'))
                ).click()
                time.sleep(2)                            # Allow time for the job details to load

                # Wait until the job details content is fully loaded
                content = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'details-pane__content'))
                )
                time.sleep(3)                            # Additional wait to ensure all job details are visible

                # Initialize job details variables
                job_title = ''
                try:
                    # Get the job title
                    job_title = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.TAG_NAME, "h2"))
                    ).text
                except Exception as e:
                    print(f"Failed to retrieve job title: {e}")

                # Initialize company details variables
                company_name = ''
                location = ''
                days = ''
                seniority_level = ''
                employment_type = ''
                posted_date = ''
                try:
                    # Get the company name
                    company_name = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, "topcard__org-name-link"))
                    ).text
                except Exception as e:
                    print(f"Failed to retrieve company name: {e}")
                
                try:
                    # Get the job location
                    location = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'topcard__flavor--bullet'))
                    ).text
                except Exception as e:
                    print(f"Failed to retrieve location: {e}")

                try:
                    # Get the posted time
                    days = WebDriverWait(driver, 20).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'posted-time-ago__text'))
                    ).text
                except Exception as e:
                    print(f"Failed to retrieve posted time: {e}")
                    
                # Calculate the actual posted date based on 'days ago' information
                days_ago = 0
                if 'day' in days:
                    days_ago = int(days.split(' ')[0])
                elif 'week' in days:
                    days_ago = int(days.split(' ')[0]) * 7
                posted_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime('%d-%m-%Y')
                # Get seniority level and employment type
                try:
                    seniority_level = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'description__job-criteria-text'))
                    )[0].text
                except Exception as e:
                    print(f"Failed to retrieve seniority level: {e}")
                    
                try:
                    employment_type = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'description__job-criteria-text'))
                    )[1].text
                except Exception as e:
                    print(f"Failed to retrieve employment type: {e}")
                current_url = driver.current_url
                parsed_url = urlparse(current_url)
                query_params = parse_qs(parsed_url.query)                      # Extract query parameters
                current_job_id = query_params.get('currentJobId', [None])[0]   # Get the value of 'currentJobId'
                job_listings.append({                                          # Append the job details to the list
                    "company": company_name,
                    "job_title": job_title,
                    "linkedin_job_id": current_job_id,
                    "location": location,
                    "posted_on": days,
                    "posted_date": posted_date,
                    "employment_type": employment_type,  
                    "seniority_level": seniority_level
                })
                
            except Exception as e:
                print(f"An error occurred with job {j}: {e}")
            
            driver.execute_script("arguments[0].scrollIntoView();", job)        # Scroll down to the next job element to ensure it is in view
            time.sleep(1)                                                       # Give time for scrolling effect to complete
    except Exception as e:
        print(f"An overall error occurred: {e}")

    return job_listings


urls = [
    # List of LinkedIn job search URLs to scrape
    'https://www.linkedin.com/jobs/search?location=India&geoId=102713980&f_C=1035&position=1&pageNum=0',
    'https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_C=1441',
    'https://www.linkedin.com/jobs/search?keywords=&location=India&geoId=102713980&f_TPR=r86400&f_C=1586&position=1&pageNum=0'
]

# Initialize Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window() 
driver.switch_to.window(driver.current_window_handle)
driver.implicitly_wait(10)                                                       # Implicit wait to manage dynamic content loading

all_jobs = []
for url in urls:
    all_jobs.extend(get_job_data(url))                                           # Scrape job data for each URL

# Close the WebDriver instance after scraping
driver.quit()

# Save the scraped job data in JSON format
with open('linkedin_jobs.json', 'w') as f:
    json.dump(all_jobs, f, indent=4)

# Save the scraped job data in CSV format
df = pd.DataFrame(all_jobs)
df.to_csv('linkedin_jobs.csv', index=False)

print(all_jobs)

