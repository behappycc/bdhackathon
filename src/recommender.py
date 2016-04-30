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



class Recommender():
    def __init__(self):
        self.startTime = None
        self.endTime = None
        self.habitDict = {}
        self.location = None
        self.budget = 0

    def setTimeInterval(self,start,end):
        self.startTime = start
        self.endTime = end

    def setHabit(self,habitDict):
        self.habitDict = habitDict

    def setLocation(self,location):
        self.location = location

    def setBudget(self,budget):
        self.budget = budget

    def recommend(self):
        pass

