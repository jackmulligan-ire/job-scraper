#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 16:55:18 2021

@author: jackmulligan
"""

#Importing libraries
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import json
import time

#MAIN FUNCTIONS

def search(search_term, country, city, number_pages=10):
    '''
    -search_term: str, the term you want to search for e.g. "developer"
    -country: str, country code of indeed site e.g. "ie" for Ireland
    -city: str, city you want to search in e.g. "dublin"
    -number_pages: int (default=10), number of search result pages you want to search
    '''
    print("Starting!")
    
    #Start with first 10 pages
    m = 0
    while m <= (number_pages * 10):
    
        #Gathering job offers
        with requests.Session() as s:
            #Changing URL in the loop
            URL = 'https://' + country.lower() + '.indeed.com/jobs?q=+' + search_term + '&sort=date&l=' + city.lower() + '&start=' + str(m)
            
            URL_nr = int(m/10)
            print("Getting URL " + str(URL_nr))
            
            m+=10
            
            p = s.get(URL)
            #print(p.text)
            
            soup = BeautifulSoup(p.content, 'html.parser')
            
            #Getting relevant section of the page
            results = soup.find(id='resultsCol')
            
            #Getting job postings
            job_elems = results.find_all(class_='jobsearch-SerpJobCard')
            
            #Creating place to store our data
            data = {'Date': [],
                    'Title': [],
                    'Company': [],
                    'Country': [],
                    'Posted': [],
                    'Link': []
                    }
            
            #CREATING NEW FILE IF NEEDED
            try:
                with open("data_file.json", 'x') as write_file:
                    json.dump(data, write_file)
            except FileExistsError:
                pass
            
            #Printing out individual job postings
            n = 1
            for job_elem in job_elems:
                
                #GETTING ELEMENTS
                now = datetime.now() #Timestamp
                current_time = now.strftime("%d/%m/%Y, %H:%M")
                
                title_elem = job_elem.find(class_='jobtitle') #Title
                company_elem = job_elem.find('span', class_='company') #Company
                country_elem = job_elem.find('span', class_='location') #Country
                age_elem = job_elem.find('span', class_='date') #Age
                
                #Transforming age_elem into a number
                if 'just posted' in age_elem.text.lower():
                    age_elem = "0"
                elif 'today' in age_elem.text.lower():
                    age_elem = "0"
                elif '1 day ago' in age_elem.text.lower():
                    age_elem = "1"
                else:
                    age_elem = age_elem.text.replace('days ago', '')
                    age_elem = age_elem.strip()
                
                link_elem = job_elem.find('a')['href'] #Link
                href_elem = "https://" + country + ".indeed.com" + link_elem
                
                #Continue if elem empty
                if None in (
                        title_elem, 
                        company_elem, 
                        country_elem, 
                        age_elem, 
                        link_elem,
                        href_elem):
                    continue
                
                #STORING ELEMS AS DATA
                #Row
                data['Date'].append(current_time) #Store Date
                data['Title'].append(title_elem.text.strip()) #Store Title
                data['Company'].append(company_elem.text.strip()) #Store Company
                data['Country'].append(country_elem.text.strip()) #Store Location
                data['Posted'].append(age_elem) #Store age
                data['Link'].append(href_elem) #Store link
                
                n += 1
            
            append_data(data)
        
        write_data(city, search_term)

    clear_data(data)

def filter_search(search_term, filter_term, country, city, number_pages=10):
    '''
    -search_term: str, the term you want to search for e.g. "backend+developer"
    -filter_term: str, term you want to filter for e.g. "junior"
    -country: str, country code of indeed site e.g. "ie" for Ireland
    -city: str, city you want to search in e.g. "dublin"
    -number_pages: int (default=10), number of search result pages you want to search

    '''
    print("Starting!")
    
    #Start with first 10 pages
    m = 0
    while m <= (number_pages * 10):
    
        #Gathering job offers
        with requests.Session() as s:
            #Changing URL in the loop
            URL = 'https://' + country.lower() + '.indeed.com/jobs?q=+' + search_term + '&sort=date&l=' + city.lower() + '&start=' + str(m)
            
            URL_nr = int(m/10)
            print("Getting URL " + str(URL_nr))
            
            m+=10
            
            p = s.get(URL)
            #print(p.text)
            
            soup = BeautifulSoup(p.content, 'html.parser')
            
            #Getting relevant section of the page
            results = soup.find(id='resultsCol')
            
            #Getting job postings
            job_elems = results.find_all(class_='jobsearch-SerpJobCard')
            
            #Creating place to store our data
            data = {'Date': [],
                    'Title': [],
                    'Company': [],
                    'Country': [],
                    'Posted': [],
                    'Link': []
                    }
            
            #CREATING NEW FILE IF NEEDED
            try:
                with open("data_file.json", 'x') as write_file:
                    json.dump(data, write_file)
            except FileExistsError:
                pass
            
            #Printing out individual job postings
            n = 1
            for job_elem in job_elems:
                
                #GETTING ELEMENTS
                now = datetime.now() #Timestamp
                current_time = now.strftime("%d/%m/%Y, %H:%M")
                
                title_elem = job_elem.find(class_='jobtitle') #Title
                company_elem = job_elem.find('span', class_='company') #Company
                country_elem = job_elem.find('span', class_='location') #Country
                age_elem = job_elem.find('span', class_='date') #Age
                
                #Transforming age_elem into a number
                if 'just posted' in age_elem.text.lower():
                    age_elem = "0"
                elif 'today' in age_elem.text.lower():
                    age_elem = "0"
                elif '1 day ago' in age_elem.text.lower():
                    age_elem = "1"
                else:
                    age_elem = age_elem.text.replace('days ago', '')
                    age_elem = age_elem.strip()
                
                link_elem = job_elem.find('a')['href'] #Link
                href_elem = "https://" + country + ".indeed.com" + link_elem
                
                #Continue if elem empty
                if None in (
                        title_elem, 
                        company_elem, 
                        country_elem, 
                        age_elem, 
                        link_elem,
                        href_elem):
                    continue
                
                #filter and exclude params (only include active param)
                if not(filter_term in title_elem.text.lower()):
                    continue
                
                #STORING ELEMS AS DATA
                #Row
                data['Date'].append(current_time) #Store Date
                data['Title'].append(title_elem.text.strip()) #Store Title
                data['Company'].append(company_elem.text.strip()) #Store Company
                data['Country'].append(country_elem.text.strip()) #Store Country
                data['Posted'].append(age_elem) #Store age
                data['Link'].append(href_elem) #Store link
                
                n += 1
            
            append_data(data)
        
        write_data(city, search_term, extra_term=filter_term)

    clear_data(data)
    
def exclude_search(search_term, exclude_term, country, city, number_pages=10):
    '''
    -search_term: str, the term(s) you want to search for e.g. "backend+developer"
    -country: str, country code of indeed site e.g. "ie" for Ireland
    -city: str, city you want to search in e.g. "dublin"
    -number_pages: int (default=10), number of search result pages you want to search
    -exclude_term: str, term you want to exclude for e.g. "senior"
    '''
    print("Starting!")
    
    #Start with first 10 pages
    m = 0
    while m <= (number_pages * 10):
    
        #Gathering job offers
        with requests.Session() as s:
            #Changing URL in the loop
            URL = 'https://' + country.lower() + '.indeed.com/jobs?q=+' + search_term + '&sort=date&l=' + city.lower() + '&start=' + str(m)
            
            URL_nr = int(m/10)
            print("Getting URL " + str(URL_nr))
            
            m+=10
            
            p = s.get(URL)
            #print(p.text)
            
            soup = BeautifulSoup(p.content, 'html.parser')
            
            #Getting relevant section of the page
            results = soup.find(id='resultsCol')
            
            #Getting job postings
            job_elems = results.find_all(class_='jobsearch-SerpJobCard')
            
            #Creating place to store our data
            data = {'Date': [],
                    'Title': [],
                    'Company': [],
                    'Country': [],
                    'Posted': [],
                    'Link': []
                    }
            
            #CREATING NEW FILE IF NEEDED
            try:
                with open("data_file.json", 'x') as write_file:
                    json.dump(data, write_file)
            except FileExistsError:
                pass
            
            #Printing out individual job postings
            n = 1
            for job_elem in job_elems:
                
                #GETTING ELEMENTS
                now = datetime.now() #Timestamp
                current_time = now.strftime("%d/%m/%Y, %H:%M")
                
                title_elem = job_elem.find(class_='jobtitle') #Title
                company_elem = job_elem.find('span', class_='company') #Company
                country_elem = job_elem.find('span', class_='location') #Country
                age_elem = job_elem.find('span', class_='date') #Age
                
                #Transforming age_elem into a number
                if 'just posted' in age_elem.text.lower():
                    age_elem = "0"
                elif 'today' in age_elem.text.lower():
                    age_elem = "0"
                elif '1 day ago' in age_elem.text.lower():
                    age_elem = "1"
                else:
                    age_elem = age_elem.text.replace('days ago', '')
                    age_elem = age_elem.strip()
                
                link_elem = job_elem.find('a')['href'] #Link
                href_elem = "https://" + country + ".indeed.com" + link_elem
                
                #Continue if elem empty
                if None in (
                        title_elem, 
                        company_elem, 
                        country_elem, 
                        age_elem, 
                        link_elem,
                        href_elem):
                    continue
                
                #Skipping over excluded terms
                if exclude_term in title_elem.text.lower():
                    continue
                
                #STORING ELEMS AS DATA
                #Row
                data['Date'].append(current_time) #Store Date
                data['Title'].append(title_elem.text.strip()) #Store Title
                data['Company'].append(company_elem.text.strip()) #Store Company
                data['Country'].append(country_elem.text.strip()) #Store Country
                data['Posted'].append(age_elem) #Store age
                data['Link'].append(href_elem) #Store link
                
                n += 1
            
            append_data(data)
        
        write_data(city, search_term, extra_term=exclude_term)

    clear_data(data)

#Modules - common to all functions
def append_data(data):
    '''
    Gathers previous data obtained by JSON and appends it to data
    '''
    #RELOAD DATA THAT WE'VE STORED
    with open("data_file.json", 'r+') as read_file:
        stored_data = json.load(read_file)
    
    #APPEND NEW DATA TO STORED DATAA
    
    #DATE
    dates = data['Date'] #Selecting
    stored_dates = stored_data['Date']
    
    #Append values to data
    for date in dates:
        stored_dates.append(date)

    #TITLE
    titles = data['Title']
    stored_titles = stored_data['Title'] #Selecting
    
    #Append values to data
    for title in titles:
        stored_titles.append(title)
    
    #COMPANY
    companies = data['Company']
    stored_companies = stored_data['Company'] #Selecting
    
    #Append values to data
    for company in companies:
        stored_companies.append(company)
        
    #LOCATION
    locations = data['Country']
    stored_locations = stored_data['Country'] #Selecting
    
    #Append values to data
    for location in locations:
        stored_locations.append(location)
        
    #POSTED
    posteds = data['Posted']
    stored_posteds = stored_data['Posted'] #Selecting
    
    #Append values to data
    for posted in posteds:
        stored_posteds.append(posted)
    
    #LINKS
    links = data['Link']
    stored_links = stored_data['Link'] #Selecting
    
    #Append values to data
    for link in links:
        stored_links.append(link)
    
    #POSTING DATA TO JSON FOR LATER RETRIEVAL
    with open("data_file.json", 'w') as write_file:
        json.dump(stored_data, write_file)
    
    #Giving server 1-sec break to not overload
    time.sleep(1)
    

def write_data(city, search_term, extra_term=""):
    '''
    Transforms data in df, exports to .csv file
    '''
    with open("data_file.json", 'r+') as read_file:
        stored_data = json.load(read_file)
    
    #Making dataframe from data
    df = pd.DataFrame(stored_data, columns=['Date',
                                     'Title',
                                     'Company',
                                     'Country',
                                     'Posted',
                                     'Link'])
            
    #Storing dataframe as an excel file
    now = datetime.now()
    current_date = now.strftime("%d%m%Y")
    if extra_term == "":
        csv_filename = '/Users/jackmulligan/Documents/66DaysofDataScience/March_2021/Job_Scraper/' + city + '_' + search_term + '_' + current_date + '.csv'
        df.to_csv(csv_filename, index=False, header=True)
    else:
        csv_filename = '/Users/jackmulligan/Documents/66DaysofDataScience/March_2021/Job_Scraper/' + city + '_' + search_term + '_' + extra_term + '_' + current_date + '.csv'
        df.to_csv(csv_filename, index=False, header=True)
        
def clear_data(data):
    '''
    Clears data to allow clean slate for next function call
    '''
    #Clearing data
    data = {'Date': [],
            'Title': [],
            'Company': [],
            'Country': [],
            'Posted': [],
            'Link': []
            }
        
    #Clearing JSON file
    with open("data_file.json", 'w') as write_file:
        json.dump(data, write_file)
        
    print("Done!")
