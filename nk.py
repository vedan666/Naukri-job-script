from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
import csv
import os

# Path to the GeckoDriver executable
GECKO_PATH = r"C:\tools\geckodriver.exe"

# CSV file to store job data and the columns for the CSV file
CSV_FILE = 'devops_jobs.csv'
COLUMNS = ["Index", "Job Title", "Company Name", "URL"]

# Configure Firefox options to run in headless mode
firefox_options = Options()
firefox_options.add_argument("--headless")

# Create a service object with the GeckoDriver executable
service = Service(GECKO_PATH)

# Initialize the Firefox WebDriver with the specified service and options
driver = webdriver.Firefox(service=service, options=firefox_options)

def scrape_jobs():
    # URL of the Naukri page to scrape
    driver.get("your_naukri_url_here")

    # Read existing data from the CSV file to avoid duplicates
    existing_urls = set()
    last_index = 0
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_urls.add(row['URL'])
                last_index = int(row['Index'])

    # List to store new job entries
    jobs = []

    # Set of required skills to filter jobs
    required_skills = {'azure', 'terraform', 'prometheus', 'grafana', 'git', 'github', 'devops', 'ci/cd', 'iac', 'pipelines', 'yaml'}

    page_number = 1
    while True:
        print(f"📄 Scraping Page {page_number}...")
        try:
            # Wait for job cards to load on the page
            job_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'srp-jobtuple-wrapper'))
            )
        except Exception as e:
            print(f"⚠️ Error: {e}")
            break

        for job in job_cards:
            try:
                # Extract job URL
                title_element = job.find_element(By.CLASS_NAME, 'title')
                url = title_element.get_attribute('href')
                if url in existing_urls:
                    continue  # Skip duplicates

                # Extract basic job information
                title = title_element.text.strip()
                company = job.find_element(By.CLASS_NAME, 'comp-name').text.strip()
                description = job.find_element(By.CLASS_NAME, 'job-desc').text.strip()

                # Check if job description contains any required skills
                combined_text = (title + " " + description).lower()
                if not any(skill in combined_text for skill in required_skills):
                    continue

                # Add the job to the jobs list
                last_index += 1
                jobs.append({
                    "Index": last_index,
                    "Job Title": title,
                    "Company Name": company,
                    "URL": url
                })
                existing_urls.add(url)  # Prevent duplicates in current run

            except StaleElementReferenceException:
                continue

        # Pagination logic to go to the next page
        try:
            next_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//span[text()='Next']"))
            )
            driver.execute_script("arguments[0].click();", next_button)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'srp-jobtuple-wrapper'))
            )
            page_number += 1
        except (NoSuchElementException, TimeoutException):
            print("🚫 No more pages.")
            break

    # Write the collected job data to the CSV file (append if file exists)
    mode = 'a' if os.path.exists(CSV_FILE) else 'w'
    with open(CSV_FILE, mode, newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        if mode == 'w':
            writer.writeheader()
        writer.writerows(jobs)

    print(f"✅ Added {len(jobs)} new jobs. Total jobs: {last_index}")

if __name__ == "__main__":
    scrape_jobs()
    driver.quit()
