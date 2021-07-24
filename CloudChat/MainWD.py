from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from HostDialog import Ui_HostDialog
from JoinDialog import Ui_JoinDialog
import threading
import os

class Ui_StartWD(object):
	def hostBTClicked(self):
		dialog = MyHostDialog()
		dialog.exec_()
		window.close()

	def joinBTClicked(self):
		dialog = MyJoinDialog()
		dialog.exec_()
		window.close()

	def setupUi(self, StartWD):
		self.hostDialog = QtWidgets.QDialog()
		self.joinDialog = QtWidgets.QDialog()
		StartWD.setObjectName("StartWD")
		StartWD.resize(300, 450)
		StartWD.setMinimumSize(QtCore.QSize(300, 450))
		StartWD.setMaximumSize(QtCore.QSize(300, 450))

		font = QtGui.QFont()
		font.setPointSize(10)
		StartWD.setFont(font)
		self.centralwidget = QtWidgets.QWidget(StartWD)
		self.centralwidget.setObjectName("centralwidget")

		self.hostBT = QtWidgets.QPushButton(self.centralwidget)
		self.hostBT.setGeometry(QtCore.QRect(75, 140, 150, 75))
		self.hostBT.setObjectName("hostBT")
		self.hostBT.setStyleSheet(stylesheet)
		self.hostBT.setToolTip('Host a Server')

		self.joinBT = QtWidgets.QPushButton(self.centralwidget)
		self.joinBT.setGeometry(QtCore.QRect(75, 280, 150, 75))
		self.joinBT.setObjectName("joinBT")
		self.joinBT.setStyleSheet(stylesheet)
		self.joinBT.setToolTip('Join a Server')

		self.label = QtWidgets.QLabel(self.centralwidget)
		self.label.setGeometry(QtCore.QRect(10, 410, 171, 16))
		font = QtGui.QFont()
		font.setPointSize(8)
		self.label.setFont(font)
		self.label.setObjectName("label")
		
		StartWD.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(StartWD)
		self.statusbar.setObjectName("statusbar")
		StartWD.setStatusBar(self.statusbar)

		#Chức năng
		self.hostBT.clicked.connect(self.hostBTClicked)
		self.joinBT.clicked.connect(self.joinBTClicked)

		self.retranslateUi(StartWD)
		QtCore.QMetaObject.connectSlotsByName(StartWD)

	def retranslateUi(self, StartWD):
		_translate = QtCore.QCoreApplication.translate
		StartWD.setWindowTitle(_translate("StartWD", "Cloud Chat"))
		self.hostBT.setText(_translate("StartWD", "HOST"))
		self.hostBT.setShortcut(_translate("StartWD", "h"))
		self.joinBT.setText(_translate("StartWD", "JOIN"))
		self.joinBT.setShortcut(_translate("StartWD", "Enter"))
		self.label.setText(_translate("StartWD", "A program by Error404 Team"))

class MyWindow(QtWidgets.QMainWindow, Ui_StartWD, ):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

class MyHostDialog(QtWidgets.QDialog, Ui_HostDialog):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

class MyJoinDialog(QtWidgets.QDialog, Ui_JoinDialog):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

stylesheet = """
	QMainWindow 
	{
		background-image: url("Images/bg2.png"); 
		background-repeat: no-repeat; 
		background-position: center;
	}

	QDialog 
	{
		background-image: url("Images/cloudIMG.jpg"); 
		background-repeat: no-repeat; 
		background-position: left;
	}

	QPushButton 
	{
		background-color: #ffffff;
		color: rgb(37, 166, 250);
		border-style: outset;
		border-width: 5px;
		border-color: rgb(196, 240, 251);
		border-radius: 20px;
		font: bold 14px;
		padding: 5px;
		width: 100px;
	}

	QPushButton:hover 
	{
		background-color: rgb(37, 166, 250);
		color: #ffffff;
	}

	QLineEdit {
		background-color: #ffffff;
		color: rgb(37, 166, 250);
		border-style: outset;
		border-width: 5px;
		border-color: rgb(196, 240, 251);
		border-radius: 20px;
		font: 14px;
	}

	QTextEdit {
		background-color: #ffffff;
		color: rgb(37, 166, 250);
		border-style: outset;
		border-width: 5px;
		border-color: rgb(196, 240, 251);
		border-radius: 20px;
		font: bold 11px;
	}

	QListWidget {
		background-color: #ffffff;
		color: rgb(37, 166, 250);
		border-style: outset;
		border-width: 5px;
		border-color: rgb(196, 240, 251);
		border-radius: 20px;
		font: 14px;
	}

	QMessageBox QLabel {
		color: #ffffff;
		font: bold 14px;
	}

	QMessageBox {
		background-image: url("Images/cloudIMG.jpg"); 
		background-repeat: no-repeat; 
		background-position: top;
	}
"""

stylesheet1 = """
	QPushButton {
		background-image: url(Images/x.png);
		background-repeat: no-repeat;
		background-position: center;
	}
"""



if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	app.setStyleSheet(stylesheet)
	app.setQuitOnLastWindowClosed(True)
	window = MyWindow()
	window.show()
	sys.exit(app.exec_())
