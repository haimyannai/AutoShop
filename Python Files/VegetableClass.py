
class Vegetable:
    """
          A class used to represent Vegetable

          ...

          Attributes
          ----------

          vegName : str
              The name of the website = Kishurit

          vegPrice : str
              The price of the vegetable

          vegUnit : str
              The unit of the vegetable

          webSite : str
              The website that this vegetable is sold

          baseProd : str
              The base name of a vegetable that is mostly close to in terms of meaning


          Methods
          -------
          printVegetableDetails(self)
              Prints the vegetable details - name, price, unit, website, base name

          getRow(self)
              Returns a tuple of the vegetable details (name, price, unit, website, base name)

       """
    def __init__(self, name, price, unit, webSite, baseProd,   prodIdWeb=None, link=None):
        """
                Parameters
                ----------
                name : str
                    The name of the Vegetable
                price : str
                    The price that the Vegetable is sold for
                unit : str
                    The unit that the vegetable is sold for
                webSite : str
                    The website that the vegetable came from
                baseProd : str
                    The base name of a vegetable that this vegetable is mostly close to in terms of meaning

                """
        self.vegName = name
        self.vegPrice = price
        self.vegUnit = unit
        self.webSite = webSite
        self.baseProd = baseProd
        self.prodIdWeb = prodIdWeb
        self.Checked = False
        self.link = link


    def printVegetableDetails(self):
        """Prints the vegetable details - name, price, unit, website, base name
        """
        print(self.vegName)
        print(str(self.vegPrice))
        print(self.vegUnit)
        print(self.webSite)
        print(self.baseProd)
        print(self.prodIdWeb)

    def getRow(self):
        """Returns a tuple of the vegetable details (name, price, unit, website, base name)
               """
        return \
        (self.vegName, self.vegUnit, float(self.vegPrice), self.webSite, self.baseProd, self.prodIdWeb, self.link, self.Checked)
