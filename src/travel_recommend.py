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
    startTime = datetime(2016,4,30,18)
    endTime = datetime(2016,5,2,22)

    recom = Recommender()
    recom.setTimeInterval(startTime,endTime)
    recom.setHabit({"2"})
    recom.setLocation("")
    recom.setBudget(50000)
    travelList = recom.recommend()
    print(travelList)

if __name__ == '__main__':
    main()
