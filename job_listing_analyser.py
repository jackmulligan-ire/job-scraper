#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 17:49:36 2021

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
import random

###Asking for first set of user input via search function###
print("Welcome to the job scraper and analyser!")

time.sleep(2)
print("\nFirst we need a search term. You can enter a single word (e.g. developer) or multiple words joined with a + sign (e.g. junior+developer)")
user_st = input("Please enter your search term: ")

time.sleep(1)
print("\nNext we need a country code. Common examples are: uk, ie, de")
user_coun = input("Please enter a country code: ")

time.sleep(1)
print("\nNext we need the city you want to search in (e.g. London, Berlin)")
user_city = input("Please enter a city: ")

#Job Scraper Functions
def search(search_term, country, city, number_pages=10):
    '''
    -search_term: str, the term you want to search for e.g. "developer"
    -country: str, country code of indeed site e.g. "ie" for Ireland
    -city: str, city you want to search in e.g. "dublin"
    -number_pages: int (default=10), number of search result pages you want to search
    '''
    print("\nStarting!\n")
    
    #Start with first 10 pages
    m = 0
    while m <= (number_pages * 10):
    
        #Gathering job offers
        with requests.Session() as s:
            #Changing URL in the loop
            URL = 'https://' + country.lower() + '.indeed.com/jobs?q=+' + search_term + '&sort=date&l=' + city.lower() + '&start=' + str(m)
            
            URL_nr = int(m/10)
            print("Getting results from page " + str(URL_nr + 1))
            
            m+=10
            
            try:
                p = s.get(URL, timeout=1)
            except requests.exceptions.RequestException as e:
                print("Blocked by source. Wait and try again.")
                print("\nFor next round: " + search_term + "-" + country + "-" + city +"\n")
                raise SystemExit(e)
            
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
    
        csv_filename = '/Users/jackmulligan/Documents/66DaysofDataScience/March_2021/Job_Scraper/' + city + '_' + search_term + '_' + current_date + '.csv'
        df.to_csv(csv_filename, index=False, header=True)
        

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
        
    print("\nDone!")
    return csv_filename

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
    
#Calling first part of function w/ user input
scraper_results = search(user_st, user_coun, user_city)

time.sleep(1)
#Getting second set of user inputs
print("\nWe got your job postings, now let's analyse them for keywords!")
user_npost = int(input("How many posts would you like to analyse: "))
        
#Description scraper function
def get_ran_postings(filename, num_postings, user_st):
    '''
    Takes in random job postings from .csv
    '''
    #Repairing user_st if it's in wrong format
    if "+" in user_st:
        plus_sign_index = user_st.find("+")
        user_st = user_st[:plus_sign_index] #we take first word
    
    empty_space = " "
    if empty_space in user_st:
        empty_space_index = user_st.find(empty_space)
        user_st = user_st[:empty_space_index] #we take first word
    
    #Read in the .csv file via filename
    df = pd.read_csv(filename)
    limit = len(df) - 1
    
    if num_postings > limit:
        raise Exception('You have requested too many postings. Maximum number for this file is: ' + str(limit))
    
    #Select 10 random numbers, store them in an array
    selection = {'Nr.': [],
                'Title': [],
                'Company': [],
                'Location': [],
                'Link': []}
    
    #Looping through df to get random selection of postings
    ran_nums = []
    i = 0
    
    timeout = 5 # [seconds]
    timeout_start = time.time()
    
    while i < num_postings:
        if time.time() > timeout_start + timeout: #Timeout 
            print("Timeout! Could not gather full requested amount")
            break
        n = random.randint(0, limit)
        
        if n in ran_nums: #Continuing if number already selected
            continue
        
        title = df.iloc[n, 1].lower() #Checking if title relevant to search 
        match_test = int(user_st in title)
        if match_test == 1:
            selection['Nr.'].append(n)
            selection['Title'].append(df.iloc[n, 1])
            selection['Company'].append(df.iloc[n, 2])
            selection['Location'].append(df.iloc[n, 3])
            selection['Link'].append(df.iloc[n, 5])
            ran_nums.append(n)
            i += 1
        else:
            continue
    
    print(str(len(ran_nums)) + " acquired.")
        
    #Make a new df
    df_columns = list(selection.keys())
    df = pd.DataFrame(selection, columns=df_columns)
    
    #Exporting to .csv
    now = datetime.now()
    current_date = now.strftime("%d%m%Y")
    csv_filename = '/Users/jackmulligan/Documents/66DaysofDataScience/March_2021/Job_Scraper/job_descriptions_' + current_date + '_parsed.csv'
    df.to_csv(csv_filename, index=False, header=True)
    return csv_filename

#Getting ran_postings for user
postings_results = get_ran_postings(scraper_results, user_npost, user_st)
time.sleep(1)

print("\nYou can now enter keyword(s) to analyse. You can enter as many as you'd like!")
print("Just answer along, and enter 'yes' if you want to continue")

more_terms = True
user_kws = []

while more_terms:
    user_t = input("Enter a keyword you want to search for: ")
    user_kws.append(user_t)
    new_round = input("Would you like to enter another keyword?: ")
    if new_round.lower().strip() == "yes":
        continue
    else:
        more_terms = False

def parse_custom(filename, search_terms):
    '''
    Filename: .xls file with job_descriptions, converted from csv_file
              Best to take max 10-15 job descriptions at a time
              .xls file must contain sheet_name='job_descriptions' w/ standard
              form
    '''
    # Read in specific sheet of .xls file
    df = pd.read_csv(filename)
    
    #Creating storage for data
    data = {'Title': [],
            'Company': [],
            'Location': [],
            'Link': [],}
    
    #Use a for loop to append to data using key value pairs
    for term in search_terms:
        data[term] = []

    #Parsing through URLs in the df
    m=0
    while m < len(df):
        URL = df.iloc[m, 4]
        with requests.Session() as s:
            #Getting webpage
            try:
                p = s.get(URL)
            except requests.exceptions.RequestException as e:
                print("Blocked by source. Try new IP address via VPN")
                raise SystemExit(e)
                
            soup = BeautifulSoup(p.content, 'html.parser')
            
            #Getting page section
            job_description = soup.find(id="jobDescriptionText")
            
            #Appending basic data
            data['Title'].append(df.iloc[m, 1])
            data['Company'].append(df.iloc[m, 2])
            data['Location'].append(df.iloc[m, 3])
            data['Link'].append(URL)
            
            print("\nAnalysing post number: " + str(m+1))
            #Detecting for search terms in job desc via loop
            for term in search_terms:
                
                #Boolean for detection
                present = int(term.lower() in job_description.text.lower())
                if present == 1:
                    print("Found: " + term)
                
                #Appending to dict with data
                data[term].append(present) 
            
            #Giving code time to execute
            time.sleep(1)
            
            #Going to next item
            m += 1
            
    #Creating columns with data
    df_columns = list(data.keys())
    new_df = pd.DataFrame(data, columns=df_columns)
    
    #Printing to CSV
    csv_filename = '/Users/jackmulligan/Documents/66DaysofDataScience/March_2021/Job_Scraper/keyword_results.csv'
    new_df.to_csv(csv_filename, index=False, header=True)
    
    #Printing final counts to console    
    n = 4 #Need to increase if length of data changes
    max_n = len(new_df.columns)
    while n < max_n:
        count = sum(new_df.iloc[:,n])
        col_name = df_columns[n]
        print("\nCount for " + col_name + ": " + str(count))
        n += 1
    
    return csv_filename

#Getting keyword results for users
keyword_results = parse_custom(postings_results, user_kws)
time.sleep(1)
print("\nKeyword results available in: " + keyword_results)
time.sleep(1)
print("\nFull listings available in: " + scraper_results) 
time.sleep(1)
print("\nProgramme finished. Goodbye!")
