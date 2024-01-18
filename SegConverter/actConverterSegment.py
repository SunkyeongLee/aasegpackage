from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import actConvertSeg as ac
import sys
import os
import pandas as pd
import time


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("segment_converter.ui")
form_class = uic.loadUiType(form)[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Segment Converter")
        self.textLine_owner_enter.clicked.connect(self.getOwnerId)
        self.pushButton_seglist.clicked.connect(self.getSegmentList)
        self.pushButton_currentSeg.clicked.connect(self.current_segment_open)
        self.pushButton_segArc.clicked.connect(self.segment_archive_open)
        self.complete.clicked.connect(self.function_execute)

        self.as_is_prop.clicked.connect(self.asIsRadChecked)
        self.as_is_evar.clicked.connect(self.asIsRadChecked)
        self.as_is_entry.clicked.connect(self.asIsRadChecked)
        self.as_is_exit.clicked.connect(self.asIsRadChecked)

        self.to_be_prop.clicked.connect(self.tobeRadChecked)
        self.to_be_evar.clicked.connect(self.tobeRadChecked)
        self.to_be_entry.clicked.connect(self.tobeRadChecked)
        self.to_be_exit.clicked.connect(self.tobeRadChecked)

    def asIsRadChecked(self):
        global as_is
        if self.as_is_prop.isChecked():
            as_is = "prop"
            return as_is
        
        elif self.as_is_evar.isChecked():
            as_is = "evar"
            return as_is
        
        elif self.as_is_entry.isChecked():
            as_is = "entry"
            return as_is

        elif self.as_is_exit.isChecked():
            as_is = "exit"
            return as_is

    def tobeRadChecked(self):
        global to_be
        if self.to_be_prop.isChecked():
            to_be = "prop"
            return to_be
        
        elif self.to_be_evar.isChecked():
            to_be = "evar"
            return to_be
        
        elif self.to_be_entry.isChecked():
            to_be = "entry"
            return to_be

        elif self.to_be_exit.isChecked():
            to_be = "exit"
            return to_be

    def getOwnerId(self):
        global owner_id
        owner_id = self.textLine_owner.text()
        self.textLine_owner_out.setText(owner_id)

    def getSegmentList(self):
        global segment_list
        segment_list = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.textBrowser_seglist.setText(segment_list[0])

    def current_segment_open(self):
        global current_segment
        current_segment = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_currentSeg.setText(current_segment)

    def segment_archive_open(self):
        global segment_archive
        segment_archive = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_segArc.setText(segment_archive)
        
    def function_execute(self):
        segment_id = [item.split(',')[1] for item in ac.readCSV(segment_list[0])]

        seglist = []
        for i in range(len(segment_id)):
            seglist.append(ac.segmentConverter(current_segment, segment_archive, as_is, to_be, owner_id, segment_id[i]))

        df1 = pd.DataFrame(seglist).drop(["description", "owner", "isPostShardId", "rsid"], axis=1)
        df1.to_csv(segment_archive + '\seg_converter-' + time.strftime('%Y%m%d-%H%M%S', time.localtime()) + '.csv', index=False)
        print("***Segment Convertion is completed***")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()