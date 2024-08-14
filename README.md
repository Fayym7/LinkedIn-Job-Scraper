```markdown
# LinkedIn Job Scraper

This project is a web scraper built with Python and Selenium for extracting job postings from LinkedIn. It collects job data from specified LinkedIn job search URLs and saves the information in both JSON and CSV formats.

## Features

- Scrapes job listings from LinkedIn based on provided search URLs.
- Filters job postings by 'Past 1 month' for up-to-date listings.
- Extracts detailed information including job title, company name, location, posted date, employment type, and seniority level.
- Saves the extracted data in JSON and CSV formats for further analysis.

## Requirements

- Python 3.x
- Selenium
- `webdriver_manager` for managing ChromeDriver
- Pandas
- JSON

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Fayym7/LinkedIn-Job-Scraper.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Linkedin-Job-Scraper
   ```

3. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Ensure you have the Chrome browser installed on your system.

2. Run the scraper:

   ```bash
   python scraper.py
   ```

3. The scraped job data will be saved in `linkedin_jobs.json` and `linkedin_jobs.csv` in the project directory.

### `requirements.txt`:
Ensure your `requirements.txt` file includes the necessary dependencies:

```
selenium
webdriver_manager
pandas
```
