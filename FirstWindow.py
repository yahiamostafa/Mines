from PyQt5.QtWidgets import (QApplication , QWidget  ,QPushButton , QGridLayout  , QInputDialog)
from PyQt5 import  QtGui 
import sys
import Mines


class FirstWindow(QWidget):
    def __init__(self):
        super().__init__()

        grid_layout = QGridLayout()

        size = app.primaryScreen().size()

        width = size.width() ; height = size.height()

        self.setFixedSize(width , height)

        btnSize = self.getSize(width - 100 , height - 100)

        btn1 = QPushButton()
        btn1.setText("8 x 8\n 10 mines")
        btn1.setFixedSize(btnSize , btnSize)
        btn1.setStyleSheet("QPushButton { text-align: center; }")
        btn1.setFont(QtGui.QFont('Times', 16))
        btn1.clicked.connect(lambda : self.startGame(8 , 8 , 10))
        grid_layout.addWidget( btn1 , 0 , 0 )

        btn2 = QPushButton()
        btn2.setText("16 x 16\n 40 mines")
        btn2.setFixedSize(btnSize , btnSize)
        btn2.setStyleSheet("QPushButton { text-align: center; }")
        btn2.setFont(QtGui.QFont('Times', 16))
        btn2.clicked.connect(lambda : self.startGame(16 , 16 , 40))
        grid_layout.addWidget( btn2 ,  0 ,  1 )

        btn3 = QPushButton()
        btn3.setText("30 x 16\n 99 mines")
        btn3.setFixedSize(btnSize , btnSize)
        btn3.setStyleSheet("QPushButton { text-align: center; }")
        btn3.setFont(QtGui.QFont('Times', 16))
        btn3.clicked.connect(lambda : self.startGame(30 , 16 , 99))
        grid_layout.addWidget( btn3 , 1 ,  0 )

        btn4 = QPushButton()
        btn4.setText("?\n Custom")
        btn4.setFixedSize(btnSize , btnSize)
        btn4.setStyleSheet("QPushButton { text-align: center; }")
        btn4.setFont(QtGui.QFont('Times', 16))
        btn4.clicked.connect(self.takeInputs)
        grid_layout.addWidget( btn4 ,  1 ,  1 )
        

        self.setLayout(grid_layout)

    

    def takeInputs(self):
        width , dn1 = QInputDialog.getInt(
            self , 'Input Dialog' , 'Width'
        )
        height , dn2 = QInputDialog.getInt(
            self , 'Input Dialog' , 'Height'
        )
        mines , dn3 = QInputDialog.getInt(
            self , 'Input Dialog' , 'Number of Mines'
        )

        if dn1 and dn2 and dn3 and width * height > mines:
            self.startGame(width , height , mines )

    def startGame(self , width , height , mines):
    
        self.close()
        window = Mines.MinesGame(width , height , mines , app)
        window.show()

    
    def getSize(self , width , height):
        return min (width // 2 , height // 2)





app = QApplication(sys.argv)
window = FirstWindow()
window.show()
sys.exit(app.exec_())
