from Compare import compareStrCmp95
from Utils import connectionChecker, insertToDB
from bs4 import BeautifulSoup
import re
from VegetableClass import Vegetable
import time


class DovMarket:
    """
       A class used to represent the 'Kishurit' Website

       ...

       Attributes
       ----------

       webName : str
           The name of the website = Dov

       linkList : list
           A list that contains all pages links of Kishurit website

       resultVegList : list
           A list that contains all the vegetables in Kishurit website

       baseNameList : list
           A list that contains all the basic names of vegetables (retrieved from DATA BASE)


       Methods
       -------
       startScrape(self, sem, dataBaseCon)
           Starts scraping each page link in Kishurit website.The start function of the threads

       getLinkData(self, link)
           Retrieve the link raw data of unit, price and name of a vegetable

       getVegDetails(self, title, price)
           Creates a Vegetable instance


    """

    def __init__(self, baseNameList):
        """
        Parameters
        ----------
        baseNameList : list
            A list of basic names of vegetable (retrieved from DATA BASE)
        """
        self.webName = 'Dov'
        self.linkList = []
        self.linkList.append('https://dovdov.co.il/products/category/yrqwt-32')
        self.linkList.append('https://dovdov.co.il/products/category/yrq-wsby-tybwl-71')
        self.resultVegList = []
        self.baseNameList = baseNameList

    def startScrape(self):
        """Starts scraping each page link in Kishurit website.The start function of the threads.
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
        for i, div in enumerate(html.find_all('div', attrs={'class': 'col-sm-6 col-lg-3 col-md-4 col-xs-6 views-row'})):
            name = div.find('div', attrs={'class':'field field--name-title field--type-string field--label-hidden field--item'}).text
            price = div.div.text
            price = price.replace(' ', '')
            price = price.replace('\n', '')
            prodIdWeb = div.find('button', attrs={'class':'use-ajax-submit button button--primary js-form-submit form-submit btn-primary btn'}).get('id')
            self.resultVegList.append(self.getVegDetails(name, price, prodIdWeb, link))

    def getVegDetails(self, name, price, prodIdWeb, link):
        """Creates a Vegetable instance
               Parameters
               ----------
               name : str
                   Name of vegetable

               price : str
                   The price of the vegetable and the unit
        """
        unit = ''.join(re.sub("\d+\.\d+|[₪,',ל]", "", price))
        price = ''.join(re.findall("\d+\.\d+", price))
        name = name.replace("'", "")
        baseName = compareStrCmp95(name, self.baseNameList)
        return Vegetable(name, price, unit, self.webName, baseName, prodIdWeb, link)
