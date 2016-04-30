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

def main():
    startTime = datetime(2016,4,30,8)
    endTime = datetime(2016,5,2,18)

    recom = Recommender()
    recom.setTimeInterval(startTime,endTime)
    recom.setHabit({"0":90,"1":40,"2":50})
    recom.setBudget(1) # allow 1,2,3
    travelList = recom.recommend()
    print(travelList)

if __name__ == '__main__':
    main()
