from KishuritClass import Kishurit
from SultanClass import Sultan
from DovMarket import DovMarket
from Utils import deleteFromDB, selectFromDB, insertToDB, updateDB
import time
from datetime import datetime
import concurrent.futures


# Link to 'משק כישורית' site.
def importData(dataBaseCon, baseNamesList):
    # Devide to Threads
    # deleteFromDB(dataBaseCon, deleteQuery="DELETE FROM AllProds")
    kishurit = Kishurit(baseNamesList)
    sultan = Sultan(baseNamesList)
    dov = DovMarket(baseNamesList)
    startTime = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        workThreads = [executor.submit(kishurit.startScrape), executor.submit(sultan.startScrape), executor.submit(dov.startScrape)]
        for work in concurrent.futures.as_completed(workThreads):
            checkBeforeInsert(dataBaseCon, work.result()[1])
            print(f'Thread {work.result()[0]} Finish')
        deleteFromDB(dataBaseCon, deleteQuery="DELETE FROM Updates")
        lastUpdate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        insertToDB(dataBaseCon, data=lastUpdate, insertQuery='INSERT INTO Updates (Last_Update)' \
                                                             'VALUES (?);')
        endTime = time.time()
        print('#####  ' + str((endTime - startTime) / 60) + '  ####')
        return lastUpdate


def checkBeforeInsert(dataBaseCon, newVegList):
    # deleteFromDB(dataBaseCon, 'DELETE FROM AllProds')
    for veg in newVegList:
        row = veg.getRow()
        unit = row[1].replace("'", "")
        prodName = row[0].replace("'", "")
        prodName = prodName.replace('`', '')
        updateQuery = f"UPDATE [BraudeProject].[dbo].[AllProds]" \
                      f"SET Prod_Id_Web ='{row[5]}' , Prod_Unit ='{unit}' , Prod_Price = {row[2]}" \
                      f"WHERE Prod_Name = '{prodName}' AND Prod_Web = '{row[3]}'"
        if not updateDB(dataBaseCon, updateQuery):
            insertQuery = 'INSERT INTO AllProds (Prod_Name,Prod_Unit,Prod_Price,Prod_Web,Base_Prod,Prod_Id_Web,Prod_Id_Web_Link,Checked)' \
                          'VALUES (?,?,?,?,?,?,?,?);'
            insertToDB(dataBaseCon, row, insertQuery)


def insertAdminData(dataBaseCon, data):

    for row in data:
        prodName = row[0].replace("'", "")
        updateQuery = f"UPDATE [BraudeProject].[dbo].[AllProds]" \
                      f"SET Base_Prod ='{row[4]}' ,Checked = '{row[7]}'" \
                      f"WHERE Prod_Name = '{prodName}' AND Prod_Web = '{row[3]}'"
        updateDB(dataBaseCon, updateQuery)
    lastUpdate = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    insertToDB(dataBaseCon, data=lastUpdate, insertQuery='INSERT INTO Updates (Last_Update)' \
                                                         'VALUES (?);')
    print("Insert Admin Finish")
    return lastUpdate
