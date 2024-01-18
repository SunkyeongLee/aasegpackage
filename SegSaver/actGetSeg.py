# Created by  Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com / sunkyong9768@gmail.com

import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import sys
import os
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


def getSegmentInfo(segmentId):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    createSeg = ags.getSegment(segmentId, False, "definition")
    
    return createSeg

def readCSV(csvFile):
    lines = open(csvFile).readlines()
    listCsv = []
    for line in lines[1:]:
        listCsv.append(line.split('\n')[0])

    return listCsv


#231024 DB검색 > csv 인풋으로 seg id 바로 받는 방식으로 변경
#segment 이름이 있는 csv > segment id return
# def idToList(segmentId):
#     db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
#     db_connection = create_engine(db_connection_str, encoding='utf-8')
#     conn = db_connection.connect()

#     query = """
#     SELECT id FROM segment.tb_segment_list
#     where name in ("{0}")
#     """.format(listToStr(segmentId))
    
#     result = pd.read_sql_query(query, conn)
#     result_to_list = result['id'].values.tolist()
#     conn.close()
    
#     return result_to_list

def listToStr(segList):
    return '", "'.join(segList)


def createCSV(fileLoc, seg_id, seg_def):
    string = fileLoc + '\\' + str(seg_id) + '.json'
    with open(str(string), 'w', encoding='utf-8') as fileName:
        json.dump(seg_def, fileName, indent="\t")


def getSegmentDefinition(seg_id, current_seg, segment_archive):
    seg_def = getSegmentInfo(seg_id)
    createCSV(current_seg, seg_id, seg_def)
    createCSV(segment_archive, seg_id + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()), seg_def)
