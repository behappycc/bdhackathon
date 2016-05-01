#-------------------------------------------------------------------------------
# Name:        璅∪?1
# Purpose:
#
# Author:      b9890_000
#
# Created:     30/04/2016
# Copyright:   (c) b9890_000 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from datetime import datetime

from recommender import Recommender
import web_util

def main():
    startTime = datetime(2016,4,30,8)
    endTime = datetime(2016,5,1,18)

    recom = Recommender()
    recom.setTimeInterval(startTime,endTime)
    recom.setHabit({"0":90,"1":40,"2":50})
    recom.setBudget(1) # allow 1,2,3
    travelList = recom.recommend()
    print(travelList)

    day = 1
    travelDict = {}
    for _list in travelList:
        travelDict[day] = {}
        for spot in _list:
            print(spot)
            travelDict[day][spot.name] = {"coord":spot.coord,"popularity":spot.popularity,"priceLevel":spot.priceLevel,"topic":spot.topicList,"order":spot.order}
        day += 1
    web_util.write_json(travelDict,"travelList.json")

if __name__ == '__main__':
    main()
