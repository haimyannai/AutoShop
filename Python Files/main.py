import concurrent
import time

from App import App
import textdistance

from Utils import connectToDB, selectFromDB


# longest common subsequence similarity
def compareGotoh(namesList, baseNameList):
    pair = None
    pairList = []
    start = time.time()
    for name in namesList:
        minDistance = float('inf')
        for baseName in baseNameList:
            base = baseName
            res = textdistance.gotoh.distance(name, baseName)
            if res < minDistance:
                minDistance = res
                pair = (name, baseName)
        pairList.append(pair)
        # print(f'Matching Pair is {pair} and the Hamming distance is: {minDistance}')
    runTime = (time.time() - start)/60
    return 'Gotoh Distance', runTime, pairList

def compareStrCmp95(namesList, baseNameList):
    pair = None
    pairList = []
    start = time.time()
    for name in namesList:
        minDistance = float('inf')
        for baseName in baseNameList:
            base = baseName
            res = textdistance.strcmp95.distance(name, baseName)
            if res < minDistance:
                minDistance = res
                pair = (name, baseName)
        pairList.append(pair)
        # print(f'Matching Pair is {pair} and the Hamming distance is: {minDistance}')
    runTime = (time.time() - start)/60
    return 'StrCmp95 Distance', runTime, pairList


if __name__ == '__main__':
    # GUI section #
    app = App()
    app.startApp()
    # dataBaseCon = connectToDB('LAPTOP-VNSLHC31', 'BraudeProject')
    # baseNamesList = selectFromDB(dataBaseCon, 'SELECT * FROM [BraudeProject].[dbo].[AllVegNames]')
    # namesList = selectFromDB(dataBaseCon, 'SELECT Prod_Name FROM [BraudeProject].[dbo].[AllProds]')
    # namesList = [name[0] for name in namesList]
    # baseNamesList = [name[0] for name in baseNamesList]
    # resultSet = []
    # CountAlg1 = CountAlg2 = 0
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     workThreads = [executor.submit(compareStrCmp95, namesList, baseNamesList), executor.submit(compareGotoh, namesList, baseNamesList)]
    #     print('Test Results:\n')
    #     for work in concurrent.futures.as_completed(workThreads):
    #         resultSet.append(work.result())
    #     Alg1, Time1, pairList1 = resultSet[0]
    #     Alg2, Time2, pairList2 = resultSet[1]
    #     print(f'Algorithm {Alg1} finish in: {Time1}')
    #     print(f'Algorithm {Alg2} finish in: {Time2}')
    #     print(f'Results Differences:')
    #     for set1, set2 in zip(pairList1, pairList2):
    #         if set1[1] != set2[1]:
    #             print('------------------------------')
    #             print(f'Algorithm {Alg1} result: {set1}')
    #             print(f'Algorithm {Alg2} result: {set2}')
    #             ans = int(input(f'Press 1 for {Alg1} Press 2 for {Alg2}'))
    #             if ans == 1:
    #                 CountAlg1 = CountAlg1 + 1
    #             if ans == 2:
    #                 CountAlg2 = CountAlg2 + 1
    #             print('------------------------------')
    #     if CountAlg1 > CountAlg2:
    #         print(f'Winner is {Alg1} with {CountAlg1} wins compare to {Alg2} with {CountAlg2}')
    #     else:
    #         print(f'Winner is {Alg2} with {CountAlg2} wins compare to {Alg1} with {CountAlg1}')


