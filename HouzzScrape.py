__author__ = 'U464363'
# Step 1 : Grab all the links of a houzz page
# Step 2 : Open each link one by one and grab firm name, address, phone, contact
from BeautifulSoup import BeautifulSoup
import urllib2
import re
from urlparse import urlparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from urllib.parse import urlparse

# Spread sheet import info here...

# Import list of general web pages (e.g. ...//page15, ...//page30, etc...)

# Counter for spread sheet row, so that we do not overwrite data that has just been entered
rowCounter = 0

def selectLinks(url):
# Function to get desired links from specified page ( STEP 1 )
    html_page = urllib2.urlopen(url)
    soup  = BeautifulSoup(html_page)

    # Create array for final list
    firmsLinksList = []

    # Grab all the links from the page we have put into the function
    allLinks = soup.findAll('div', attrs={'class' : 'THE CLASS WE WANT'}) # this part may be somewhat optional

    # Filter for the links we want (this part likely needs some editing)
    for link in allLinks:
        listFiltered = link.findAll('a', href=True)
        for link2 in listFiltered:
            firmsLinksList.append(a['href'])
    # Return a list of the desired links from the inputed page
    return firmsLinksList

def mineInfo(firmsList):
# Function to open up each page and mine desired info
    driver = webdriver.Chrome()

    for currentPage in firmsList:

        rowCounter = rowCounter + 1

        driver.get(currentPage)
        ##Driver get address, phone, name, and firm name by driver.find_element_ETC...
        ## Print out info so we know it works, then...
            ## write each element to the row of the spreadsheet we are working on
                ## use a counter for row number as opposed to the list, since we will be importing several pages
                ## I.E. variable: rowCounter


def main(webList):

    # Loop to go through each web url listed in outside spread sheet
    for url in webList:
        firmsList = selectLinks(url) # individual pages on the site
        mineInfo(firmsList) # individual firms listed on the page

main(webList)





