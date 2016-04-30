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
import math
from datetime import datetime

srcDir = os.path.dirname(os.path.realpath(__file__))

def rad(d):
        return d*math.pi/180.0

def distance(spot1,spot2):
    lat1, lng1 = spot1.coord
    lat2, lng2 = spot2.coord
    radlat1=rad(lat1)
    radlat2=rad(lat2)
    a=radlat1-radlat2
    b=rad(lng1)-rad(lng2)

    s=2*math.asin(math.sqrt(math.pow(math.sin(a/2),2)+math.cos(radlat1)*math.cos(radlat2)*math.pow(math.sin(b/2),2)))
    earth_radius=6378.137
    s=s*earth_radius

    if s<0:
        return -s
    else:
        return s


class View():
    def __init__(self,name,term):
        self.name = name

        self.popularity = term["popularity"]
        self.coord = term["coord"]
        self.topicList = term["topic"]
        self.priceLevel = term["priceLevel"]
        self.order = -1

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

class Recommender():
    def __init__(self):
        self.startTime = None
        self.endTime = None
        self.habitDict = {}
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
            for topic in terms[term]["topic"]:
                if topic == "0":
                    self.restaurantList.append(view)
                elif topic == "6":
                    self.taxfreeList.append(view)
                elif topic == "7":
                    self.airportList.append(view)
                elif topic == "8":
                    self.hotelList.append(view)
                else:
                    if view not in self.spotList:
                        self.spotList.append(view)

    def setTimeInterval(self,start,end):
        self.startTime = start
        self.endTime = end

        self.travelDays = (end-start).days + 1
        print("travle days = ",self.travelDays)

    def setHabit(self,habitDict):
        self.habitDict = habitDict

    def setBudget(self,level):
        if level not in [1,2,3]:
            self.budget = 2
        else:
            self.budget = level

    def evaluate(self,currentSpot,termList,habitDict=None):
        returnList = []
        disWeight = 0.02
        popWeight = 0.1
        habWeight = 5
        priWeight = 2

        for term in termList:
            # Calculate distance
            dis = distance(currentSpot,term)

            # Calculate popularity
            popularity = term.popularity

            # Calculate habit
            if not habitDict:
                habit = 0
            else:
                habit = 0
                for h in habitDict:
                    if h in term.topicList:
                        habit += habitDict[h]

            # Calculate price
            if self.budget == 1:
                if term.priceLevel in [0,1]:
                    price = 5
                elif term.priceLevel in [2,3]:
                    price = 3
                else:
                    price = 1
            elif self.budget == 2:
                if term.priceLevel in [0,1]:
                    price = 3
                elif term.priceLevel in [2,3]:
                    price = 5
                else:
                    price = 2
            elif self.budget == 3:
                if term.priceLevel in [0,1]:
                    price = 1
                elif term.priceLevel in [2,3]:
                    price = 3
                else:
                    price = 5

            #print(currentSpot,term,"dis = ",dis," pop = ",popularity," price = ",price," habit = ",habit)
            value = disWeight*dis + popWeight*popularity + priWeight*price + habWeight*habit
            #print("value = ",value)
            returnList.append((term,value))

        if not returnList:
            return None
        else:
            returnList = sorted(returnList,key=lambda x: x[1])
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
            order = 0
            if day == 0: # The first day
                print("First Day.")
                # start from airport
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # 09:00~12:00 spot
                if self.startTime.hour < 12:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 12:00~1330 launch
                if self.startTime.hour < 14:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 1330~1600 spot
                if self.startTime.hour < 16:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 1600~1800 spot
                if self.startTime.hour < 18:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 1800~1930 dinner
                if self.startTime.hour < 20:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 1930~2100 spot
                if self.startTime.hour < 21:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 2100~... sleep
                currentSpot = self.evaluate(currentSpot,self.hotelList)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

            elif day == self.travelDays-1: # The last day, keep 6 hours in airport
                print("Last Day.")
                # 09:00~12:00 spot
                if self.endTime.hour-3 > 9:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 12:00~1330 launch
                if self.endTime.hour-3 > 12:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 1330~1600 spot
                if self.endTime.hour-3 > 14:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # 18:00~1930 launch
                if self.endTime.hour-3 > 18:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    currentSpot.order = order
                    order += 1
                    dayList.append(currentSpot)

                # Shop at tax-free shop 1hr
                currentSpot = self.evaluate(currentSpot,self.taxfreeList)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # end to airport and keep 2hr for waiting check in
                currentSpot = self.airportList[0]
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

            else:
                print("Middle Day.")
                # 09:00~12:00 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # 12:00~1330 launch
                currentSpot = self.evaluate(currentSpot,self.restaurantList)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # 1330~1600 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # 1600~1800 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # 1800~1930 dinner
                currentSpot = self.evaluate(currentSpot,self.restaurantList)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # 1930~2100 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)

                # 2100~... sleep
                currentSpot = self.evaluate(currentSpot,self.hotelList)
                currentSpot.order = order
                order += 1
                dayList.append(currentSpot)
            travelList.append(dayList)

        return travelList


