from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QAbstractItemView
from PyQt5.QtCore import Qt
import threading
import sqlite3
import os

class Ui_ClientListDialog(object):
	def getAllNickname(self):
		BASE_DIR = os.path.dirname(os.path.abspath(__file__)) + "/Server/Data/data.db"
		con  = sqlite3.connect(BASE_DIR)
		sql = "SELECT nickname FROM " + self.clientTableName + ";"
		cur = con.execute(sql)
		l = []
		for n, row in enumerate(cur):
			for m, col in enumerate(row):
				l.append(str(col))
		con.close()
		return l

	def updateClientList(self):
		allNicknameList = self.getAllNickname()
		for nickname in allNicknameList:
			isFound = False
			for online in self.onlineList:
				if nickname == online:
					self.clientList.addItem(nickname + " - Online")
					isFound = True
					break
			if isFound == False:
				self.clientList.addItem(nickname)

	def setupUi(self, ClientListDialog, clientTableName, onlineList):
		self.clientTableName = clientTableName
		self.onlineList = onlineList

		ClientListDialog.setObjectName("ClientListDialog")
		ClientListDialog.resize(300, 450)

		self.clientList = QtWidgets.QListWidget(ClientListDialog)
		self.clientList.setGeometry(QtCore.QRect(10, 10, 281, 391))
		font = QtGui.QFont()
		font.setPointSize(10)
		self.clientList.setFont(font)
		self.clientList.setSelectionMode(QAbstractItemView.NoSelection)

		self.buttonBox = QtWidgets.QDialogButtonBox(ClientListDialog)
		self.buttonBox.setGeometry(QtCore.QRect(210, 410, 81, 31))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
		self.buttonBox.setObjectName("buttonBox")

		self.updateClientList()
		self.buttonBox.rejected.connect(ClientListDialog.close)

		self.retranslateUi(ClientListDialog)

	def retranslateUi(self, ClientListDialog):
		_translate = QtCore.QCoreApplication.translate
		ClientListDialog.setWindowTitle(_translate("ClientListDialog", "Cloud Chat - Client list"))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	ClientListDialog = QtWidgets.QDialog()
	ClientListDialog.setWindowFlag(Qt.FramelessWindowHint)
	ui = Ui_ClientListDialog()
	ui.setupUi(ClientListDialog)
	ClientListDialog.show()
	sys.exit(app.exec_())