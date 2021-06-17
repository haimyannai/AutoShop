import textdistance

def compareStrCmp95(name, baseNameList):
    minDistance = float('inf')
    for baseName in baseNameList:
        res = textdistance.strcmp95.distance(name, baseName)
        if res < minDistance:
            minDistance = res
            base = baseName
    return base


# def copmareByPerecent(name, baseName):
#     """
#     : compare two veg names according to continues characters
#     :param name: the original name of the veg.
#     :param baseName: the 'base' name of a veg.
#     :return matchPercent: the percentage of the two products resemblance.
#     """
#     matchPercent = 0
#     count = 0
#     for A, B in zip(baseName, name):
#         if A == B:
#             count += 1
#         else:
#             break
#     matchPercent = float(count / min(len(name), len(baseName)))
#     return matchPercent
