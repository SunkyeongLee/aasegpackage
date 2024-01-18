# Created by Sunkyeong Lee
# Inquiry : sunkyeong.lee@concentrix.com / sunkyong9768@gmail.com

from copy import deepcopy
import sys
import aanalytics2 as api2
import json
from itertools import *
import time
import os
from ast import literal_eval


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

def updateSegment(segmentID, jsonFile):
    dataInitiator()
    cid = "samsun0"
    ags = api2.Analytics(cid)
    ags.header

    return ags.updateSegment(segmentID, jsonFile)

def readJson(jsonFile):
    with open(jsonFile, 'r', encoding='UTF8') as bla:
        jsonFile = json.loads(bla.read())

    return jsonFile

def readCSV(csvFile):
    lines = open(csvFile).readlines()
    listCsv = []
    for line in lines[1:]:
        listCsv.append(line.split('\n')[0])

    return listCsv

def dumpJson(seg_location, seg_id, target):
    string = seg_location + '\\' + str(seg_id) + '-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.json'
    with open(str(string), 'w', encoding='UTF8') as fileName:
        json.dump(target, fileName, indent="\t")


def replace_segment(old_seg, new_seg, base_seg):
    if old_seg in base_seg:
        return base_seg.replace(old_seg, new_seg), True
    return base_seg, False


# return 변경한 세그먼트 id 리스트로 반환
def segmentUpdate(before, after, seg_contains, current_segment, segment_archive):
    checkerList = []

    for i in range(len(seg_contains)):
        # 변경할 세그먼트의 old 버전 archive에 현재 날짜 붙여서 저장
    
        # 1. 파일 읽기
        seg_loc = current_segment + "\\" + seg_contains[i] + '.json'
        base_segment = readJson(seg_loc)
        segment_copy = deepcopy(base_segment)

        # 세그먼트 긁어 모으기
        if 'stream' in str(base_segment):
            base_seg = str(base_segment['definition']['container']['pred']['stream'])
            old_seg_json = str(readJson(before)['definition']['container']['pred'])
            new_seg_json = str(readJson(after)['definition']['container']['pred'])

            # 변환 필요한 세그먼트가 base 세그먼트에 있는지 확인
            if old_seg_json in base_seg:
                checkerList.append(True)
            else:
                checkerList.append(False)

            base_seg_replaced = base_seg.replace(old_seg_json, new_seg_json)
            segment_copy['definition']['container']['pred']['stream'] = list(literal_eval(base_seg_replaced))
        
        else :
            base_seg = str(base_segment['definition']['container']['pred'])
            old_seg_json = str(readJson(before)['definition']['container']['pred'])
            new_seg_json = str(readJson(after)['definition']['container']['pred'])

            if old_seg_json in base_seg:
                checkerList.append(True)
            else:
                checkerList.append(False)

        # 저장된 세그먼트에 옛날 세그먼트를 새로운 세그먼트로 변경 후
            base_seg_replaced = base_seg.replace(old_seg_json, new_seg_json)
            # json 형식에 변경한 부분 엎어치기
            segment_copy['definition']['container']['pred'] = literal_eval(base_seg_replaced)

        # 원 파일에 저장
        with open(str(seg_loc), 'w', encoding='utf-8') as fileName:
            json.dump(segment_copy, fileName, indent="\t")

        # archive old seg
        dumpJson(segment_archive, seg_contains[i], segment_copy)

    return seg_contains, checkerList