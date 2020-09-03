#!/usr/bin/env python
"""
Given metadata in a CSV file, submits it to the Bookshare V2 API.
Any failed submissions are written to an additional CSV file, to be retried later.
"""
import csv
import os
import json

from util.bksapiv2 import fetch_token, BKS_BASE_URL, BKS_API_KEY_PARAM

in_filename = 'input_data/in.csv'
out_filename = 'output_data/out_failed_submission.csv'

METADATA_POST_URL = BKS_BASE_URL + '/titles'

if os.path.exists(in_filename):
    with open(in_filename, 'r') as in_file:
        with open(out_filename, 'w') as out_file:
            # Open data file as column-indexable CSV
            csv_reader = csv.DictReader(in_file)
            headers = csv_reader.fieldnames
            # Open error log
            csv_writer = csv.DictWriter(out_file, fieldnames=headers)
            csv_writer.writeheader()
            # Get our API V2 session
            (session, token) = fetch_token()
            for in_row in csv_reader:
                print(METADATA_POST_URL)
                response = session.post(METADATA_POST_URL, data=in_row, params=BKS_API_KEY_PARAM)
                if response.status_code != 202:
                    # Problem with uploading the metadata
                    csv_writer.writerow(in_row)
                    print(str(response.status_code))
                    print(response.content)
                else:
                   print(json.dumps(response.json(),indent=4))









