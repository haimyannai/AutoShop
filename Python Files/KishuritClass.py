from Compare import compareStrCmp95
from Utils import connectionChecker, insertToDB
from bs4 import BeautifulSoup
import re
from VegetableClass import Vegetable
import time


class Kishurit:
    """
       A class used to represent the 'Kishurit' Website

       ...

       Attributes
       ----------

       webName : str
           The name of the website = Kishurit

       pageLink : str
           The page link of Kishurit website

       insertQuery : str
           The query to insert new vegetable to the DB

       linkList : list
           A list that contains all pages links of Kishurit website

       resultVegList : list
           A list that contains all the vegetables in Kishurit website

       baseNameList : list
           A list that contains all the basic names of vegetables (retrieved from DATA BASE)
       pageCount : int
           The number of pages in 'Kishurit' website

       Methods
       -------
       startScrape(self, sem, dataBaseCon)
           Starts scraping each page link in Kishurit website.The start function of the threads

       getLinkData(self, link)
           Retrieve the link raw data of unit, price and name of a vegetable

       getVegDetails(self, title, price)
           Creates a Vegetable instance

       unitSelector(self, unit)
           Defines the unit of the vegetable

       createPagesLinks(self)
           Creates the pages links in Kishurit website


    """

    def __init__(self, baseNameList, pageCount=3):
        """
        Parameters
        ----------
        baseNameList : list
            A list of basic names of vegetable (retrieved from DATA BASE)
        pageCount : int, optional
            The number of pages in Kishurit website. by default 3 pages
        """
        self.webName = 'Kishurit'
        self.pageLink = 'http://www.meshek-kishorit.org/47955-%D7%99%D7%A8%D7%A7%D7%95%D7%AA?page='
        self.pageCount = pageCount
        self.linkList = []
        self.resultVegList = []
        self.createPagesLinks()
        self.baseNameList = baseNameList

    def startScrape(self):
        """Starts scraping each page link in Kishurit website.The start function of the threads.
               Parameters
               ----------
               sem : threading.Semaphore
                   Semaphore to synchronize the threads when inserting to DB

               dataBaseCon : pyodbc.connect.cursor
                   The connection to the DB
        """
        for link in self.linkList:
            self.getLinkData(link)
        return self.webName, self.resultVegList

    def getLinkData(self, link):
        """Retrieve the link raw data of unit, price and name of a vegetable.
                  Parameters
                  ----------
                  link : str
                      String representation of webpage
        """
        page = connectionChecker(link, self.webName)
        html = BeautifulSoup(page.content, features="html.parser")
        for div in html.select('div[class*="layout_list_item css_class_479"]'):
            title = div.find('div', attrs={'class': 'list_item_title_with_brand'}).text
            price = div.find('a', attrs={'class': 'price'}).text
            prodIdWeb = div.get('id')
            self.resultVegList.append(self.getVegDetails(title, price, prodIdWeb, link))

    def getVegDetails(self, title, price, prodIdWeb, link):
        """Creates a Vegetable instance
               Parameters
               ----------
               title : str
                   Name and unit of vegetable

               price : str
                   The price of the vegetable
        """
        price = ''.join(re.findall(r'\d+', price))
        title = title.replace("*במבצע*", "")
        title = title.replace("*זוג במבצע*", "")  # לנסות להשתמש בביטוי רגולרי
        name = title[:title.find('(')]
        name = name.split()
        name = ' '.join(name)
        unit = title[title.find('(') + 1:title.find(')')]
        unit = self.unitSelector(unit)
        baseName = compareStrCmp95(name, self.baseNameList)
        name = name.replace("'", "")
        name = name.replace("'", "")
        name = name.replace('`', '')
        return Vegetable(name, price, unit, self.webName, baseName, prodIdWeb, link)

    def unitSelector(self, unit):
        """Retrieve the link raw data of unit, price and name of a vegetable.
                  Parameters
                  ----------
                  unit : str
                      String of the unit of a vegetable
                  """
        if unit.find('ק"ג') != -1:
            return 'ק"ג'
        elif unit.find("יח") != -1:
            indexNumber = re.search(r"\d", unit)  # 2 יחידות לדוגמא
            if indexNumber:
                return unit[indexNumber.start()] + ' ' + "יח"
            else:
                return "יח"
        else:
            return "יח"

    def createPagesLinks(self):
        """Creates the pages links in Kishurit website.
                    """
        for i in range(self.pageCount):
            link = self.pageLink + str(i + 1)
            self.linkList.append(link)
