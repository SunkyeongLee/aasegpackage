# Created by Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com / sunkyong9768@gmail.com

import aanalytics2 as api2
import json
from copy import deepcopy
from itertools import *
import csv
import os
from ast import literal_eval
from sqlalchemy import create_engine
import pandas as pd
import time


def dataInitiator():
    api2.configure()
    logger = api2.Login() 
    logger.connector.config

def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile

def createSegment(jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header
    return ags.createSegment(jsonFile)

def convert_list_description(item):
    # 1. prop > evar
    if item == "prop_evar":
        return {"'description': 'Page'" : "'description': 'PageName (v40)'", "'description': 'All Page Track (p6)'" : "'description': 'All Page Track (v6)'", "'description': 'URL (p39)'" : "'description': 'URL (v39)'", "'description': 'Site Section'" : "'description': 'Site Section (v18)'", "'description': 'Third Level Site Section (p3)'" : "'description': 'Third Level Site Section (v3)'", "'description': 'Fourth Level Site Section (p4)'" : "'description': 'Fourth Level Site Section (v4)'", "'description': 'Fifth Level Site Section (p5)'" : "'description': 'Fifth Level Site Section (v5)'", "'description': 'Site Code (p1)'" : "'description': 'Site Code (v1)'"}
    
    # 2. prop > entry    
    elif item == "prop_entry":    
        return {"'description': 'Page'" : "'description': 'Entry Pages'", "'description': 'All Page Track (p6)'" : "'description': 'Entry All Page Track (p6)'", "'description': 'URL (p39)'" : "'description': 'Entry URL (p39)'", "'description': 'Site Section'" : "'description': 'Entry Site Section'", "'description': 'Third Level Site Section (p3)'" : "'description': 'Entry Third Level Site Section (p3)'", "'description': 'Fourth Level Site Section (p4)'" : "'description': 'Entry Fourth Level Site Section (p4)'", "'description': 'Fifth Level Site Section (p5)'" : "'description': 'Entry Fifth Level Site Section (p5)'", "'description': 'Site Code (p1)'" : "'description': 'Entry Site Code (p1)'"}

    # 3. evar > prop  
    elif item == "evar_prop":  
        return {"'description': 'PageName (v40)'" : "'description': 'Page'", "'description': 'All Page Track (v6)'" : "'description': 'All Page Track (p6)'", "'description': 'URL (v39)'" : "'description': 'URL (p39)'", "'description': 'Site Section (v18)'" : "'description': 'Site Section'", "'description': 'Third Level Site Section (v3)'" : "'description': 'Third Level Site Section (p3)'", "'description': 'Fourth Level Site Section (v4)'" : "'description': 'Fourth Level Site Section (p4)'", "'description': 'Fifth Level Site Section (v5)'" : "'description': 'Fifth Level Site Section (p5)'", "'description': 'Site Code (v1)'" : "'description': 'Site Code (p1)'"}

    # 4. evar > entry
    elif item == "evar_entry": 
        return {"'description': 'PageName (v40)'" : "'description': 'Entry Pages'", "'description': 'All Page Track (v6)'" : "'description': 'Entry All Page Track (p6)'", "'description': 'URL (v39)'" : "'description': 'Entry URL (p39)'", "'description': 'Site Section (v18)'" : "'description': 'Entry Site Section'", "'description': 'Third Level Site Section (v3)'" : "'description': 'Entry Third Level Site Section (p3)'", "'description': 'Fourth Level Site Section (v4)'" : "'description': 'Entry Fourth Level Site Section (p4)'", "'description': 'Fifth Level Site Section (v5)'" : "'description': 'Entry Fifth Level Site Section (p5)'", "'description': 'Site Code (v1)'" : "'description': 'Entry Site Code (p1)'"}
    
    # 5. entry > prop
    elif item == "entry_prop":     
        return {"'description': 'Entry Pages'" : "'description': 'Page'", "'description': 'Entry All Page Track (p6)'" : "'description': 'All Page Track (p6)'", "'description': 'Entry URL (p39)'" : "'description': 'URL (p39)'", "'description': 'Entry Site Section'" : "'description': 'Site Section'", "'description': 'Entry Third Level Site Section (p3)'" : "'description': 'Third Level Site Section (p3)'", "'description': 'Entry Fourth Level Site Section (p4)'" : "'description': 'Fourth Level Site Section (p4)'", "'description': 'Entry Fifth Level Site Section (p5)'" : "'description': 'Fifth Level Site Section (p5)'", "'description': 'Entry Site Code (p1)'" : "'description': 'Site Code (p1)'"}
    
    # 6. entry > evar
    elif item == "entry_evar":    
        return {"'description': 'Entry Pages'" : "'description': 'PageName (v40)'", "'description': 'Entry All Page Track (p6)'" : "'description': 'All Page Track (v6)'", "'description': 'Entry URL (p39)'" : "'description': 'URL (v39)'", "'description': 'Entry Site Section'" : "'description': 'Site Section (v18)'", "'description': 'Entry Third Level Site Section (p3)'" : "'description': 'Third Level Site Section (v3)'", "'description': 'Entry Fourth Level Site Section (p4)'" : "'description': 'Fourth Level Site Section (v4)'", "'description': 'Entry Fifth Level Site Section (p5)'" : "'description': 'Fifth Level Site Section (v5)'", "'description': 'Entry Site Code (p1)'" : "'description': 'Site Code (v1)'"}

def convert_list_name(item):
    # 1. prop > evar
    if item == "prop_evar":
        return {"'name': 'variables/page'" : "'name': 'variables/evar40'", "'name': 'variables/prop6'" : "'name': 'variables/evar6'", "'name': 'variables/prop39'" : "'name': 'variables/evar39'", "'name': 'variables/sitesections'" : "'name': 'variables/evar18'", "'name': 'variables/prop3'" : "'name': 'variables/evar3'", "'name': 'variables/prop4'" : "'name': 'variables/evar4'", "'name': 'variables/prop5'" : "'name': 'variables/evar5'", "'name': 'variables/prop1'" : "'name': 'variables/evar1'"}
    
    # 2. prop > entry    
    elif item == "prop_entry":    
        return {"'name': 'variables/page'" : "'name': 'variables/entrypage'", "'name': 'variables/prop6'" : "'name': 'variables/entryprop6'", "'name': 'variables/prop39'" : "'name': 'variables/entryprop39'", "'name': 'variables/sitesections'" : "'name': 'variables/entrysitesections'", "'name': 'variables/prop3'" : "'name': 'variables/entryprop3'", "'name': 'variables/prop4'" : "'name': 'variables/entryprop4'", "'name': 'variables/prop5'" : "'name': 'variables/entryprop5'", "'name': 'variables/prop1'" : "'name': 'variables/entryprop1'"}

    # 3. evar > prop  
    elif item == "evar_prop":  
        return {"'name': 'variables/evar40'" : "'name': 'variables/page'", "'name': 'variables/evar6'" : "'name': 'variables/prop6'", "'name': 'variables/evar39'" : "'name': 'variables/prop39'", "'name': 'variables/evar18'" : "'name': 'variables/sitesections'", "'name': 'variables/evar3'" : "'name': 'variables/prop3'", "'name': 'variables/evar4'" : "'name': 'variables/prop4'", "'name': 'variables/evar5'" : "'name': 'variables/prop5'", "'name': 'variables/evar1'" : "'name': 'variables/prop1'"}

    # 4. evar > entry
    elif item == "evar_entry": 
        return {"'name': 'variables/evar40'" : "'name': 'variables/entrypage'", "'name': 'variables/evar6'" : "'name': 'variables/entryprop6'", "'name': 'variables/evar39'" : "'name': 'variables/entryprop39'", "'name': 'variables/evar18'" : "'name': 'variables/entrysitesections'", "'name': 'variables/evar3'" : "'name': 'variables/entryprop3'", "'name': 'variables/evar4'" : "'name': 'variables/entryprop4'", "'name': 'variables/evar5'" : "'name': 'variables/entryprop5'", "'name': 'variables/evar1'" : "'name': 'variables/entryprop1'"}
    
    # 5. entry > prop
    elif item == "entry_prop":     
        return {"'name': 'variables/entrypage'" : "'name': 'variables/page'", "'name': 'variables/entryprop6'" : "'name': 'variables/prop6'", "'name': 'variables/entryprop39'" : "'name': 'variables/prop39'", "'name': 'variables/entrysitesections'" : "'name': 'variables/sitesections'", "'name': 'variables/entryprop3'" : "'name': 'variables/prop3'", "'name': 'variables/entryprop4'" : "'name': 'variables/prop4'", "'name': 'variables/entryprop5'" : "'name': 'variables/prop5'", "'name': 'variables/entryprop1'" : "'name': 'variables/prop1'"}
    
    # 6. entry > evar
    elif item == "entry_evar":    
        return {"'name': 'variables/entrypage'" : "'name': 'variables/evar40'", "'name': 'variables/entryprop6'" : "'name': 'variables/evar6'", "'name': 'variables/entryprop39'" : "'name': 'variables/evar39'", "'name': 'variables/entrysitesections'" : "'name': 'variables/evar18'", "'name': 'variables/entryprop3'" : "'name': 'variables/evar3'", "'name': 'variables/entryprop4'" : "'name': 'variables/evar4'", "'name': 'variables/entryprop5'" : "'name': 'variables/evar5'", "'name': 'variables/entryprop1'" : "'name': 'variables/evar1'"}


def convertValue(as_is, to_be, json):
    for i in range(len(as_is)):
        if as_is[i] in json:
            json = json.replace(as_is[i], to_be[i])
        else:
            continue

    return json

def convertSeg(item, json):
    prop = readJson(json)
    prop_temp = str(deepcopy(prop['definition']))
    
    seg_description = convertValue(list(convert_list_description(item).keys()), list(convert_list_description(item).values()), prop_temp)
    seg_name = convertValue(list(convert_list_name(item).keys()), list(convert_list_name(item).values()), seg_description)

    prop['definition'] = literal_eval(seg_name)
    
    return prop    

def item_maker(as_is, to_be):
    return as_is + "_" + to_be

def idToList(segmentId):
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    conn = db_connection.connect()

    query = """
    SELECT id FROM segment.tb_segment_list
    where name = "{0}"
    """.format(segmentId)

    result = pd.read_sql_query(query, conn)
    result_to_list = ''.join(result['id'].values.tolist())

    conn.close()
    
    return result_to_list

def jsonMaker(seg_def, target):
    with open(str(seg_def), 'w', encoding='utf-8') as fileName:
        json.dump(target, fileName, indent="\t")

def csvSaver(current_segment, segment_archive, callSegment, target):
    current_seg_def = current_segment + '\\' + str(callSegment["id"]) + '.json'
    seg_arc_def = segment_archive + '\\' + str(callSegment["id"]) + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.json'
    jsonMaker(current_seg_def, target)
    jsonMaker(seg_arc_def, target)
    
    segmentInfo = []
    segmentInfo.append(callSegment)

    segmentList = pd.DataFrame(segmentInfo).drop(["description", "owner", "isPostShardId", "rsid"], axis=1)

    stackTodb(segmentList, 'tb_segment_list')

def updateNameId(as_is, to_be, owner_id, file):
    seg = convertSeg(item_maker(as_is, to_be), file)
    seg['name'] = deepcopy(seg['name']) + ' (' + as_is + ' > ' + to_be + ')'
    seg["owner"]["id"] = owner_id
    
    return seg

def stackTodb(dataFrame, dbTableName):
    print(dataFrame)
    db_connection_str = 'mysql+pymysql://root:12345@127.0.0.1:3307/segment'
    db_connection = create_engine(db_connection_str, encoding='utf-8')
    db_connection.connect()

    dataFrame.to_sql(name=dbTableName, con=db_connection, if_exists='append', index=False)
    print("finished")

def segmentLocation(current_segment, segment_name):
    return  current_segment + '\\' + idToList(segment_name) + '.json'

def segmentConverter(current_segment, segment_archive, as_is, to_be, owner_id, segment_name):
    segment = updateNameId(as_is, to_be, owner_id, segmentLocation(current_segment, segment_name))
    output = createSegment(segment)
    print(output)

    csvSaver(current_segment, segment_archive, output, segment)


if __name__ == "__main__":
    current_segment = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/current_segment"
    segment_archive = "C://Users/sunky/OneDrive - Concentrix Corporation/Desktop/업무/Save/02-2022/세그먼트 업데이트 자동화/segment List/segment_archive"
    
    segment_name = "Group : HHP - test"
    as_is = "prop"
    to_be = "entry"
    owner_id = "200121276"

    segmentConverter(current_segment, segment_archive, as_is, to_be, owner_id, segment_name)
