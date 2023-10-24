from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import actConvertSeg as ac
import sys
import os
import pymysql


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("segment_converter.ui")
form_class = uic.loadUiType(form)[0]
# form_class = uic.loadUiType("..\SegmentCreate\segment_create_main.ui")[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Segment Converter")
        self.textLine_owner_enter.clicked.connect(self.getOwnerId)
        self.segment_name_enter.clicked.connect(self.getSegmentName)
        self.pushButton_currentSeg.clicked.connect(self.current_segment_open)
        self.pushButton_segArc.clicked.connect(self.segment_archive_open)
        self.complete.clicked.connect(self.function_execute)

        self.as_is_prop.clicked.connect(self.asIsRadChecked)
        self.as_is_evar.clicked.connect(self.asIsRadChecked)
        self.as_is_entry.clicked.connect(self.asIsRadChecked)

        self.to_be_prop.clicked.connect(self.tobeRadChecked)
        self.to_be_evar.clicked.connect(self.tobeRadChecked)
        self.to_be_entry.clicked.connect(self.tobeRadChecked)

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

    def getOwnerId(self):
        global owner_id
        owner_id = self.textLine_owner.text()
        self.textLine_owner_out.setText(owner_id)

    def getSegmentName(self):
        global segment_name
        segment_name = self.segment_name.text()
        self.segment_name_out.setText(segment_name)

    def current_segment_open(self):
        global current_segment
        current_segment = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_currentSeg.setText(current_segment)

    def segment_archive_open(self):
        global segment_archive
        segment_archive = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textBrowser_segArc.setText(segment_archive)
        
    def function_execute(self):
        ac.segmentConverter(current_segment, segment_archive, as_is, to_be, owner_id, segment_name)
        print("***" + segment_name + " has been converted***")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()