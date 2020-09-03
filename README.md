# Bookshare Metadata API Upload Example

This code example illustrates how to upload metadata to the Bookshare API, and then return and get Bookshare IDs for that metadata.

## Prerequisites
* A collection assistant account with Vision Australia
* Python 3.8
    * If you want to use another version, update it in the Pipfile before running `pipenv install`
    * These scripts were not tested with other versions, but should be compatible with anything >= 3.6.  Pipenv does not let you specify version ranges in the Pipfile.
* pipenv
* A Bookshare API V2 key  

## Set up the environment
* Set up some environment variables to expose your login credentials to the scripts.
| V2_API_KEY  | Your API key, usually a random 24-character string  |
| V2_API_USERNAME  | Username for the collection assistant, usually an email address  |
| V2_API_PASSWORD  | Password for the collection assistant  |
| BKS_API_BASE_URL | Base URL for the API, defaults to the QA environment  |
| BKS_TOKEN_URL | URL for retrieving tokens for Bookshare API, defaults to the QA environment  |
* Check out the project
* Enter the project directory
* Run `pipenv install`

## Set up the data
Because this example focuses on interacting with the APIs, the data loading format is as simple as possible: CSV files.

The CSV file needs to be in input_data/in.csv.  The columns in the example data are:

* title
* subtitle
* isbn13
* authors
* synopsis
* seriesTitle
* copyrightHolder
* copyrightDate
* allowRecommend
* categories
* countries
* languages
* usageRestriction
* contentType
* externalFormat

You should be able to add more columns, as long as you give them headers with the exact same of the corresponding argument in the Bookshare API.  

For simplicity, this example has the limitation that only one value is processed per column, even if the API accepts multiple values. For example, the categories column will only handle one category. 

There are a number of ways you could update the script to accept multiple values for a single parameter. For example, you could format and read the data from JSON files instead, or separating CSV entries within a column with hash marks or semicolons.

## Running the Scripts

###`load_physical_item_metadata.py`
To run this script using pipenv, run the following from the root of the project directory:

`pipenv run python load_physical_item_metadata.py`

The script will attempt to submit each line in the file input_data/in.csv to the Bookshare V2 API endpoint described at "[Submit metadata for new title](https://apidocs.bookshare.org/catalog/index.html#_title-submit)"

Any rows that fail will get copied to the output file output_data/out_failed_submission.csv in the same format, so that they can be investigated and retried later.

###`retrieve_bookshare_ids.py`

Metadata sent to the Bookshare API does not immediately show up in search results.  It is filtered through a number of processes before it can be found in Solr, the search engine used by Bookshare.  How long this can take depends on what else is going on in the Bookshare ecosystem: is it a quiet day, or are floods of new books being submitted?

After you've submitted the metadata, you can retrieve the Bookshare IDs of the new records with the second script.  You run the second script with this command:

`pipenv run python retrieve_bookshare_ids.py`

This command will go through each line in the input_data/in.csv file and search for the title in Bookshare.  Using the endpoint described at "[Search for titles](https://apidocs.bookshare.org/reference/index.html#_title-search)", the script will try to match on the fields isbn13, title, authors, language, and externalFormat.  Then it will take the Bookshare ID of the first result and write it to output_data/out.csv, followed by a copy of the input row.  If there is more than 1 matching result, a warning message will be printed, and the first result will be used.

If the request fails or returns no results, the row is copied to the output_data/retry.csv file to be investigated and retried later.
 
