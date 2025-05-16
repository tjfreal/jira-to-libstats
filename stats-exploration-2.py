#!/usr/bin/env python3
import sqlite3
import json

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('libstats.db')
    cursor = conn.cursor()

    # Fetch each issue key and its JSON content
    cursor.execute("SELECT key, content FROM issues ORDER BY key")
    rows = cursor.fetchall()
    conn.close()

    # Iterate and count comments per issue
    for key, raw_json in rows:
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            print(f"{key}: invalid JSON")
            continue

        fields = data.get('fields', {})
        comments = fields.get('comment', {}).get('comments', [])
        count = len(comments)
        print(f"{key}: {count} comments")

if __name__ == '__main__':
    main()