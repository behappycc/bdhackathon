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

import os
import web_util
import json

srcDir = os.path.dirname(os.path.realpath(__file__))

class View():
    def __init__(self,name,term):
        self.name = name

        self.popularity = term["popularity"]
        self.coord = term["coord"]
        self.topicList = term["topic"]

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

        self.candidateList = []
        for term in terms:
            view = View(term,terms[term])
            self.candidateList.append(view)

    def setTimeInterval(self,start,end):
        self.startTime = start
        self.endTime = end

        #TODO
        self.travelDays = 3

    def setHabit(self,habitDict):
        self.habitDict = habitDict

    def setLocation(self,location):
        self.location = location

    def setBudget(self,budget):
        self.budget = budget

    def recommend(self):
        travelList = []
        for day in range(self.travelDays):
            if day == 0: # The first day, start from airport
                print("First Day.")
            elif day == self.travelDays-1: # The last day, keep 6 hours in airport
                print("Last Day")
            travelList.append([])

        return travelList


