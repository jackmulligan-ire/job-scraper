# job-scraper
Learned: functional programming, making http requests, writing to a .csv file, using JSON as a temporary place to store data.

# Functions available:

search(search_term, location, city, number_pages)
-search_term: str, the term you want to search for e.g. "backend+developer"

-location: str, country code of indeed site e.g. "ie" for Ireland

-city: str, city you want to search in e.g. "dublin"

-number_pages: int (default=10), number of search result pages you want to search

filter_search(search_term, location, city, number_pages, filter_term)

-search_term: str, the term you want to search for e.g. "backend+developer"

-location: str, country code of indeed site e.g. "ie" for Ireland

-city: str, city you want to search in e.g. "dublin"

-number_pages: int (default=10), number of search result pages you want to search

-filter_term: str, term you want to filter for e.g. "junior"

exclude_search(search_term, location, city, number_pages, exclude_term)

-search_term: str, the term(s) you want to search for e.g. "backend+developer"

-location: str, country code of indeed site e.g. "ie" for Ireland

-city: str, city you want to search in e.g. "dublin"

-number_pages: int (default=10), number of search result pages you want to search

-exclude_term: str, term you want to exclude for e.g. "senior"
