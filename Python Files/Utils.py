import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import pyodbc


def connectionChecker(link, webName):
    """
       : Handle http request to a given link
       :param link: The link to get.
       :param webName: Website name.
       :return session.get: The session.
       """
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"}
        session = requests.Session()
        retry = Retry(connect=5, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session.get(link, headers=headers)
    except requests.exceptions.RequestException:
        print("Connection Failure  " + webName)
        exit(1)
        return None


def connectToDB(serverName, dbName):
    """
       : Establish a connection to a Data - Base
       :param serverName: The name of the server.
       :param dbName: The name of the Data - Base.
       :return session.get: The session.
       """
    try:
        # Establish SQL server connection to insert data
        # Define our connection string
        connect = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                                                     SERVER=' + serverName + '; \
                                                     DATABASE=' + dbName + ';\
                                                     Trusted_Connection=yes;')
        # Create the connection cursor
        return connect.cursor()
    except Exception:
        print("Cannot connect to DB Failuer")
        exit(1)


def insertToDB(dataBaseCon, data, insertQuery):
    """
          : Handle insert query's to Data - Base.
          :param dataBaseCon: The connection to Data - Base.
          :param data: The data to insert.
          :param insertQuery: The insert query to preform.
          """
    try:
        dataBaseCon.execute(insertQuery, data)
        dataBaseCon.commit()
    except Exception as e:
        print(insertQuery + "  -> Fail")
        print(e)


def deleteFromDB(dataBaseCon, deleteQuery):
    """
          : Handle delete query's to Data - Base.
          :param dataBaseCon: The connection to Data - Base.
          :param deleteQuery: The delete query to preform.
          """
    try:
        dataBaseCon.execute(deleteQuery)
        dataBaseCon.commit()
    except Exception as e:
        print(deleteQuery + "  -> Fail")
        print(e)


def selectFromDB(dataBaseCon, selectQuery, queue=None):
    """

          : Handle select query's to Data - Base.
          :param queue: queue to insert data (for threads)
          :param dataBaseCon: The connection to Data - Base.
          :param selectQuery: The select query to preform.
          :return Data: A list of the data.
          """
    try:
        if queue is not None:
            dataBaseCon.execute(selectQuery)
            for row in dataBaseCon:
                queue.put(row)
        else:
            data = []
            dataBaseCon.execute(selectQuery)
            for row in dataBaseCon:
                data.append(row)
            return data
    except Exception as e:
        print(e)
        print(selectQuery + '  -> Fail')


def updateDB(dataBaseCon, updateQuery):
    try:
        dataBaseCon.execute(updateQuery)
        if dataBaseCon.rowcount == 0:
            return False
    except Exception as e:
        print(e)
        print(updateQuery + '  -> Fail')
        return False
    return True
