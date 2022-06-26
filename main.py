# Imports
from tokenize import Triple
import math
import PyQt5
import sys
import random
import threading
from concurrent.futures import ThreadPoolExecutor
import time

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
        
        # Rounds dictionary (each round will have own, pairing being (image / desc., why trash / recycle)) (44 chars / line)
        self.round_1 = [["Welcome. This is an introduction.\nEasy points, right? Click Trash!", "trash", "It said to click trash..."],
                        ["Now click Recycle!", "recycle", "It said to click recycle..."],
                        ["Click Trash once more!", "recycle", "Just got siked! This popup will explain why you got something wrong.\nDon't worry; this will be the only \"jk\" in the game!"],
                        ["Congratulations. You made it!\nClick Recycle to finish off.\nIf you do not, you will not pass.\nYou need at least a 60%.", "recycle", "It said to click recycle...please read..."],
                        ]
        
        self.round_2 = [["Your backpack from kindergarden.", "recycle", "Backpacks are recyclable!\nNote that only specific centers accept them."],
                        ["The leftover burrito on your floor.", "trash", "Food is not recyclable. It is compostable, though!\nTry that instead."],
                        ["The zipper of your sister's hoodie.", "recycle", ""],
                        ["A drawing on paper you tore\nto minuscule pieces.", "trash", "Shredded paper can sometimes be recyclable; however, the smaller it is, the less it can be.\nThis is because paper fibers get shortened every time they are recycled, until they are downcycled.\nTorn paper has very short fibers."],
                        ["Holiday card your aunt gifted you on\nCinco De Mayo.", "recycle", "Holiday cards are made of paper, and are not contaminated, so recycle them!\nAny electronic part inside may also be recyclable."],
                        ["Aerosol can containing hair spray inside.", "trash", "The can is recyclable, but if ANYTHING is inside, even whipped cream,\nthen recycling programs won't accept it. Use the produce inside completely."]]
        
        self.round_3 = [["Your mint-flavored\nColgate toothpaste tube.", "recycle", "Terracycle accepts Colgate toothbrushes and recycles them.\nWhat a great partnership!"],
                        ["The bubble wrap around\nyour Amazon package.", "trash", "Bubble wrap is made of Type #4 plastic.\nType #2 and #4 plastics can tangle with other recyclables and damage equipment.\n So do not recycle them!"],
                        ["Sheet of multicolored glass.", "recycle", "Glass is a recyclable object. The type and color does not cause an issue."],
                        ["A new type of bioplastic - PEF.", "recycle", "Bioplastics, in general, are not recyclable.\nHowever, a new type has been created - PEF - which is recyclable."],
                        ["The broken glass of your window.", "trash", "Although glass is recyclable, broken shards can harm handlers, so keep them out!"],
                        ["The oil of your car engine.", "recycle", "Oil is recyclable!\nThis is the best option, for dumping it can contaminate the water supply.\nOnly specific centers accept it, so check."]]
        
        self.round_4 = [["Paper that you used to wax.", "trash", "Due to the wax on the paper, it is considered mixed paper, and is not recyclable."],
                        ["Pizza box,\nwith the remains scraped away.", "recycle", "Although the box is contaminated, we can easily remove the food and recycle.\nGrease is not a major problem."],
                        ["Robot battery containing 12 volts.", "recycle", "All batteries are recyclable!\nRemember to tape their ends when the volt is greater than 9, however..."],
                        ["Paper you accidently spilled water on.", "trash", "Water can cause the paper fibers to shorten and degrade,\nand wet paper may cause clogs to form."],
                        ["Aluminum foil with no food residue.", "recycle", "As long as the alumininum is not contaminiated, this foil is recyclable."],
                        ["Those receipts from your\nmall shopping spree.", "trash", "Receipts are printed on thermal paper, which contains BPA,\nmaking them not recyclable nor compostable."]]
        
        self.round_5 = [["Paper plates from your birthday party,\nstained with food and grease.", "trash", "Although paper plates are recyclable, this is only when they are not contaminated."],
                        ["The license plate of your\ngrandfather's car.", "recycle", "You surrender your old license plate when recieveing a new one.\nIf not, the scrap metal can go to good use."],
                        ["The stickers on your laptop.", "trash", "The adhesive side of the sticker can harm recycling machines, so don't do it!"],
                        ["Hard drive of your old Toshiba laptop.", "recycle", "Although difficult, these drives are recyclable.\nAfter years of use and new technology, you won't need them!\nFind a center near you."],
                        ["A blunt knife that you have now replaced.", "recycle", "Knives are made of scrap metal that have numerous uses, making them recyclable."],
                        ["Your strawberry yogurt cup from Publix.", "recycle", "Although they are made of Plastic #5, these cups are recyclable.\nThe process is costly, so some centers do not.\nBe sure to check!"]]

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
        sys.exit()  # TODO Cleaner way to end program? CANT END MIDGAME BECAUSE NOT DAEMON (ALSO DONT EVEN TRY TOUCHING THE THREADS THEY MAGICALLY WORK APPRECIATE IT OK)

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
                num_items = len(self.round_2)
                for questions in self.round_2:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
                
            case 3:
                num_items = len(self.round_3)
                for questions in self.round_3:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
                
            case 4:
                num_items = len(self.round_4)
                for questions in self.round_4:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
                
            case 5:
                num_items = len(self.round_5)
                for questions in self.round_5:
                    items.append(questions[0])
                    answers.append(questions[1])
                    explanations.append(questions[2])
            
        # Play The Game
        
        # Question By Question
        for question in range(0, num_items):
            
            self.ui.stats.setText(f"Round: {self.round}\nCorrect: {right_answers}\nWrong: {wrong_answers}\nScore: {self.round_points}")
            
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
                self.ui.text_1337.setText(explanations[question])
                self.ui.popup_2.show()
            else:
                self.round_points += 4
                right_answers += 1    
            
            # Display User Statistics
            self.ui.stats.setText(f"Round: {self.round}\nCorrect: {right_answers}\nWrong: {wrong_answers}\nScore: {self.round_points}")
        
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
            
            self.total_points += round(self.round_points * accuracy)
            self.ui.stats.setText(f"🎉🎉🎉\nTotal Points: {self.total_points}\n🎉🎉🎉")
            
        # Failed Round
        else:
            self.ui.text_1337.setText(f"Your accuracy was less than 60%, the minimum.\nThe round will be restarted. Good luck.")
        
        self.round_points = 0
        
        # Show Popup for Information 
        self.ui.item_display.setText(f"Round {self.round}")
        self.ui.popup_2.show()
        
        # Reset Variables
        right_answers = 0
        wrong_answers = 0
        accuracy = 0
        
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
