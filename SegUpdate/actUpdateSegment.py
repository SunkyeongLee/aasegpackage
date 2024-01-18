from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import actUpdateSeg as au
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path("segment_update_main.ui")
form_class = uic.loadUiType(form)[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Segment Update")
        self.pushButton_before.clicked.connect(self.before_segment_upload)
        self.pushButton_after.clicked.connect(self.after_segment_upload)
        self.pushButton_csv.clicked.connect(self.csv_list_upload)
        
        self.pushButton_current.clicked.connect(self.current_segment_open)
        self.pushButton_archive.clicked.connect(self.segment_archive_open)
        self.pushButton_complete.clicked.connect(self.function_execute)

    def before_segment_upload(self):
        global before_segment
        before_segment = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Json')
        self.textEdit_before.setText(before_segment[0])

    def after_segment_upload(self):
        global after_segment
        after_segment = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Json')
        self.textEdit_after.setText(after_segment[0])

    def csv_list_upload(self):
        global csv_list
        csv_list = QtWidgets.QFileDialog.getOpenFileName(self, 'Open CSV')
        self.textEdit_csv.setText(csv_list[0])

    def current_segment_open(self):
        global current_segment
        current_segment = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textEdit_current.setText(current_segment)

    def segment_archive_open(self):
        global segment_archive
        segment_archive = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.textEdit_archive.setText(segment_archive)
        
    def function_execute(self):
        segment_id = [item.split(',')[1] for item in au.readCSV(csv_list[0])]

        result = au.segmentUpdate(before_segment[0], after_segment[0], segment_id, current_segment, segment_archive)
        seg_list = result[0]
        checker_list = result[1]
        
        for i in range(len(seg_list)):
            seg_loc = current_segment + "\\" + seg_list[i] + '.json'
            if checker_list[i] == True:
                update_log = au.updateSegment(seg_list[i], au.readJson(seg_loc))
                print(update_log)
            else:
                print('Nothing to change')
        
        print('**All segment definitions saved***')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()