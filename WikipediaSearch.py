__author__ = 'U464363'
# Things to investigate:
# 1. Why is the list built statefully? Can it be pulled functionally and immutably from the links in the article via map()?
#  #     referring to linkeUrls = []
# 2. Concurrent Modification: modifying a list at the same time as iterating over it.
# #     This can lead to very confusing behavior. If you have "for a in b" you should never modify b inside that loop.
# 3. For-loops should consume elements, not indices. Since you only use "current" in the context of "allLinks[current]",
# #     current is an inappropriate level of indirection. That means it's too specific compared to its use.
#       Try to get your for-loop to look like "for link in links" ???
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
                currentLink = 'https://en.wikipedia.org' + allLinks[urlCounter]
                linksToAdd = getLinks(currentLink)
               # print('NillaPleaseNewSection')
                #???
                allLinks = allLinks + linksToAdd
                #???
