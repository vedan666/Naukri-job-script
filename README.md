```markdown
# Naukri DevOps Jobs Scraper 🚀

A Python script to scrape DevOps-related job listings from Naukri.com with advanced filtering for skills like Azure, Terraform, Prometheus, and more. Perfect for job hunters targeting DevOps roles!

---

## Features ✨
- **Headless Browsing**: Uses Selenium with Firefox in headless mode for faster scraping.
- **Duplicate Prevention**: Skips already scraped jobs using a CSV tracker.
- **Skill-Based Filtering**: Targets jobs requiring skills like `Azure`, `Terraform`, `CI/CD`, and more.
- **Pagination Support**: Automatically navigates through all available pages.
- **CSV Export**: Saves results to `devops_jobs.csv` with details like Job Title, Company, and URL.

---

## Prerequisites 📋
- Python 3.x
- [Geckodriver](https://github.com/mozilla/geckodriver/releases) (for Selenium/Firefox)
- Libraries: `selenium`, `csv`

---

## Installation 🛠️

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/naukri-devops-scraper.git
   cd naukri-devops-scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install selenium
   ```

3. **Set up Geckodriver**:
   - Download `geckodriver.exe` from [here](https://github.com/mozilla/geckodriver/releases).
   - Place it in `C:\tools\` (default path) **OR** update the `GECKO_PATH` variable in `nk.py` with your path.

---

## Usage 🖥️

1. Run the script:
   ```bash
   python nk.py
   ```
2. Check the output file `devops_jobs.csv` for results.

**Sample Output**:
```
Index,Job Title,Company Name,URL
1,"Senior DevOps Engineer",TechCorp,https://naukri.com/job1
2,"Cloud Infrastructure Engineer",CloudWorks,https://naukri.com/job2
```

---

## Customization 🔧

1. **Modify Skills Filter**:
   - Edit the `required_skills` set in `nk.py`:
   ```python
   required_skills = {'aws', 'docker', 'kubernetes'}  # Add/remove skills
   ```

2. **Change Target URL**:
   - Update the URL in `scrape_jobs()` to scrape different roles:
   ```python
   driver.get("https://naukri.com/your-custom-search-url")
   ```

---

## Limitations ⚠️
- Website structure changes on Naukri.com may break the script.
- Headless browsers might be detected and blocked by some sites.
- Rate limiting or IP blocking possible if used aggressively.

---

## Contributing 🤝

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/new-feature`.
3. Commit changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature/new-feature`.
5. Open a Pull Request.

---

## License 📄

MIT License. Feel free to use, modify, and distribute!  
**Disclaimer**: Use this script responsibly. Respect website terms of service and robots.txt rules.
``` 

---

**Pro Tip** 🔥: Run the script daily with a scheduler (e.g., `cron`) to keep your job list updated!