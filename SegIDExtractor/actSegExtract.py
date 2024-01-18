from fileinput import filename
import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets, uic
import segExtract as se
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# form_class = uic.loadUiType("SegmentLibrary\segment_library.ui")[0]
form = resource_path("segment_id_extractor.ui")
form_class = uic.loadUiType(form)[0]

class MyWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Segment ID Extractor")

        self.csvimport.clicked.connect(self.keyword_list_open)
        self.folderselect.clicked.connect(self.where_to_save_open)
        self.complete.clicked.connect(self.function_execute)

    def keyword_list_open(self):
        global keyword_list
        keyword_list = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        self.csvimport_text.setText(keyword_list[0])

    def where_to_save_open(self):
        global where_to_save
        where_to_save = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory')
        self.folderselect_text.setText(where_to_save)

    def function_execute(self):
        keyword = [item.split(',')[0] for item in se.readCSV(keyword_list[0])]

        print(se.segIdExtractor(keyword, where_to_save))
        print('***Segment ID List created successfully***')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    app.exec_()