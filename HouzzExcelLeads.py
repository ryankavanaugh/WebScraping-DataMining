import xlrd
import xlwt
from xlwt import easyxf
from xlutils.copy import copy
import requests
from BeautifulSoup import BeautifulSoup
import urllib2
import re
from urlparse import urlparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os.path
from selenium.webdriver.common.by import By


# Spread sheet import info here...

# Import list of general web pages (e.g. ...//page15, ...//page30, etc...)

# Counter for spread sheet row, so that we do not overwrite data that has just been entered
rowCounter = 0

url = 'https://www.houzz.com/professionals/landscape-contractors/s/Landscape-Contractors/c/Portland%2C-OR/sortReviews'


workbookO = xlrd.open_workbook('Blank.xlsx')
worksheet = workbookO.sheet_by_name('Sheet1')

wbNew = copy(workbookO)
wb_sheet = wbNew.get_sheet(0)

#allFirmInfo = {'number' : 0, 'firm name' : 'name', 'location' : 'adddress', 'phone' : 'number'}

def selectLinks(url):
# Function to get desired links from specified page ( STEP 1 )
    html_page = urllib2.urlopen(url)
    soup  = BeautifulSoup(html_page)

    # Create array for final list
    firmsLinksList = []

    # Grab all the links from the page we have put into the function
    allLinks = soup.findAll('div', attrs={'class' : 'name-info'}) # this part may be somewhat optional

    # Filter for the links we want (this part likely needs some editing)
    for link in allLinks:
        listFiltered = link.findAll('a', href=True)
        for link2 in listFiltered:
            firmsLinksList.append(link2['href'])
            #print(link2)

    counter = 0
    finalList = []
    for link3 in firmsLinksList:
        if firmsLinksList[counter].startswith('https://www.houzz.com/'):
            finalList.append(link3)
        counter =+ 1
        #print(link3)

    return firmsLinksList

def mineInfo(firmsList):
# Function to open up each page and mine desired info

    rowCounter = 0
    excelCounter = 1

    for currentPage in firmsList:
        try:
            onlinePage = firmsList[rowCounter]
            if onlinePage.startswith('https://www.houzz.com/pro/'):
                driver = webdriver.Chrome()
                driver.get(onlinePage)
                delay = 3
                try:
                    myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'profileHeader')))
                    print
                    "Page is ready!"
                except TimeoutException:
                    print
                    "Loading took too much time!"

                try:
                    firmName = driver.find_element_by_xpath('//*[@id="profileHeader"]/div/div/div/div[2]/div/h1/a')
                except:
                    firmName = "error"
                print(firmName.text)

                try:
                    contact = driver.find_element_by_xpath('//*[@id="profileMainContent"]/div[1]/div[2]/div/div[2]/div/div/div[2]/div')
                except:
                    contact = "error"
                print(contact.text)

                try:
                    address = driver.find_element_by_xpath('//*[@id="profileMainContent"]/div[1]/div[2]/div/div[2]/div/div/div[3]/div')
                except:
                    address = "error"
                print(address.text)

                try:
                    phone = driver.find_element_by_xpath('//*[@id="profileHeader"]/div/div/div/div[5]/div/ul/li[2]/div/span[2]/a')
                    phoneReal = phone.get_attribute('phone')
                except:
                    phoneReal = "error"
                print(phoneReal)

                wb_sheet.write(excelCounter, 0, firmName.text)
                if contact.text.startswith('Location:'):
                    wb_sheet.write(excelCounter, 1, 'Currently N/A')
                    wb_sheet.write(excelCounter, 3, contact.text)
                else:
                    wb_sheet.write(excelCounter, 1, contact.text)
                    wb_sheet.write(excelCounter, 3, address.text)
                wb_sheet.write(excelCounter, 2, phoneReal)
                wb_sheet.write(excelCounter, 5, onlinePage)

                excelCounter = excelCounter + 1
            driver.quit()
            rowCounter = rowCounter + 1
        except:
            wb_sheet.write(excelCounter, 0, firmName.text)
            try:
                wb_sheet.write(excelCounter, 3, address.text)
            except:
                pass
            try:
                if contact.text.startswith('Location:'):
                    wb_sheet.write(excelCounter, 1, 'Currently N/A')
                    wb_sheet.write(excelCounter, 3, contact.text)
                else:
                    wb_sheet.write(excelCounter, 1, contact.text)
                    wb_sheet.write(excelCounter, 3, address.text)
            except:
                pass
            try:
                wb_sheet.write(excelCounter, 2, phoneReal)
            except:
                pass
            wb_sheet.write(excelCounter, 5, onlinePage)

            excelCounter = excelCounter + 1
            rowCounter = rowCounter + 1
            pass


def main(webList):

    # Loop to go through each web url listed in outside spread sheet
    for url in webList:
        firmsList = selectLinks(url) # individual pages on the site
        mineInfo(firmsList) # individual firms listed on the page

firms = selectLinks(url)

mineInfo(firms)

file_path = '/Users/Ryan/Desktop/WebScrape1/Lists With Addresses/LAContractorInfo'
wbNew.save(file_path + '.csv' + os.path.splitext(file_path)[-1])
