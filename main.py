# Imports
from tokenize import Triple
import math
import PyQt5
import sys
import random
import threading
from concurrent.futures import ThreadPoolExecutor

# PyQt5 Imports
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QThread, QThreadPool, QRunnable
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
        self.trash = False
        self.recycle = False
        self.continue_on = False
        
        # Game Process
        game_prc = ThreadPoolExecutor(1)
        
        # Rounds dictionary (each round will have own, pairing being (image / desc., why trash / recycle))
        self.round_1 = [["item1", "trash", "reasoning"],
                        ["item2", "recycle", "reasoning_2"],
                        ["item3", "trash", "reasoning"]]

        # Hide Title Bar
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        # ?
        app.setQuitOnLastWindowClosed(False)

        # Button Functions
        self.ui.btn_close.clicked.connect(self.exit_app)
        self.ui.btn_minimize.clicked.connect(self.min_app)
        # self.ui.btn_maximize.clicked.connect(self.max_app)
        self.ui.btn_close_popup.clicked.connect(self.begin_app)
        self.ui.text_104.clicked.connect(self.begin_app)
        self.ui.btn_close_note.clicked.connect(self.hide_notes)
        self.ui.help_but.clicked.connect(self.return_welcome)
        self.ui.timer_btn.clicked.connect(lambda: game_prc.submit(self.start_game,))
        self.ui.trashcan.clicked.connect(self.clicked_waste)
        self.ui.recycle.clicked.connect(self.clicked_green)

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
        self.ui.text_1337.setText(f"Hello there! To begin the game, close this popup (red button) and click begin. The green box will\ncontain a description of an item. Your goal is to decide whether to recycle or trash it! If you get it\nwrong, a popup will appear, showing the correct answer. Wrong answers are -1 points, right\nanswers being 4 points. The final score will be the points you recieved times the accuracy (of the\nround). You will play for five rounds. Have fun, and begin Round {self.round}.")  # Max 100 chars per line.
        self.ui.popup_2.show()
        
    def hide_notes(self):
        self.ui.popup_2.hide()
        self.ui.window.show()
        
    def return_welcome(self):
        self.ui.window.hide()
        self.ui.popup.show()
        self.ui.popup_2.hide()

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
    # and right answers lead to 4 positive points (MAO, let's go!).
    
    def clicked_waste(self):
        self.trash = True
        self.recycle = False
        
    def clicked_green(self):
        self.recycle = True
        self.trash = False
    
    def start_game(self):
        
        self.ui.timer_btn.hide()
            
        # Game Params
        current_round = self.round
        right_answers = 0
        wrong_answers = 0
        self.round_points = 0
        
        # Round Params
        items = []
        answers = []
        explanations = []
            
        # Get Each Round's Information Beforehand
        match current_round:
            
            case 1:
                self.total_points = 0
                num_items = len(self.round_1)
                for questions in self.round_1:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
                    
            case 2:
                num_items = len(self.round_1)
                for questions in self.round_1:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
                
            case 3:
                num_items = len(self.round_1)
                for questions in self.round_1:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
                
            case 4:
                num_items = len(self.round_1)
                for questions in self.round_1:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
                
            case 5:
                num_items = len(self.round_1)
                for questions in self.round_1:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
            
        # Play The Game
        
        # Question By Question
        for question in range(0, num_items):
            
            # Display Question
            self.ui.item_display.setText(items[question])
            
            # Wait for answer to be clicked.
            while self.trash == False and self.recycle == False:
                pass
                
            # Check answer.
            if self.trash == True:
                answer = "trash"
            else:
                answer = "recycle"
                
            # Reset Variables
            self.trash = False
            self.recycle = False
                
            if answer != answers[question]:
                self.round_points -= 1
                wrong_answers += 1
            else:
                self.round_points += 4
                right_answers += 1
            
        # Accuracy
        accuracy = right_answers / (right_answers + wrong_answers)
        
        # Decide Next Round
        if accuracy >= 0.6:
            
            # Proceed
            if current_round != 5:
                self.round += 1
                self.ui.text_1337.setText("Congratulations! You passed. Welcome to the next round.")
            
            # Restart
            else:
                self.round = 1
                self.ui.text_1337.setText("🎉 Congrats! You finished! 🎉\nWith this knowledge, you can help the world. If you wish, you can restart at Round 1.")
            
            self.total_points += round((self.round_points * accuracy))
            self.ui.stats.setText(f"🎉🎉🎉\nTotal Points: {self.total_points}\n🎉🎉🎉")
            
        # Failed Round
        else:
            self.ui.text_1337.setText(f"Your accuracy was {round(accuracy, 2) * 100}%. You need at least 60%.\nThe round will be restarted. Good luck.")
        
        self.round_points = 0
        
        # Show Popup for Information 
        self.ui.item_display.setText(f"Round {self.round}")
        self.ui.popup_2.show()
        
        self.ui.timer_btn.show()
        
        # self.game_prc.join()
                
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
