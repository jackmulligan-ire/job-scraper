# job-scraper: Scrape indeed for relevant job postings.
Scrapes job postings from indeed. You can search by country and city location. You'll find a general search function, as well as functions to include or exclude certain keywords. I've also written a programme that scrapes posts and analyses them for particular keywords. Written in Python 3.7! 

Set-up: Change all directories to a file on your device.

Learned: Functional programming, making http requests, writing to a .csv file, using JSON, using random library, using time library.

## Functions available in job-scraper.py:

* `search(search_term, country, city, number_pages=10)`

* `filter_search(search_term, filter_term, country, city, number_pages=10)`

* `exclude_search(search_term, exclude_term, country, city, number_pages=10)`

## job-listing-analyser.py

Listings analyser programme, based in console. Enter in search term, country and location to get started. You'll then be prompted to input number of scraped listings to be more closely analysed, as well as the keywords you'd like to analyse for. Results are outputed to .csv, with instant feedback about results also offered in console.

## job-listing-spider.py

Upcoming spider project.
