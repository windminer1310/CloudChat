from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ServerWD import Ui_ServerWD

class Ui_HostDialog(object):
	def showError(self):
		msg = QMessageBox()
		msg.setWindowTitle("Error!")
		msg.setIcon(QMessageBox.Critical)
		msg.setText("IP or Port is invalid!")
		msg.setStandardButtons(QMessageBox.Ok)
		x = msg.exec_()

	def getIP(self):
		return str(self.ipLE.text())

	def getPort(self):
		return int(self.portLE.text())

	def IPChecking(self):
		ip = self.getIP()
		count = 0
		stPos = 0
		for i in range(len(ip)):
			if ip[i] == '.':
				part = ip[stPos:i]
				try:
					num = int(part)
					if num >= 0 and num <= 255:
						count += 1
						stPos = i + 1
				except:
					return False
		if count == 3:
			return True
		else:
			return False

	def portChecking(self):
		port = str(self.getPort())
		if port.isnumeric():
			return True
		else:
			return False

	def buttonOKClicked(self):
		if self.IPChecking()  == True and self.portChecking() == True:
			window = MyWindow(self.getIP(), self.getPort())
			window.show()
		else:   
			self.showError()

	def setupUi(self, HostDialog):
		HostDialog.setObjectName("HostDialog")
		HostDialog.resize(300, 450)
		HostDialog.setMinimumSize(QtCore.QSize(300, 450))
		HostDialog.setMaximumSize(QtCore.QSize(300, 450))

		self.ipLE = QtWidgets.QLineEdit(HostDialog)
		self.ipLE.setGeometry(QtCore.QRect(10, 120, 281, 30))
		self.ipLE.setObjectName("ipLE")

		self.portLE = QtWidgets.QLineEdit(HostDialog)
		self.portLE.setGeometry(QtCore.QRect(10, 230, 281, 30))
		self.portLE.setObjectName("portLE")

		self.hostLB = QtWidgets.QLabel(HostDialog)
		self.hostLB.setGeometry(QtCore.QRect(10, 10, 280, 30))
		font = QtGui.QFont()
		font.setPointSize(12)
		font.setBold(True)
		font.setWeight(75)
		self.hostLB.setFont(font)
		self.hostLB.setObjectName("hostLB")
		self.hostLB.setAlignment(QtCore.Qt.AlignCenter)
		self.hostLB.setStyleSheet(stylesheet1)

		self.portLB = QtWidgets.QLabel(HostDialog)
		self.portLB.setGeometry(QtCore.QRect(10, 180, 100, 30))
		self.portLB.setStyleSheet(stylesheet)
		self.portLB.setObjectName("portLB")
		self.portLB.setAlignment(QtCore.Qt.AlignCenter)

		self.ipLB = QtWidgets.QLabel(HostDialog)
		self.ipLB.setGeometry(QtCore.QRect(10, 70, 100, 30))
		self.ipLB.setStyleSheet(stylesheet)
		self.ipLB.setObjectName("ipLB")
		self.ipLB.setAlignment(QtCore.Qt.AlignCenter)

		self.buttonBox = QtWidgets.QDialogButtonBox(HostDialog)
		self.buttonBox.setGeometry(QtCore.QRect(130, 410, 161, 32))
		self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
		self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
		self.buttonBox.setObjectName("buttonBox")

		#Chức năng
		self.buttonBox.accepted.connect(self.buttonOKClicked)

		self.retranslateUi(HostDialog)
		QtCore.QMetaObject.connectSlotsByName(HostDialog)
		self.buttonBox.accepted.connect(HostDialog.accept)
		self.buttonBox.rejected.connect(HostDialog.reject)

	def retranslateUi(self, HostDialog):
		_translate = QtCore.QCoreApplication.translate
		HostDialog.setWindowTitle(_translate("HostDialog", "Cloud Chat"))
		self.hostLB.setText(_translate("HostDialog", "Host Server"))
		self.portLB.setText(_translate("HostDialog", "Port server"))
		self.ipLB.setText(_translate("HostDialog", "IP server"))

class MyWindow(QtWidgets.QMainWindow, Ui_ServerWD):
	def __init__(self, ip, port):
		super().__init__()
		self.setupUi(self, ip, port)

stylesheet = """
	QLabel {
		background-color: #ffffff;
		color: rgb(37, 166, 250);
		border-style: outset;
		border-width: 5px;
		border-color: rgb(196, 240, 251);
		border-radius: 20px;
		font: bold 14px;
	}
"""

stylesheet1 = """
	QLabel {
		color: #ffffff;
		font: bold 20px;
	}
"""

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	HostDialog = QtWidgets.QDialog()
	ui = Ui_HostDialog()
	ui.setupUi(HostDialog)
	HostDialog.show()
	sys.exit(app.exec_())
