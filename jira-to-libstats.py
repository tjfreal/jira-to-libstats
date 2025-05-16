import re
import requests
from collections import defaultdict
from requests.auth import HTTPBasicAuth
import json
import os
import sqlite3
from dotenv import load_dotenv

# Load secrets from .env
load_dotenv()
JIRA_USERNAME = os.getenv('JIRA_USERNAME')
JIRA_PASSWORD = os.getenv('JIRA_PASSWORD')
BASE_URL = os.getenv('BASE_URL')

# Initialize SQLite database for storing full issue JSON
conn = sqlite3.connect('libstats.db')
cursor = conn.cursor()
cursor.execute(
    'CREATE TABLE IF NOT EXISTS issues (key TEXT PRIMARY KEY, content TEXT)'
)
conn.commit()

def fetch_issues(start_at=0, max_results=50):
    jql = "project=PR"
    #jql = "project=PR AND key >= PR-17175 AND key <= PR-17285"
    
    url = "{}/rest/api/2/search".format(BASE_URL)
    params = {
        "jql": jql,
        "startAt": start_at,
        "maxResults": max_results,
        "fields": "summary,description,comment"
    }
    headers = {"Accept": "application/json"}

    print("\n--- Fetching Issues ---")
    print("URL: {}".format(url))
    print("JQL: {}".format(jql))
    print("StartAt: {}, MaxResults: {}".format(start_at, max_results))

    try:
        response = requests.get(url, headers=headers, params=params, auth=HTTPBasicAuth(JIRA_USERNAME, JIRA_PASSWORD))
        print("Status Code: {}".format(response.status_code))
        if not response.ok:
            print("Response Text: {}".format(response.text))
        return response.json() if response.ok else None
    except Exception as e:
        print("Request failed: {}".format(str(e)))
        return None


def main():
    start_at = 0
    max_results = 50

    while True:
        result = fetch_issues(start_at, max_results)
        if not result:
            break

        issues = result.get('issues', [])
        if not issues:
            break

        for issue in issues:
            # Store full issue JSON in database
            raw_json = json.dumps(issue)
            cursor.execute(
                'REPLACE INTO issues (key, content) VALUES (?, ?)',
                (issue['key'], raw_json)
            )
            conn.commit()
            print(f"Stored issue {issue['key']} in database")

        if start_at + max_results >= result.get('total', 0):
            break
        start_at += max_results

if __name__ == "__main__":
    main()
