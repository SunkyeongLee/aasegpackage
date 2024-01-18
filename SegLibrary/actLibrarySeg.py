# Created by Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com / sunkyong9768@gmail.com

import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import csv
import os
from ast import literal_eval
import pandas as pd
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def dataInitiator():
    api2.importConfigFile(resource_path("aanalyticsact_auth.json"))
    logger = api2.Login()
    logger.connector.config

def readCSV(csvFile):
    lines = open(csvFile).readlines()
    listCsv = []
    for line in lines[1:]:
        listCsv.append(line.split('\n')[0])

    return listCsv

def createSegment(jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header
    
    return ags.createSegment(jsonFile)

def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile

def pullFromLib(ownerId, segment):
    segJson = readJson(segment)
    segJson_temp = deepcopy(segJson)
    newName = segJson_temp['name'] + ' (Pulled from Lib)'

    segJson['name'] = newName
    segJson["owner"]["id"] = ownerId

    return segJson
