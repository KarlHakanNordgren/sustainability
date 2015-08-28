#############################################
#############################################
# 

def writeFile(objectName):
    with open('/Users/simon.walne/work/sustainability/'+ objectName + '.csv', "wb") as f:
        writer = csv.writer(f)
        writer.writerows(eval(objectName))

def getCrimeSource(postCode):
    with contextlib.closing(webdriver.Firefox()) as driver:
        driver.get('http://www.ukcrimestats.com/')
        wait = ui.WebDriverWait(driver,10)
        driver.find_element_by_id('globalsearch').click()
        driver.find_element_by_id('globalsearch').send_keys(postCode)
        driver.find_element_by_xpath('//*[@id="index_searchbox"]/form/table/tbody/tr[1]/td[2]/input').click()
        wait.until(lambda driver: driver.find_element_by_id('tablediv'))
        source = (driver.page_source).encode('utf-8')
    return source;

def getHeader(headTag):
    trTags = headTag.findAll("tr")
    for trTag in trTags:
        rowTags = trTag.findAll("th")
        row = [str(rowTag.contents) for rowTag in rowTags]
        row = [element.replace(r'<b>', '').replace(r'</b>', '').replace(r'[', '').replace(r']', '') for element in row]
    return row;

def getBodyer(bodyTag):
    trTags = bodyTag.findAll("tr")
    body = []
    for trTag in trTags:
        tdTags = trTag.findAll("td")
        row = [tdTag.contents[0] for tdTag in tdTags]
        body.append(row)
    return body;

def getCrimeTable(source, postCode):
    "This function does some stuff"
    soup = BeautifulSoup(source)
    divTag = soup.find('div', attrs = {"id":"tablediv"})
    theadTag = divTag.find("thead")
    head = getHeader(theadTag)
    tbodyTag = divTag.find("tbody")
    body = getBodyer(tbodyTag)
    all = [head] + body
    return all;

def getSource(postCode):
    br = mechanize.Browser()
    br.open('https://tfl.gov.uk/maps/bus')
    for form in br.forms():
        for control in form.controls:
            if control.name == 'Input':
                br.form = form
                break
    br["Input"] = postCode
    response2 = br.submit()
    source = response2.read()

    #with contextlib.closing(webdriver.Firefox()) as driver:
    #    driver.get('https://tfl.gov.uk/maps/bus')
    #    wait = ui.WebDriverWait(driver,10)
    #    driver.find_element_by_xpath('//*[@id="Input"]').send_keys(postCode)
    #    driver.find_element_by_xpath('//*[@id="search-filter-form"]/div[2]/input').click()
    #    wait.until(lambda driver: driver.find_element_by_id('nearby-list-container'))
    #    source = (driver.page_source).encode('utf-8')
    #print('End of getSource')

    return source;

def getStopTable(source, postCode):
    "This function does some stuff"
    soup = BeautifulSoup(source)

    stopTag = soup.find('ul', attrs={"class" : "nearby-list"})
    stopLat = stopTag["data-search-lat"]
    stopLon = stopTag["data-search-lon"]
    stopTable = [postCode, float(stopLat), float(stopLon)]
    return stopTable;

def getBusTable(source, postCode):
    "This function does some stuff"
    
    soup = BeautifulSoup(source)

    nearbyListResultTags = soup.findAll('li', attrs={"class" : "nearby-list-result"})

    destinationTable = []
    for result in nearbyListResultTags:
        nearbyListHeadingTags = result.findAll('span', attrs = {"class":"nearby-list-heading"})
	for heading in nearbyListHeadingTags:
            stopName = heading.text
            destinationTable.append([postCode, stopName, float(result['data-lon']), float(result['data-lat'])])
    return destinationTable;

