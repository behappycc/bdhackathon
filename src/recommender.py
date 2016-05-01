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
        self.priceLevel = 0#term["priceLevel"]
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
        termFile = os.path.join(srcDir,"nlp","new_term.json")
        terms = web_util.load_json(termFile)
        airportFile = os.path.join(srcDir,"nlp","airport.json")
        airport = web_util.load_json(airportFile)
        hotelFile = os.path.join(srcDir,"nlp","hotel.json")
        hotels = web_util.load_json(hotelFile)

        self.restaurantList = []
        self.spotList = []
        self.hotelList =[]

        for air in airport:
            self.airport = View((air),airport[air])

        for hotel in hotels:
            view = View(hotel,hotels[hotel])
            self.hotelList.append(view)

        for term in terms:
            if terms[term]["popularity"] == 0: # ignore
                continue

            view = View(term,terms[term])
            for topic in view.topicList:
                if topic[0] == "0":
                    self.restaurantList.append(view)
                elif topic[0] == "1":
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
                    if h in term.topicList[0]:
                        habit += int(habitDict[h])

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
            recommendSpot = returnList[0][0]
            tlist = [x[0] for x in recommendSpot.topicList]
            termList.remove(recommendSpot)

            return returnList[0][0]

    def addSpot(self,spot):
        if spot:
            spot.order = self.order
            self.order += 1
            self.dayList.append(spot)

    def recommend(self):
        travelList = []
        currentSpot = self.airport # default airport

        for day in range(self.travelDays):
            self.dayList = []
            self.order = 0
            if day == 0: # The first day
                print("First Day.")
                # start from airport
                self.addSpot(currentSpot)

                # 09:00~12:00 spot
                if self.startTime.hour < 12:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    self.addSpot(currentSpot)

                # 12:00~1330 launch
                if self.startTime.hour < 14:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    self.addSpot(currentSpot)

                # 1330~1600 spot
                if self.startTime.hour < 16:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    self.addSpot(currentSpot)

                # 1600~1800 spot
                if self.startTime.hour < 18:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    self.addSpot(currentSpot)

                # 1800~1930 dinner
                if self.startTime.hour < 20:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    self.addSpot(currentSpot)

                # 1930~2100 spot
                if self.startTime.hour < 21:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    self.addSpot(currentSpot)

                # 2100~... sleep
                currentSpot = self.evaluate(currentSpot,self.hotelList)
                self.addSpot(currentSpot)

            elif day == self.travelDays-1: # The last day, keep 6 hours in airport
                print("Last Day.")
                # 09:00~12:00 spot
                if self.endTime.hour-3 > 9:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    self.addSpot(currentSpot)

                # 12:00~1330 launch
                if self.endTime.hour-3 > 12:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    self.addSpot(currentSpot)

                # 1330~1600 spot
                if self.endTime.hour-3 > 14:
                    currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                    self.addSpot(currentSpot)

                # 18:00~1930 launch
                if self.endTime.hour-3 > 18:
                    currentSpot = self.evaluate(currentSpot,self.restaurantList)
                    self.addSpot(currentSpot)

                # end to airport and keep 3hr for waiting check in
                currentSpot = self.airport
                self.addSpot(currentSpot)

            else:
                print("Middle Day.")
                # 09:00~12:00 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                self.addSpot(currentSpot)

                # 12:00~1330 launch
                currentSpot = self.evaluate(currentSpot,self.restaurantList)
                self.addSpot(currentSpot)

                # 1330~1600 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                self.addSpot(currentSpot)

                # 1600~1800 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                self.addSpot(currentSpot)

                # 1800~1930 dinner
                currentSpot = self.evaluate(currentSpot,self.restaurantList)
                self.addSpot(currentSpot)

                # 1930~2100 spot
                currentSpot = self.evaluate(currentSpot,self.spotList,habitDict=self.habitDict)
                self.addSpot(currentSpot)

                # 2100~... sleep
                currentSpot = self.evaluate(currentSpot,self.hotelList)
                self.addSpot(currentSpot)

            travelList.append(self.dayList)

        return travelList


