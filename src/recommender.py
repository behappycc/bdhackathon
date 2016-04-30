#-------------------------------------------------------------------------------
# Name:        ??1
# Purpose:
#
# Author:      b9890_000
#
# Created:     30/04/2016
# Copyright:   (c) b9890_000 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import web_util
import json
import random
from datetime import datetime

srcDir = os.path.dirname(os.path.realpath(__file__))

class View():
    def __init__(self,name,term):
        self.name = name

        self.popularity = term["popularity"]
        self.coord = term["coord"]
        self.topicList = term["topic"]

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Recommender():
    def __init__(self):
        self.startTime = None
        self.endTime = None
        self.habitDict = {}
        self.location = None
        self.budget = 0

        self.loadTerms()

    def loadTerms(self):
        print(srcDir)
        termFile = os.path.join(srcDir,"nlp","term.json")
        terms = web_util.load_json(termFile)
        categoryFile = os.path.join(srcDir,"nlp","category.json")
        categories = web_util.load_json(categoryFile)

        self.restaurantList = []
        self.spotList = []
        self.shoppingList = []
        self.taxfreeList = []
        self.airportList = []
        self.hotelList = []

        for term in terms:
            view = View(term,terms[term])
            if "0" in terms[term]["topic"]:
                self.restaurantList.append(view)
            elif "6" in terms[term]["topic"]:
                self.taxfreeList.append(view)
            elif "7" in terms[term]["topic"]:
                self.airportList.append(view)
            elif "8" in terms[term]["topic"]:
                self.hotelList.append(view)
            else:
                self.spotList.append(view)

    def setTimeInterval(self,start,end):
        self.startTime = start
        self.endTime = end

        self.travelDays = (end-start).days + 1
        print("travle days = ",self.travelDays)

    def setHabit(self,habitDict):
        self.habitDict = habitDict

    def setLocation(self,location):
        self.location = location

    def setBudget(self,budget):
        self.budget = budget

    def evaluate(self,currentSpot,termList,habitDict=None):
        returnList = []

        if not habitDict:
            for term in termList:
                returnList.append((term,random.randint(1,10)))

            returnList = sorted(returnList,key=lambda x: x[1])
        else:
            for term in termList:
                returnList.append((term,random.randint(1,10)))

            returnList = sorted(returnList,key=lambda x: x[1])

        if not returnList:
            return None
        else:
            tlist = returnList[0][0].topicList
            if "7" not in tlist and "8" not in tlist:
                # not remove airport and hotel
                termList.remove(returnList[0][0])

            return returnList[0][0]

    def recommend(self):
        travelList = []
        currentSpot = self.airportList[0] # default airport

        for day in range(self.travelDays):
            dayList = []
            if day == 0: # The first day
                print("First Day.")
                # start from airport
                dayList.append(self.airportList[0])

                # 09:00~12:00 spot
                if self.startTime.hour < 12:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    dayList.append(currentSpot)

                # 12:00~1330 launch
                if self.startTime.hour < 14:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    dayList.append(currentSpot)

                # 1330~1600 spot
                if self.startTime.hour < 16:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    dayList.append(currentSpot)

                # 1600~1800 spot
                if self.startTime.hour < 18:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    dayList.append(currentSpot)

                # 1800~1930 dinner
                if self.startTime.hour < 20:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    dayList.append(currentSpot)

                # 1930~2100 spot
                if self.startTime.hour < 21:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    dayList.append(currentSpot)

                # 2100~... sleep
                currentSpot = self.evaluate(currentSpot,self.hotelList)
                dayList.append(currentSpot)

            elif day == self.travelDays-1: # The last day, keep 6 hours in airport
                print("Last Day.")
                # 09:00~12:00 spot
                if self.endTime.hour-3 > 9:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    dayList.append(currentSpot)

                # 12:00~1330 launch
                if self.endTime.hour-3 > 12:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    dayList.append(currentSpot)

                # 1330~1600 spot
                if self.endTime.hour-3 > 14:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    dayList.append(currentSpot)

                # 18:00~1930 launch
                if self.endTime.hour-3 > 18:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    dayList.append(currentSpot)

                # Shop at tax-free shop 1hr
                currentSpot = self.evaluate(currentSpot,self.taxfreeList)
                dayList.append(currentSpot)

                # end to airport and keep 2hr for waiting check in
                dayList.append(self.airportList[0])

            else:
                print("Middle Day.")
                # 09:00~12:00 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                dayList.append(currentSpot)

                # 12:00~1330 launch
                currentSpot = self.evaluate(currentSpot,self.restaurantList)
                dayList.append(currentSpot)

                # 1330~1600 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                dayList.append(currentSpot)

                # 1600~1800 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                dayList.append(currentSpot)

                # 1800~1930 dinner
                currentSpot = self.evaluate(currentSpot,self.restaurantList)
                dayList.append(currentSpot)

                # 1930~2100 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                dayList.append(currentSpot)

                # 2100~... sleep
                currentSpot = self.evaluate(currentSpot,self.hotelList)
                dayList.append(currentSpot)
            travelList.append(dayList)

        return travelList


