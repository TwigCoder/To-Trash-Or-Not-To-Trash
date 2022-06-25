# Imports
import PyQt5
import sys

# PyQt5 Imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from my_ui import Ui_MainWindow


# Runnable Application GUI
class Window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.title_bar.isPressed = False

        # Hide Title Bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Button Functions
        self.ui.btn_close.clicked.connect(self.exit_app)
        self.ui.btn_minimize.clicked.connect(self.min_app)
        # self.ui.btn_maximize.clicked.connect(self.max_app)
        self.ui.btn_close_popup.clicked.connect(self.begin_app)
        self.ui.text_104.clicked.connect(self.begin_app)

        # Show Window
        self.setMouseTracking(True)
        self.show()
        self.ui.popup.show()
        self.ui.popup_2.hide()
        self.ui.window.hide()

    # Title Bar Buttons #

    def exit_app(self):
        sys.exit()

    def min_app(self):
        self.showMinimized()
        print("Passed: App successfully minimized.")
        
    def begin_app(self):
        self.ui.popup.hide()
        self.ui.window.show()

    #def max_app(self):
    #    if not self.isMaximized():
    #        self.geometry = self.saveGeometry()
    #        self.showMaximized()
    #
    #    else:
    #        self.restoreGeometry(self.geometry)

    ##

    # Movable Title Bar #

    def mousePressEvent(self, event):

        self.ui.title_bar.isPressed = True
        self.startPos = event.globalPos()
        return QWidget().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.ui.title_bar.isPressed = False
        return QWidget().mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.ui.title_bar.isPressed:

            if self.isMaximized:
                self.showNormal()

            move_pos = event.globalPos() - self.startPos
            self.startPos = event.globalPos()
            self.move(self.pos() + move_pos)

        return QWidget().mouseMoveEvent(event)

    ##


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    app.exec_()
