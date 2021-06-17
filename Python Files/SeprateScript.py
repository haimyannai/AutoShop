import sys
import json
import simplejson as json


# [{'basicName': 'תפוח', 'quantity': 2, 'realName': 'item_id_2112537', 'link': None, 'cost': '8'}
class Vegetable:
    def __init__(self, siteName, basicName, quantity, realName, link, cost):
        self.siteName = siteName
        self.basicName = basicName
        self.quantity = quantity
        self.realName = realName
        self.link = link
        self.cost = cost

    # {'basicName': 'תפוח', 'quantity': 2, 'realName': 'item_id_2112537', 'link': None, 'cost': '8'}
    def getVegDic(self):
        return {
            'supplierName': self.siteName,
            'basicName': self.basicName,
            'quantity': self.quantity,
            'realName': self.realName,
            'link': self.link,
            'cost': self.cost,

        }

    def getVegDetails(self):
        return f'Site: {self.siteName}\n' \
               f'Basic Name: {self.basicName}\n' \
               f'Quantity: {self.quantity}\n' \
               f'Cost: {self.cost}\n' \
               f'Real Name: {self.realName}\n' \
               f'Link: {self.link}\n' \
               f'\n'


def createVegList(data=sys.argv[1]):  # =sys.argv[1]):
    try:
        jsonList = json.loads(data)
        # Debug
        # jsonList = data
        kishuritDic = jsonList["purchaseList"]["prodsKishurit"]
        sultanDic = jsonList["purchaseList"]["prodsSultan"]
        dovDic = jsonList["purchaseList"]["prodsDov"]
        kishuritVegs = []
        sultanVegs = []
        dovVegs = []
        for prod in kishuritDic:
            kishuritVegs.append(
                Vegetable("Kishurit", prod["basicName"], prod["quantity"], prod["realName"], prod["link"],
                          prod["cost"]))
        for prod in sultanDic:
            sultanVegs.append(
                Vegetable("Sultan", prod["basicName"], prod["quantity"], prod["realName"], prod["link"], prod["cost"]))
        for prod in dovDic:
            dovVegs.append(
                Vegetable("Dov", prod["basicName"], prod["quantity"], prod["realName"], prod["link"], prod["cost"]))
        # with open("Stam1.txt", "w") as file:
        #     for item in kishuritVegs:
        #         file.write(item.getVegDetails())
        #     for item in sultanVegs:
        #         file.write(item.getVegDetails())
        #     for item in dovVegs:
        #         file.write(item.getVegDetails())
        #     file.write("----------------------------------")
        return kishuritVegs, sultanVegs, dovVegs
    except Exception as e:
        print(0)
        exit(0)


def compareLists(List1, List2):
    try:
        resultList = []
        totalListPrice = 0
        for veg1 in List1:
            tempVeg = None
            for veg2 in List2:
                if veg1.basicName == veg2.basicName:
                    if float(veg1.cost) <= float(veg2.cost):
                        tempVeg = veg1
                    else:
                        tempVeg = veg2
                    break
            if tempVeg:
                totalListPrice = totalListPrice + float(tempVeg.cost) * float(tempVeg.quantity)
                resultList.append(tempVeg)
            else:
                totalListPrice = totalListPrice + float(veg1.cost) * float(veg1.quantity)
                resultList.append(veg1)

        for veg2 in List2:
            tempVeg = 0
            for resVeg in resultList:
                if veg2.basicName == resVeg.basicName:
                    tempVeg = 1
                    break
            if tempVeg == 0:
                totalListPrice = totalListPrice + float(veg2.cost) * float(veg2.quantity)
                resultList.append(veg2)

        return resultList, totalListPrice
    except Exception as e:
        print(0)
        exit(0)


def findSeperation(kishurit, sultan, dov):
    try:
        kishuritSultan = []
        kishuritDov = []
        sultanDov = []
        maxItemsLists = []
        longestList = max(len(kishurit), len(sultan), len(dov))
        # Kishurit - Sultan
        if len(kishurit) is not 0 and len(sultan) is not 0:
            kishuritSultan, kishuritSultanTotal = compareLists(kishurit, sultan)
        else:
            kishuritSultan, kishuritSultanTotal = [], float('inf')
        # Kishurit - Sultan

        # Kishurit - Dov
        if len(kishurit) is not 0 and len(dov) is not 0:
            kishuritDov, kishuritDovTotal = compareLists(kishurit, dov)
        else:
            kishuritDov, kishuritDovTotal = [], float('inf')
        # Kishurit - Dov

        # Sultan - Dov
        if len(dov) is not 0 and len(sultan) is not 0:
            sultanDov, sultanDovTotal = compareLists(sultan, dov)
        else:
            sultanDov, sultanDovTotal = [], float('inf')
        # Sultan - Dov

        minTotal = float('inf')
        resultList = []
        supllierName = ''
        if len(kishuritSultan) >= longestList:
            maxItemsLists.append((kishuritSultan, kishuritSultanTotal, 'K-S'))
        if len(kishuritDov) >= longestList:
            maxItemsLists.append((kishuritDov, kishuritDovTotal, 'K-D'))
        if len(sultanDov) >= longestList:
            maxItemsLists.append((sultanDov, sultanDovTotal, "S-D"))
        for Tlist in maxItemsLists:
            if Tlist[1] < minTotal:
                resultList = Tlist[0]
                minTotal = Tlist[1]
                supllierName = Tlist[2]
        return resultList, minTotal, supllierName
    except Exception as e:
        print(0)
        exit(0)


def checkMiss(resList, checkList):
    for veg in checkList:
        flag = 0
        for resVeg in resList:
            if veg.basicName == resVeg.basicName:
                flag = 1
        if flag == 0:
            return 0
    return 1


if __name__ == '__main__':
    try:
        kishuritVegs, sultanVegs, dovVegs = createVegList()
        resList, totalSum, supplierName = findSeperation(kishuritVegs, sultanVegs, dovVegs)
        # with open('finale.txt', 'w') as file:
        #     for veg in resList:

        if resList:
            finalList = []
            for veg in resList:
                finalList.append(veg.getVegDic())
            print(json.dumps(finalList))
        else:
            print(0)
    except Exception as e:
        print(0)
    sys.stdout.flush()
