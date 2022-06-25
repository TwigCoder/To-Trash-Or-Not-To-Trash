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
        
        # Variable Initialization (Game Framework)
        self.total_points = 0
        self.round_points = 0  # Remember to reinitialize to 0 per round.
        self.round = 1
        
        # Rounds dictionary (each round will have own, pairing being (image / desc., why trash / recycle))
        self.round_1 = {
            "1": None,
            "2": None
        }

        # Hide Title Bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Button Functions
        self.ui.btn_close.clicked.connect(self.exit_app)
        self.ui.btn_minimize.clicked.connect(self.min_app)
        # self.ui.btn_maximize.clicked.connect(self.max_app)
        self.ui.btn_close_popup.clicked.connect(self.begin_app)
        self.ui.text_104.clicked.connect(self.begin_app)
        self.ui.btn_close_note.clicked.connect(self.hide_notes)
        self.ui.help_but.clicked.connect(self.return_welcome)

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
        self.ui.text_1337.setText(f"Welcome to the game. To begin, close this popup (red button) and click begin. The timer will start\nticking away. Either an image or a description will popup in the green box. You are to decide if\nthat item should be trashed or recycled. See the Welcome Page for which button to press (hint:\nbuttons turn darker when you hover over them). Keep going until either you finish early (and\nreceieve bonus points) or the timer stops. All unfinished items will have no impact on your score\nnor accuracy. All wrong items will award 1 negative point, and all correct answers bestow 4 points.\nAccuracy matters: the final score of the round is the total score you recieved times the accuracy\npercentage. When something is wrong, this popup will be back with an explanation of what\nhappened. Have fun, and begin Round {self.round}.")  # Max 100 chars per line.
        self.ui.popup_2.show()
        
    def hide_notes(self):
        self.ui.popup_2.hide()
        self.ui.window.show()
        
    def return_welcome(self):
        self.ui.window.hide()
        self.ui.popup.show()

    #def max_app(self):
    #    if not self.isMaximized():
    #        self.geometry = self.saveGeometry()
    #        self.showMaximized()
    #
    #    else:
    #        self.restoreGeometry(self.geometry)

    ##
    
    
    # Game Functionality #
    
    # An item will be presented to the user, either as an image or a description. From there, they will click on
    # the recycle or trashcan icon. Remeber to bring a popup once they click off the welcome screen to tell them
    # to do this (expect nothing, and you shall not be surprised). Create a point system. There should be the
    # total number of points (of all rounds) and points per round (create a round system as well). Points per round
    # will be the accuracy percentage of the total number of points gained. Wrong answers lead to 1 negative point,
    # and right answers lead to 4 positive points (MAO, let's go!). EXPLAIN THIS TO THE USER!!!
    
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
