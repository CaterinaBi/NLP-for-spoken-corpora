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
    def __init__(self, url: str = 'https://orfeo.ortolang.fr/?f%5Btype%5D%5B%5D=entretien&locale=fr'):
        '''
        This class is used to scrape a website and extract text from it.
        '''
        url_entretiens = 'https://orfeo.ortolang.fr/?f%5Btype%5D%5B%5D=entretien&locale=fr'
        url_conversations = 'https://orfeo.ortolang.fr/?f%5Btype%5D%5B%5D=conversation&locale=fr'
        url_reunion = 'https://orfeo.ortolang.fr/?f%5Btype%5D%5B%5D=r%C3%A9union&locale=fr'
        url_repas = 'https://orfeo.ortolang.fr/?f%5Btype%5D%5B%5D=repas&locale=fr'
        url_consultation = 'https://orfeo.ortolang.fr/?f%5Btype%5D%5B%5D=consultation&locale=fr'

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        self.driver.get(url) # look for all properties for sale within a 10-mile radius from Cambridge, UK
        time.sleep(2)

        print('---Activated.')

        self.id_number = 0

        self.dictionaries_list = []
        self.cleft_dictionaries = [] # will contain all cleft dictionaries from all texts
        # self.page = 0

    
    def get_all_recording_links(self):
        '''A method that acts like a crawler'''
        print('---Creating a crawler.')

        self.all_recordings_links_list = []

        contents = self.driver.find_element(By.CSS_SELECTOR, value="#documents")

        for index in range(1-101):
            
            self.elems = contents.find_element(By.CSS_SELECTOR, value=f'#documents>div:nth-child({index})>div')
            self.elem = self.elems.find_element(By.CSS_SELECTOR, value=f'#documents>div:nth-child({index})>div>h5>a')
            self.link = self.elem.get_attribute('href')
            print(self.link)
            self.all_recordings_links_list.append(self.link)

        time.sleep(2)

        print(self.all_recordings_links_list)

    def create_global_list(self):
        '''A method that creates a list of links to the properties to scrape'''
        self.whole_query_property_links.extend(self.all_properties_links_list)
        return self.whole_query_property_links

    def scroll_to_bottom(self):
        '''A method that scrolls to bottom of page.'''
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        return '--Scrolled to bottom'

    def move_to_the_next_page(self):
        '''A method that clicks on the 'next page' button, if present.'''
        try:
            self.move_to_next_page = self.driver.find_element(By.CSS_SELECTOR, value=".pagination-button.pagination-direction.pagination-direction--next")
            self.move_to_next_page.click()
            time.sleep(2)
            return '---Moved to next page'
        except:
            pass # passes if there is no 'next page' button
            time.sleep(2)
            return '--No next page'
