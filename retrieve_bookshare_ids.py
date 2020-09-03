#!/usr/bin/env python
"""
Given metadata to search on in a CSV file, retrieves the Bookshare IDs for the data
and writes them to an output file
"""
import csv
import json
import os

from util.bksapiv2 import BKS_CLIENT_ID, BKS_BASE_URL, fetch_token
from util.data import copy_fields

in_filename = 'input_data/in.csv'
out_filename = 'output_data/out.csv'
retry_filename = 'output_data/retry.csv'

SEARCH_GET_URL = BKS_BASE_URL + '/titles'

if os.path.exists(in_filename):
    with open(in_filename, 'r') as in_file:
        with open(out_filename, 'w') as out_file:
            with open(retry_filename, 'w') as retry_file:

                # Open data file as column-indexable CSV
                csv_reader = csv.DictReader(in_file)

                # Open retry log for metadata not found yet
                retry_writer = csv.DictWriter(retry_file, fieldnames=csv_reader.fieldnames)
                retry_writer.writeheader()

                # Open CSV file to write, adding Bookshare ID column
                headers = csv_reader.fieldnames.copy()
                headers.insert(0, 'bookshareId')
                csv_writer = csv.DictWriter(out_file, fieldnames=headers)
                csv_writer.writeheader()

                # Get Bookshare API login credentials
                (session, token) = fetch_token()

                for in_row in csv_reader:
                    params = {'api_key': BKS_CLIENT_ID, 'limit': 1}
                    copy_fields(in_row, params, ['isbn13', 'title', 'authors', 'language', 'externalFormat'])
                    print(params)
                    response = session.get(SEARCH_GET_URL, params=params)
                    if response.status_code == 200:
                        title_records = response.json()
                        print(json.dumps(title_records, indent=4))
                        totalResults = title_records['totalResults']
                        if totalResults == 0:
                            print("WARNING: No matches yet for this metadata entry: ")
                            print(json.dumps(params, indent=4))
                            print("Writing to retry log.")
                            retry_writer.writerow(in_row)
                        else:
                            if totalResults > 1:
                                print("WARNING: More than one match for this metadata entry: ")
                                print(json.dumps(params, indent=4))
                            # Take the first record, regardless of how many
                            first_record = title_records['titles'][0]
                            bookshareId = first_record['bookshareId']
                            out_row = in_row.copy()
                            out_row["bookshareId"] = bookshareId
                            # Write the input data to the output file with the Bookshare ID prepended
                            csv_writer.writerow(out_row)
                    else:
                        print("HTTP Response: " + str(response.status_code))
                        print(response.text)
                        print("Writing to retry log.")
                        retry_writer.writerow(in_row)

else:
    print("Data file " + in_filename + " does not exist.")
