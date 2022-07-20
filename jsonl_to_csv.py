"""
Convert our jsonl file to CSV.
"""

import json
import csv

REBOUNDS_FILE = 'probably_rebounds.jsonl'
OUTPUT_CSV = 'probably_rebounds.csv'

rows = [('tweet_url',)]

if __name__ == '__main__':
    with open(REBOUNDS_FILE) as f:
        for line in f:
            row = json.loads(line)
            rows.append((row['url'],))
            #row = dict(sorted(row.items()))
            #rows.append(row.values())

    with open(OUTPUT_CSV, 'w', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)
