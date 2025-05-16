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
        # Diagnostic: print all JSON element names for this ticket
        #print(f"{key}: data keys = {list(data.keys())}")
        #print(f"{key}: fields keys = {list(fields.keys())}")
        comments = fields.get('comment', {}).get('comments', [])
        # # Extract attachment filenames, if any
        attachments = fields.get('attachment', [])
        filenames = [att.get('filename') for att in attachments]
        count = len(comments)
        if filenames:
             print(f"{key}: {count} comments; attachments: {', '.join(filenames)}")
        else:
             print(f"{key}: {count} comments; no attachments")

if __name__ == '__main__':
    main()