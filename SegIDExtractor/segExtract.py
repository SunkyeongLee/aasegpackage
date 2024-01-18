import aanalytics2 as api2
import pandas as pd
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def dataInitiator():
    api2.importConfigFile(resource_path("aanalyticsact_auth.json"))
    logger = api2.Login()
    logger.connector.config

def extractAction(keyword):
    ags = api2.Analytics("samsun0")
    ags.header
    data = ags.getSegments(keyword, verbose=True)

    return data

def segIdExtractor(keywordList, where_to_save):
    dataInitiator()

    df = pd.DataFrame()
    for keyword in keywordList:
        print(keyword)
        segID = extractAction(keyword).drop('description', axis=1)
        segID.insert(0, "Keyword", keyword, True)
    
        df = pd.concat([df, segID], ignore_index=True)
    
    df.to_csv(where_to_save + '\segIDList.csv')
    
    data = pd.read_csv(where_to_save + '\segIDList.csv', encoding='utf-8')
    data.to_csv(where_to_save + '\segIDList.csv', encoding='utf-8-sig')

def readCSV(csvFile):
    lines = open(csvFile).readlines()
    listCsv = []
    for line in lines[1:]:
        listCsv.append(line.split('\n')[0])

    return listCsv