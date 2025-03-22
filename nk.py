from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException

GECKO_PATH = r"C:\tools\geckodriver.exe"
HTML_FILE = 'devops_jobs.html'

firefox_options = Options()
firefox_options.add_argument("--headless")
service = Service(GECKO_PATH)
driver = webdriver.Firefox(service=service, options=firefox_options)

def scrape_jobs():
    driver.get("https://www.naukri.com/devops-engineer-azure-devops-jobs?k=devops%2C%20devops%20engineer%2C%20azure%20devops&nignbevent_src=jobsearchDeskGNB&experience=3&jobAge=1")

    jobs = []
    seen_urls = set()  # To avoid duplicates in the current run
    required_skills = {
        'azure', 'terraform', 'prometheus', 'grafana',
        'git', 'github', 'devops', 'ci/cd', 'iac', 'pipelines', 'yaml'
    }

    page_number = 1
    while True:
        print(f"📄 Scraping Page {page_number}...")
        try:
            job_cards = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'srp-jobtuple-wrapper'))
            )
        except Exception as e:
            print(f"⚠️ Error: {e}")
            break

        for job in job_cards:
            try:
                title_element = job.find_element(By.CLASS_NAME, 'title')
                url = title_element.get_attribute('href')
                if url in seen_urls:
                    continue  # Skip duplicates within the same run

                title = title_element.text.strip()
                company = job.find_element(By.CLASS_NAME, 'comp-name').text.strip()
                description = job.find_element(By.CLASS_NAME, 'job-desc').text.strip()

                # Check if at least one of the required skills is present
                combined_text = (title + " " + description).lower()
                if not any(skill in combined_text for skill in required_skills):
                    continue

                seen_urls.add(url)
                jobs.append({
                    "Index": len(jobs) + 1,
                    "Job Title": title,
                    "Company Name": company,
                    "URL": url
                })

            except StaleElementReferenceException:
                continue

        # Pagination logic: try to click the "Next" button
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

    # Generate the HTML file with the scraped jobs
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>DevOps Jobs</title>
    <style>
        table { border-collapse: collapse; width: 100%; }
        th, td { text-align: left; padding: 8px; border: 1px solid #ddd; }
        tr:nth-child(even) { background-color: #f2f2f2; }
        /* This class changes the link color to red once clicked */
        a.clicked { color: red; }
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", function() {
            var links = document.querySelectorAll("a.job-link");
            links.forEach(function(link) {
                link.addEventListener("click", function() {
                    this.classList.add("clicked");
                });
            });
        });
    </script>
</head>
<body>
    <h1>DevOps Jobs</h1>
    <table>
        <thead>
            <tr>
                <th>Index</th>
                <th>Job Title</th>
                <th>Company Name</th>
                <th>URL</th>
            </tr>
        </thead>
        <tbody>
"""
    for job in jobs:
        html_content += f"""            <tr>
                <td>{job['Index']}</td>
                <td>{job['Job Title']}</td>
                <td>{job['Company Name']}</td>
                <td><a href="{job['URL']}" target="_blank" class="job-link">{job['URL']}</a></td>
            </tr>
"""
    html_content += """        </tbody>
    </table>
</body>
</html>"""

    with open(HTML_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML file generated: {HTML_FILE}")

if __name__ == "__main__":
    scrape_jobs()
    driver.quit()
