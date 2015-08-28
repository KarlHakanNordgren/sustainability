#############################################
#############################################
# libraries

from selenium import webdriver # for webdriving
import re # for finding text in webpages
from BeautifulSoup import BeautifulSoup # for parsing HTML
import selenium.webdriver.support.ui as ui # for waiting
import contextlib
import mechanize
import csv
import functions

#############################################
#############################################
# get postcodes

unitPostcodes = []
with(open('/Users/simon.walne/work/sustainability/postcodes.csv','r')) as f:
    for i, line in enumerate(f):
        if i> 10:
            break
        lineStr = line.strip()
        lineStr = lineStr.replace(r'\n', '')
        lineStr = lineStr.replace(r'\r', '')
        lineStrSplit = lineStr.split(',')
        if lineStrSplit[1] is not '':
            unitPostcodes.append(lineStrSplit)
        else:
            continue

unitPostcodes.pop(0)

stopTable = []
busTable = []
for unit in unitPostcodes:
    source = getSource(unit[1])
    stopTable.extend(getStopTable(source, unit[1]))
    busTable.extend(getBusTable(source, unit[1]))

#print(stopTable)
#writeFile('stopTable')
writeFile('busTable')

#crimeTable = []
#for unit in unitPostcodes:
#    source = getCrimeSource(unit[1])
#    crimeTable.append(getCrimeTable(source, unit[1]))
#writeFile('crimeTable')




