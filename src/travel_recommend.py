#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      b9890_000
#
# Created:     30/04/2016
# Copyright:   (c) b9890_000 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from recommender import Recommender

def main():
    recom = Recommender()
    recom.setTimeInterval(0,1)
    recom.setHabit({})
    recom.setLocation("")
    recom.setBudget(50000)
    print(recom.recommend())

if __name__ == '__main__':
    main()
