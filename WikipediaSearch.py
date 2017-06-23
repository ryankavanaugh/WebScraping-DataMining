from BeautifulSoup import BeautifulSoup
import urllib2
import re
from urlparse import urlparse
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

firstLink = 'https://en.wikipedia.org/wiki/Sleepers'
allLinks = []
allLinks.append(firstLink)

def getLinks(url):
    html_page = urllib2.urlopen(url)
    soup = BeautifulSoup(html_page)
    linkedUrls = []
    newList = soup.findAll('div', attrs={'class': 'mw-parser-output'})
    for article in newList:
        listTemp = article.findAll('a', href=True)
        for link in listTemp:
            linkedUrls.append(a['href'])
    return linkedUrls

allLinks = getLinks(firstLink)

urlCounter = 0

whileLink = firstLink

while (whileLink == firstLink):
    for x in allLinks:
        urlCounter += 1
        if x == "/wiki/Kevin_Bacon":
            print("You Win!")
            whileLink = x
        else:
            if allLinks[urlCounter].startswith('/wiki'):
                currentLink = 'https://en.wikipedia.org' + allLinks[urlCounter] # Maybe use allLinks.pop([0]) here
                linksToAdd = getLinks(currentLink)

                allLinks = allLinks + linksToAdd
                #???
