from selenium import webdriver
import time
import datetime
import argparse
from time import sleep 
import numpy as np
from bs4 import BeautifulSoup
import urllib
import  requests
import os 
import pandas as pd 

class lgaScrapper():
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-url', '--url', help='URL to the online repository of images')
        args = vars(parser.parse_args())
        self.url = args['url']
        self.url = 'https://nigeriapostcodes.com/'
        # Extract the dir name
        
    def getStates(self):
        '''
            Get list of states in Nigeria as an array
        '''
        center_performance=pd.read_csv(r'C:\Users\otaladesuyi\Documents\Sidmach\Data science\center performance.csv', encoding='latin-1')
        states=center_performance.State.unique()
        states= np.delete(states, np.where(states=='Off Shore'))
        return states

    def getstatelinks(self):

        '''
            Get links to local governments per state and save to csv 
        '''
        self.state_name = self.url.split('//')[1].split('.')[0]

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")

        # Initialize the  webdriver and open the URL

        # # options = webdriver.FirefoxOptions()
        # self.driver = webdriver.Firefox(r'C:\Users\HP\Downloads\Software Setups\geckodriver')
        
        self.driver = webdriver.Chrome(r'C:\Users\otaladesuyi\Documents\Apps\chromedriver')
        self.driver.get(self.url)
        sleep(2)

        state_links = self.driver.find_elements_by_xpath('//ul[@id = "widgetlist"]//li[@id = "categories-2"]//li//a')

        #create an empty list to eventually hold all the url links for the states
        stateHrefs = []
        undesired = ["https://nigeriapostcodes.com/category/bank-sort-codes/", "https://nigeriapostcodes.com/category/uncategorized/" ]

        ##loop through state_links and remove the two links which are not for state: "bankSortCode" and "Uncategorized"
        for lnk in state_links:
            if undesired[0] in lnk.get_attribute('href') or undesired[1] in lnk.get_attribute('href'):
                continue
            else:   
                stateHrefs.append(lnk.get_attribute('href'))

        # Create the directory after checking if it already exists or not
        dir_name = 'StateRelatedLinks'
        if not os.path.exists(dir_name):
            try:
                os.mkdir(dir_name)
            except OSError:
                print("[INFO] Creation of the directory {} failed".format(os.path.abspath(dir_name)))
            else:
                print("[INFO] Successfully created the directory {} ".format(os.path.abspath(dir_name)))

        # Write the links to the image pages to a file
        f = open("{}/{}.csv".format(dir_name, self.state_name), 'w')
        f.write(",\n".join(stateHrefs))
        print("[INFO] Successfully created the file {}.csv with {} links".format(self.state_name, len(stateHrefs)))





if __name__ == '__main__':
    app = lgaScrapper()