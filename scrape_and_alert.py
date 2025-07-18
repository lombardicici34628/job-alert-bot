import os
import pandas as pd
from jobspy import scrape_jobs
import requests

def send_telegram_message(message):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}
    requests.post(url, data=payload)


search_terms = [
    "QA Automation Engineer", "Test Automation Engineer", "Automation Test Engineer",
    "SDET", "SDET – Java", "QA SDET", "Automation SDET",
    "Senior QA Engineer", "Sr. QA Analyst", "Senior Test Engineer",
    "Test Analyst", "QA Analyst – Automation", "Functional & Automation QA",
    "QA Engineer – Selenium/Java", "Selenium Tester", "Java QA Engineer"
]
search_query = "|".join(search_terms)
site_names = ["indeed", "linkedin"]

locations = "Hyderabad"

jobs = scrape_jobs(
    site_name=site_names,
    search_term=search_query,
    location=locations,
    results_wanted=20,
    hours_old=24,
    country_indeed="India"
)

print("🧪 Columns available:", list(jobs.columns))
print("🧪 Number of jobs scraped:", len(jobs))

expected_columns = ["title", "company", "location", "job_url"]

if jobs.empty or not all(col in jobs.columns for col in expected_columns):
    print("❌ Job data is missing or malformed.")
    send_telegram_message("🤖 Bot ran but no valid job data was retrieved today.")
else:
    df = jobs[expected_columns]
    filtered = df[df["title"].str.contains("QA|SDET|Selenium", case=False)]

    if filtered.empty:
        send_telegram_message("🤖 No matching jobs found today.")
    else:
        for _, row in filtered.iterrows():
            msg = f"<b>{row['title']}</b> at {row['company']}\n📍 {row['location']}\n🔗 <a href='{row['job_url']}'>View Job</a>"
            send_telegram_message(msg)

