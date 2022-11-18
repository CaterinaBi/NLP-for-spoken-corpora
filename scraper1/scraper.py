from openpyxl.workbook import Workbook
from pyrsistent import s
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from tika import parser # pip install tika
from webdriver_manager.chrome import ChromeDriverManager

import time
from time import sleep
from datetime import date, datetime

import nltk
from nltk.tokenize import sent_tokenize

import json
import os
import pandas as pd

class Scraper:
    def __init__(self, url: str = 'http://lecteursanonymes.org/scenario/'):
        '''
        This class is used to scrape a website and extract text from it.
        '''
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url) # look for all properties for sale within a 10-mile radius from Cambridge, UK
        time.sleep(2)

        self.id_number = 0

        # self.dictionaries_list = [] # all dictionaries, will be split into centuries later
        self.dictionaries_list = []

        self.interrogative_dictionaries = []
        self.cleft_dictionaries = []

    def close_pop_up(self):
        '''A method that bypasses pop-ups if present.'''
        print('\n---Program initialised.\n')
        try:
            accept_cookies_button = self.driver.find_element(By.CSS_SELECTOR, value='#popmake-800>button')
            accept_cookies_button.click()
            time.sleep(2)
            print('\n---Pop up closed.\n')
        except:
            pass # passes if there is no cookies button
            time.sleep(2)

    def create_dictionary(self):
        '''A method that acts like a crawler and creates a dictionary of text metrics and links'''
        value = int
        
        for number in range(101): # there are 101 rows in total but we start at 1
            number += 1 # row numbers start at 1
            dictionary = {}

            value = number
            table_row = f"#main-content>div>div>div>div>table>tbody>tr:nth-child({value})"
            author_column = f"#main-content>div>div>div>div>table>tbody>tr:nth-child({value})>td:nth-child(3)"
            title_column = f"#main-content>div>div>div>div>table>tbody>tr:nth-child({value})>td:nth-child(2)"
            text_column= f"#main-content>div>div>div>div>table>tbody>tr:nth-child({value})>td:nth-child(4)>a"

            contents = self.driver.find_element(By.CSS_SELECTOR, value="#main-content>div>div>div>div>table>tbody")
            row = contents.find_element(By.CSS_SELECTOR, value=table_row)

            # id generator
            self.id_number += 1 
            text_id = f'text_{self.id_number}'
            dictionary['ID'] = text_id
            print(f'---Scraping text #{self.id_number}.\n')

            # contents to scrape
            author = row.find_element(By.CSS_SELECTOR, value=author_column).text
            dictionary['Author'] = author
            title = row.find_element(By.CSS_SELECTOR, value=title_column).text
            dictionary['Title'] = title
            
            try:
                text = row.find_element(By.CSS_SELECTOR, value=text_column)
                link = text.get_attribute('href')
                print(link)
                dictionary['Link'] = link
                # self.text_links.append(link) # appends link to links list
                self.dictionaries_list.append(dictionary)
                 # only appends dictionary if link is present
                # print('Dictionary appended\n')
            except:
                dictionary['Link'] = 'unavailable'
                print('Link unavailable, dictionary not appended\n')
                # print(dictionary)
                print('\n')
                continue # only appends dictionary if link is present

            time.sleep(2)
        
        print("--All dictionaries correctly created.\n")

    def extract_text_from_links(self):
        "Method that extracts text from links and appends text to dedicated dictionary key"
        for i, dictionary in enumerate(self.dictionaries_list):
            link = dictionary['Link']
            
            self.driver.get(link)
            #text = self.driver.find_element(By.CSS_SELECTOR, value='body>embed').text # string

            text = parser.from_file(link)
            print(text)

            dictionary['Text'] = text
            print(f'---Text #{i} extracted.\n')
            time.sleep(2)

        # print(self.dictionaries_list)

    def save_data_to_json(self, destination_folder='raw_data/data'):
        '''A method that converts the century lists into .json files and stores them into dedicated directory'''
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)

        file_name = 'lecteurs_anonymes.json'

        folder_path = os.path.join(destination_folder, file_name)
        with open(folder_path, 'w', encoding='utf-8') as output:
            json.dump(self.dictionaries_list, output, ensure_ascii=False, indent=4)
            print('---Json file created.')