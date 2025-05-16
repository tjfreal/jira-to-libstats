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
    # Filter for a single issue PR-13974
    target_key = 'PR-13974'
    conn.close()

    # Find and pretty-print the JSON for PR-13974
    for key, raw_json in rows:
        if key != target_key:
            continue
        try:
            data = json.loads(raw_json)
        except json.JSONDecodeError:
            print(f"{key}: invalid JSON")
            return

        # Pretty-print top-level data keys
        print(f"{key} - top-level fields:")
        print(json.dumps({k: data[k] for k in data}, indent=4))

        # Pretty-print the 'fields' object
        fields = data.get('fields', {})
        print(f"{key} - 'fields' content:")
        print(json.dumps(fields, indent=4))
        return

if __name__ == '__main__':
    main()