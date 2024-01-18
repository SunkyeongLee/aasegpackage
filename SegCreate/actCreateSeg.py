# Created by Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com

import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import os
import sys
from ast import literal_eval
import pandas as pd
import time

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def dataInitiator():
    api2.importConfigFile(resource_path("aanalyticsact_auth.json"))
    logger = api2.Login()
    logger.connector.config


def exportToCSV(dataSet, fileName):
    dataSet.to_csv(fileName, sep=',', index=False)


def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile

### New
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

    createSeg = ags.createSegment(jsonFile)
    
    return createSeg

# 리스트 형식으로 return
def getJsonList(path):
    file_lst = os.listdir(path)

    jsonList = []
    for file in file_lst:
        filepath = path + '/' + file
        jsonList.append(readJson(filepath))
        
    return jsonList

### New
def getJsonListCsv(path, fileLists):

    jsonList = []
    for file in fileLists:
        filepath = path + '/' + file + '.json'
        jsonList.append(readJson(filepath))
        
    return jsonList


# 220227
def getjsonDict(component, jsonList):
    jsonDict = {}
    for i in range(len(jsonList)):
        jsonDict[component[i]] = str(jsonList[i]['definition']['container'])

    return jsonDict

# 220227
def getSegmentId(component, jsonList):
    jsonDict = {}
    for i in range(len(jsonList)):
        jsonDict[component[i]] = str(jsonList[i]['id'])

    return jsonDict


# input : list
# pull all possible options
def getAllCases_original(dataset):
    
    dataset_list = []
    for i in range(1, len(dataset)):
        #permutations
        printList = list(combinations(dataset, i+1))
        dataset_list.append(printList)

    # 중첩 리스트 제거
    dataset_list_raw = []
    for i in range(len(dataset_list)):
        for j in range(len(dataset_list[i])):
            dataset_list_raw.append(dataset_list[i][j])

    return dataset_list_raw


# List로 out
def setSegment_old(dataset, ifKey, head):
    segmentList = []
    for i in range(len(dataset)):
        if ifKey == True:
            name = head + " " + ' > '.join(dataset[i])
            segmentList.append(name)
        else:
            value = ','.join(dataset[i])
            segmentList.append(value)

    return segmentList

def setSegment(dataset, ifKey, head, prop_what):
    segmentList = []
    for i in range(len(dataset)):
        if ifKey == True:
            name = head + " " + ' > '.join(dataset[i])
            segmentList.append(name)
        else:
            if prop_what == "none":
                value = ','.join(dataset[i])
                segmentList.append(value)
            elif prop_what == "prop_thenhit":
                value = ',{"count": 1, "limit": "within", "container": "hits", "func": "container-restriction"},'.join(dataset[i])
                segmentList.append(value)
            else:
                value = ',{"count": 1, "limit": "within", "attribute": {"func": "attr", "name": "variables/page"}, "func": "dimension-restriction"},'.join(dataset[i])
                segmentList.append(value)                

    return segmentList

# input대로 중첩 리스트 만들기
def createIndex(seg_index):
    index = readCSV(seg_index)

    lst = []
    for i in range(len(index)):
        temp = list(index[i])
        lst.append(temp)

    # 리스트 내 중복 값 제거
    for i in range(len(lst)):
        while ',' in lst[i]:
            lst[i].remove(',')
    
    for i in range(len(lst)):
        while '"' in lst[i]:
            lst[i].remove('"')
        
    return lst


def getAllCases(base_seg, input_index):
    index = createIndex(input_index)
    index_temp = deepcopy(index)
    
    for i in range(len(index)):
        for j in range(len(index[i])):
            index_temp[i][j] = base_seg[int(index[i][j])-1]

    return index_temp


### NEW
def getSegment(seg_component, seg_id, property, segment_archive, current_segment, input_index, head, ownerId):

    seg_def_json = getJsonListCsv(current_segment, seg_id)
    
    # getFileName
    jsonDict = getjsonDict(seg_component, seg_def_json)
    jsonSeg = getSegmentId(seg_component, seg_def_json)

    # Description : 딕셔너리를 key, value로 분리
    jsonKey = []
    jsonValue = []
    for key, value in jsonDict.items():
        jsonKey.append(key)
        jsonValue.append(value)

    # Segment ID : 딕셔너리를 key, value로 분리
    jsonSegKey = []
    jsonSegValue = []
    for key, value in jsonSeg.items():
        jsonSegKey.append(key)
        jsonSegValue.append(value)

    # 경우의 수로 만들기
    segmentName = setSegment(getAllCases(jsonKey, input_index), True, head, "none")
    if property == "prop_thenhit" or property == "prop_thenpv" :
        segmentValue = setSegment(getAllCases(jsonValue, input_index), False, head, property)
    else:
        segmentValue = setSegment(getAllCases(jsonValue, input_index), False, head, "none")

    # Segment
    segmentIdList = { 'segment_name': setSegment(getAllCases(jsonSegKey, input_index), True, head, "none"),
                    'segment_contains' : setSegment(getAllCases(jsonSegValue, input_index), False, head, "none")}
    
    seg_source = pd.DataFrame(segmentIdList)
    seg_source.to_csv(segment_archive + '\seg_contains-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.csv', index=False)

    # template
    
    if property == "prop_or":
        targetFile = ownerIdChange_orand(ownerId, prop_what="or")
        target = deepcopy(targetFile)

    elif property == "prop_and":
        targetFile = ownerIdChange_orand(ownerId, prop_what="and")
        target = deepcopy(targetFile)

    elif property == "prop_then" or property == "prop_thenpv" or property == "prop_thenhit":
        targetFile = ownerIdChange_then(ownerId)
        target = deepcopy(targetFile)
    
    # 변경 후 호출
    segmentInfo = []
    for i in range(len(segmentName)):
        target['name'] = segmentName[i]
        if property == "prop_or" or property == "prop_and":
            target['definition']['container']['pred']['preds'] = list(literal_eval(segmentValue[i]))
        else:
            target['definition']['container']['pred']['stream'] = list(literal_eval(segmentValue[i]))

        callSegment = createSegment(target)
        print(callSegment)
        
        current_seg_def = current_segment + '\\' + str(callSegment["id"]) + '.json'
        seg_arc_def = segment_archive + '\\' + str(callSegment["id"]) + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.json'
        jsonMaker(current_seg_def, target)
        jsonMaker(seg_arc_def, target)

        segmentInfo.append(callSegment)

    segmentList = pd.DataFrame(segmentInfo).drop(["description", "owner", "isPostShardId", "rsid"], axis=1)
    segmentList.to_csv(segment_archive + '\seg_creator-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.csv', index=False)


def jsonMaker(seg_def, target):
    with open(str(seg_def), 'w', encoding='utf-8') as fileName:
        json.dump(target, fileName, indent="\t")


def createSegList(segListCsv):
    seg_list = readCSV(segListCsv)
    
    doubleSegList = []
    for i in range(len(seg_list)):
        doubleSegList.append(seg_list[i].split(','))
    
    return doubleSegList


def listToStr(segList):
    return '", "'.join(segList)

def splitSegList(seg_list_csv):
    segmentList_double = createSegList(seg_list_csv)
    component = []
    segName = []
    for i in range(len(segmentList_double)):
        component.append(segmentList_double[i][0])
        segName.append(segmentList_double[i][1])

    return component, segName

def ownerIdChange_then(ownerId):
    template = """
    {
    "name": "[Test] Home > PFS",
    "description": "",
    "rsid": "sssamsung4mstglobal",
    "reportSuiteName": "P6 WEB - MST Global",
    "owner": {
      "id": 200150002,
      "name": "string",
      "login": "string"
    },
    "definition": {
        "func":"segment",
        "version":[ 1, 0, 0 ],
        "container": {
            "func": "container",
            "context": "visits",
            "pred": {
                "func": "sequence",
                "stream": [
                    {
                        "func":"container",
                        "context":"hits",
                        "pred": {
                            "func": "streq",
                            "str": "home",
                            "val": {
                                "func":"attr", "name":"variables/prop6"
                            }
                        }
                    },
                    {
                        "func":"container",
                        "context":"hits",
                        "pred": {
                            "func": "streq",
                            "str": "product family showcase",
                            "val": {
                                "func":"attr", "name":"variables/prop6"
                            }
                        }
                    }
                ]
            }
        }
    },
    "compatibility": {
      "valid": true,
      "message": "string",
      "validator_version": "string",
      "supported_products": [
        "string"
      ],
      "supported_schema": [
        "string"
      ],
      "supported_features": [
        "string"
      ]
    },
    "definitionLastModified": "2021-08-22T06:19:00.458Z",
    "categories": [
      "string"
    ],
    "siteTitle": "string",
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": "string",
        "components": [
          {
            "componentType": "string",
            "componentId": "string",
            "tags": [
              "Unknown Type: Tag"
            ]
          }
        ]
      }
    ],
    "modified": "2021-08-22T06:19:00.458Z",
    "created": "2021-08-22T06:19:00.458Z"
  }"""
    targetFile = json.loads(template)
    targetFile["owner"]["id"] = ownerId

    return targetFile 


def ownerIdChange_orand(ownerId, prop_what):
    template = """
    {
    "name": "[Test] Home > PFS",
    "description": "",
    "rsid": "sssamsung4mstglobal",
    "reportSuiteName": "P6 WEB - MST Global",
    "owner": {
      "id": 200150002,
      "name": "string",
      "login": "string"
    },
    "definition": {
        "func":"segment",
        "version":[ 1, 0, 0 ],
        "container": {
            "func": "container",
            "context": "hits",
            "pred": {
                "func": "or",
                "preds": [
                    {
                        "func":"container",
                        "context":"hits",
                        "pred": {
                            "func": "streq",
                            "str": "home",
                            "val": {
                                "func":"attr", "name":"variables/prop6"
                            }
                        }
                    },
                    {
                        "func":"container",
                        "context":"hits",
                        "pred": {
                            "func": "streq",
                            "str": "product family showcase",
                            "val": {
                                "func":"attr", "name":"variables/prop6"
                            }
                        }
                    }
                ]
            }
        }
    },
    "compatibility": {
      "valid": true,
      "message": "string",
      "validator_version": "string",
      "supported_products": [
        "string"
      ],
      "supported_schema": [
        "string"
      ],
      "supported_features": [
        "string"
      ]
    },
    "definitionLastModified": "2021-08-22T06:19:00.458Z",
    "categories": [
      "string"
    ],
    "siteTitle": "string",
    "tags": [
      {
        "id": 0,
        "name": "string",
        "description": "string",
        "components": [
          {
            "componentType": "string",
            "componentId": "string",
            "tags": [
              "Unknown Type: Tag"
            ]
          }
        ]
      }
    ],
    "modified": "2021-08-22T06:19:00.458Z",
    "created": "2021-08-22T06:19:00.458Z"
  }"""
    targetFile = json.loads(template)
    targetFile["owner"]["id"] = ownerId
    targetFile["definition"]["container"]["pred"]["func"] = prop_what

    return targetFile 
