import random
from PyQt5.QtWidgets import (QApplication , QWidget , QHBoxLayout , QVBoxLayout ,QPushButton , QLabel, QGridLayout , QMessageBox )
from PyQt5 import ( QtCore , QtGui )
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import sys
from functools import partial
from datetime import datetime

"""
Author : Yahia Mostafa


"""

#TODO bomb icon
#TODO flag icon
#TODO disable clicked buttons 
#TODO 
#TODO 
#TODO 
class MinesGame (QWidget):


    def __init__(self , width , height , mines ,app):

        super().__init__()

        self.width = width
        self.height = height
        self.mines = mines

        self.btns = {}
        self.flags = set()
        self.isStarted = False
        self.scoreLabel = QLabel(f"0/{self.mines}")
        self.grid = [ [0] * width for i in range(height)]
        self.app = app
        self.createTimer()
        self.initTable()
        self.initGUI()

    def initTable(self):
        arr = []
        for i in range (self.height):
            for j in range(self.width):
                arr.append(str(i)+ str('+') + str(j))
        self.distMines(arr)

    def distMines(self , arr):
        for j in range(self.mines):

            index = random.randint( 0 ,  len(arr) - 1)
            randInd = arr[index].split('+')
            arr.pop(index)


            row = int(randInd[0])
            col = int(randInd[1])

            self.grid[row][col] = -1
        self.assignNums()

    def assignNums(self):
        dx = [-1 , 0  , 1  , 1 , 1 , 0 , -1 , -1]
        dy = [-1 , -1 , -1 , 0 , 1 , 1 , 1  , 0]

        for i in range (self.height):
            for j in range(self.width):
                surMines = 0
                if self.grid[i][j] == -1:
                    continue
                for k in range(8):
                    new_row = i + dy[k]
                    new_col = j + dx[k]
                    if (new_col >=0 and new_row >=0 and new_row < self.height and new_col < self.width):
                        surMines = surMines +1 if self.grid[new_row][new_col] == -1 else surMines
                self.grid[i][j] = surMines

    def pickColor(self , pos , numOfBombs):

        if numOfBombs == -1:
            return

        self.btns[pos].setText(str (numOfBombs))
        self.btns[pos].setFont(QtGui.QFont('Times'))



        if numOfBombs == 0 :
            self.btns[pos].setStyleSheet('QPushButton {background-color: #022d36; color: white;}')
            self.addCells(pos)
        elif numOfBombs == 1:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #69be28; color: white;}')   
        elif numOfBombs == 2:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #3db7e4; color: white;}')  
        elif numOfBombs == 3:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #ff3366; color: white;}') 
        elif numOfBombs == 4:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #ff8849; color: white;}') 
        elif numOfBombs == 5:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #1520a6; color: white;}') 
        elif numOfBombs == 6:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #151e3d; color: white;}') 
        elif numOfBombs == 7:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #022d36; color: white;}') 
        elif numOfBombs == 8:
            self.btns[pos].setStyleSheet('QPushButton {background-color: #82eefd; color: white;}')
        

    
    def addCells(self , pos):

        position = pos.split('+')
        i = int (position[0])
        j = int (position[1])

        if pos in self.flags:
            return



        dx = [-1 , 0  , 1  , 1 , 1 , 0 , -1 , -1]
        dy = [-1 , -1 , -1 , 0 , 1 , 1 , 1  , 0]
        for k in range(8):
            newRow = i + dy[k]
            newCol = j + dx[k]
            if  (newRow >= 0 and newRow < self.height and newCol >= 0 and newCol < self.width) :

                newKey = str(newRow) + "+" +str(newCol)
                if len(self.btns[newKey].text()) == 0 :
                    self.pickColor(newKey , self.grid[newRow][newCol])


            

    def timeInSecs(self):
        text = self.timerLabel.text().split(':')
        return int(text[0]) * 3600 + int(text[1]) * 60 + int(text[2])
    
    def showWinningDialog(self):

        self.isStarted = False

        scores = ""

        with open(f'{self.width}*{self.height}*{self.mines}' , 'a') as file:
            time = self.timeInSecs()
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M")
            file.write(f"{dt_string}              {time} seconds \n")
 

        with open(f'{self.width}*{self.height}*{self.mines}' , 'r') as file:
            scores = file.readlines()
        



        msgBox = QMessageBox.information(self , "Congratulations \n play again",
        
            "\n".join(scores),
          QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
        
        if (msgBox == QMessageBox.Cancel):
            sys.exit()
        else:
            self.close()
            window = MinesGame(self.width , self.height , self.mines , self.app)
            window.show()

    def showLosingDialog(self):

        self.isStarted = False

        msgBox = QMessageBox.information(self , "Better luck next time",
         "You lost the last game do you want to play again?",
          QMessageBox.Cancel | QMessageBox.Yes, QMessageBox.Cancel)
        
        if (msgBox == QMessageBox.Cancel):
            sys.exit()
        else:
            self.close()
            window = MinesGame(self.width ,self.height , self.mines , self.app)
            window.show()
        

    def startDigging(self , i , j):
        
        dx = [-1 , 0  , 1  , 1 , 1 , 0 , -1 , -1]
        dy = [-1 , -1 , -1 , 0 , 1 , 1 , 1  , 0]

        for k in range(8):

            newRow = i + dy[k]
            newCol = j + dx[k]

            pos = str(newRow) + "+" + str(newCol)
            if  (newRow >= 0 and newRow < self.height and newCol >= 0 and newCol < self.width) :
                if self.grid[newRow][newCol] == -1 and pos not in self.flags:
                    self.btns[pos].setStyleSheet("image: url('nuclear-bomb(2).png'); border: none; border: 2px solid white;")
                    self.btns[pos].setText('')
                    self.showLosingDialog()

                elif len(self.btns[pos].text()) != 0 :
                    continue

                else:
                    self.pickColor(pos , self.grid[newRow][newCol])

                    


    def circulate(self , i , j , text):
        surMines = 0 

        dx = [-1 , 0  , 1  , 1 , 1 , 0 , -1 , -1]
        dy = [-1 , -1 , -1 , 0 , 1 , 1 , 1  , 0]

        for k in range(8):
            newRow = i + dy[k]
            newCol = j + dx[k]
            if  (newRow >= 0 and newRow < self.height and newCol >= 0 and newCol < self.width) :
                if str(newRow) + "+" + str(newCol) in self.flags:
                    surMines+=1
            
        if surMines == int(text):
            self.startDigging( i , j )





    def clicked(self , i , j):

        self.isStarted = True

        pos = self.sender().text()
        


        if ( len (pos) != 0):
            self.circulate( i , j , pos)
            return

        pos = str(i) + "+" + str(j)

        if pos in self.flags:
            return

        if (self.grid[i][j] == -1):
            self.btns[pos].setStyleSheet("image: url('nuclear-bomb(2).png'); border: none; border: 2px solid white;")
            self.btns[pos].setText('')
            self.showLosingDialog()

        self.pickColor(pos , self.grid[i][j])
        


    def checkWinning(self):
        
        for i in range(self.height):
            for j in range(self.width):
                key = str(i) + "+" + str(j)
                if self.grid[i][j] == -1 and key not in self.flags:
                    return
        self.showWinningDialog()

    def handle_right_click( self , i , j):

        text = self.sender().text()

        if len(text) != 0 :
            return

        pos = str (i) + "+" + str (j)
        if pos not in self.flags:
            self.flags.add(pos)
            self.btns[pos].setStyleSheet("image: url('finish(1).png'); border: 2px solid white;")
            if len (self.flags) == self.mines:
                self.scoreLabel.setText(f"{self.mines}/{self.mines}")
                self.checkWinning()
        else:
            self.flags.remove(pos)
            self.btns[pos].setStyleSheet("background-color : black; border: 2px solid white;")
        self.scoreLabel.setText(f"{len(self.flags)}/{self.mines}")
        


    def getSize(self , width , height):
        return min(width // self.width , height // self.height)
        

    def restartGame(self):
        self.close()
        window = MinesGame(self.width ,self.height , self.mines , self.app)
        window.show()


    def updateTime(self):


        if not self.isStarted:
            return

        time = self.timerLabel.text().split(':')

        hrs =  int(time[0])
        mnts = int(time[1])
        secs = int(time[2])

        if secs < 59:
            secs+=1
        else:
            secs = 0
            mnts+=1
            if mnts == 60:
                mnts = 0
                hrs+=1
        
        self.timerLabel.setText(f"{hrs}:{mnts}:{secs}")



        

    def createTimer(self):

        self.timerLabel = QLabel('00:00:00')
        self.timerLabel.setStyleSheet("border : 1px solid black")
        self.timerLabel.setFont(QtGui.QFont('Times', 15))
        self.timerLabel.setAlignment(Qt.AlignCenter)

        timer = QtCore.QTimer(self)
        timer.timeout.connect(lambda:self.updateTime())
        timer.start(1000)




    def initGUI(self):
        self.setWindowTitle('Mines')
        
        size = self.app.primaryScreen().size()

        width = size.width() ; height = size.height()

        self.setFixedSize(width , height - 60)

        btnsize = int (self.getSize(width * 0.8  , height - 50  ))

        main_layout = QHBoxLayout()

        grid_layout = QGridLayout()

        image = QPixmap('finish (3).png')

        label = QLabel()

        vertical_layout = QVBoxLayout()

        label.setPixmap(image)



        vertical_layout.addWidget(self.timerLabel , alignment=Qt.AlignCenter)
        
        self.scoreLabel.setFont(QtGui.QFont('Times', 20))
        vertical_layout.addWidget(label, alignment=Qt.AlignCenter)
        vertical_layout.addWidget(self.scoreLabel, alignment=Qt.AlignCenter)
        
        restartBtn = QPushButton()
        restartBtn.setText('Restart Game')
        restartBtn.clicked.connect(lambda:self.restartGame())
        restartBtn.setFixedSize(200 , 100)
        vertical_layout.addWidget(restartBtn , alignment=Qt.AlignCenter)


        endBtn = QPushButton()
        endBtn.setText('End Game')
        endBtn.clicked.connect(lambda:sys.exit())
        endBtn.setFixedSize(200 , 100)
        vertical_layout.addWidget(endBtn , alignment=Qt.AlignCenter)


        

        # adding Empty Labels for margin
        vertical_layout.addWidget(QLabel())
        vertical_layout.addWidget(QLabel())


        



        for i in range(self.height):
            for j in range(self.width):
                
                key = str(i) + "+" + str(j)
                self.btns[key] = QPushButton()
                self.btns[key].setFixedSize(btnsize , btnsize)


                
                self.btns[key].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                self.btns[key].customContextMenuRequested.connect(partial(self.handle_right_click , i , j))
                self.btns[key].clicked.connect(partial(self.clicked , i , j))
                self.btns[key].setStyleSheet('QPushButton {background-color: black; color: #022d36; border: 1px solid white}')


                grid_layout.addWidget(self.btns[key] , i , j)



        main_layout.addLayout(grid_layout )

        main_layout.addLayout(vertical_layout )

        self.setLayout(main_layout)







        

            
            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MinesGame(16 , 16 , 60)
    window.show()
    sys.exit(app.exec_())
        

