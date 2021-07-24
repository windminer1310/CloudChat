from ClientListDialog import Ui_ClientListDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QColor
import subprocess
import threading
import datetime
import sqlite3
import socket
import codecs
import time
import sys
import os


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def killPort(port):
	find_port = 'netstat -aon | findstr %s' % port
	result = os.popen(find_port)
	text = result.read()
	text = [i.split(' ') for i in text.split('\n') if i]
	pids = []
	for i in text:
		pid = [u for u in i if u]
		if str(port) in pid[1]:
			pids.append(pid[-1])
	pids = list(set(pids))
	for pid in pids:
		find_kill = 'taskkill -f -pid %s' % pid
		result = os.popen(find_kill)

class MyClientListDialog(QtWidgets.QDialog, Ui_ClientListDialog):
	def __init__(self, clientTableName, onlineList):
		super().__init__()
		self.setupUi(self, clientTableName, onlineList)

class Ui_ServerWD(object):
	def showClientList(self):
		dialog = MyClientListDialog(self.clientTableName, self.nicknames)
		dialog.exec_()

	def closeEvent(self, event):
		close = QMessageBox()
		close.setWindowTitle("Close")
		close.setText("Are you sure?")
		close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
		close = close.exec()
		if close == QMessageBox.Yes:
			runnable = False
			server.close()
			event.accept()
		else:
			event.ignore()

	def setCurrentTime(self):
		while True:
			currentTime = datetime.datetime.now()
			self.date = currentTime.strftime("%d/%m/%Y")
			self.time = currentTime.strftime("%H:%M:%S")
			self.dateLB.setText(self.date)
			self.timeLB.setText(self.time)

	def changeTrackingFlag(self):
		if self.trackingFlag == True:
			self.trackingFlag = False
			self.reportTE.setTextColor(QColor(255, 0, 0))
			self.reportTE.append("Tracking is off!")
		else:
			self.trackingFlag = True
			self.reportTE.setTextColor(QColor(255, 0, 0))
			self.reportTE.append("Tracking is on!")

	def changeRecordingFlag(self):
		self.recordingFlag += 1
		if self.recordingFlag % 2 == 0:
			currentTime = datetime.datetime.now()
			self.time = currentTime.strftime("%H:%M:%S")
			self.reportTE.setTextColor(QColor(30, 255, 0))
			self.reportTE.append(self.time + ": Stop record!")
			self.reportTE.setTextColor(QColor(0, 0, 0))
			self.reportTE.append("Record saving in: " + self.recordName)
			self.recordBT.setToolTip('Start tracking the conversation in chat room')
		else:
			currentTime = datetime.datetime.now()
			self.time = currentTime.strftime("%H:%M:%S")
			self.reportTE.setTextColor(QColor(30, 255, 0))
			self.reportTE.append(self.time + ": Start record!")
			self.recordName = str(currentTime.strftime("%d-%m-%Y")) + "-" + str(self.ip) + "-" + str(self.port) + ".txt"
			self.recordBT.setToolTip('Stop tracking the conversation in chat room')

	def IPTransform(self):
		s = ""
		for i in range(len(self.ip)):
			if (self.ip[i] == "."):
				s += "_"
			else:
				s += self.ip[i]
		return s

	def getNickname_Message(self, msg):
		index = 0
		for i in range(len(msg)):
			if msg[i] == ":":
				index = i
				break
		return msg[:index], msg[index + 1:len(msg)]

	def getRowCount(self, cur):
		count = 0
		for row in enumerate(cur):
			count += 1
		return count

	def getMessageCount(self):
		con = sqlite3.connect(self.dataDIR)
		sql = "SELECT MAX(no) FROM " + self.messageTableName + ";"
		cur = con.execute(sql)
		count = 0
		for n, row in enumerate(cur):
			for m, col in enumerate(row):
				count = int(col)
		con.close()
		return count

	def createData(self):
		con = sqlite3.connect(self.dataDIR)
		ip = self.IPTransform()
		sql = "CREATE TABLE IF NOT EXISTS " + self.clientTableName + " (no INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, nickname TEXT);"
		cur = con.cursor()
		cur.execute(sql)
		sql = "CREATE TABLE IF NOT EXISTS " + self.messageTableName + " (no INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, datetime datetime, nickname TEXT, message TEXT);"
		cur.execute(sql)
		con.commit()
		con.close()

	def addMessage(self, message):
		ip = self.IPTransform()
		nickname, msg = self.getNickname_Message(message)
		con = sqlite3.connect(self.dataDIR)
		sql = "INSERT INTO " + self.messageTableName + " (datetime, nickname, message) VALUES ('" + self.date + " " + self.time + "', '" + nickname + "', '" + msg + "');"
		cur = con.execute(sql)
		con.commit()
		con.close()

	def addNickname(self, client, nickname):
		con = sqlite3.connect(self.dataDIR)
		ip = self.IPTransform()
		sql = "SELECT nickname FROM " + self.clientTableName + " WHERE nickname = '" + nickname + "';"
		cur = con.execute(sql)
		if self.getRowCount(cur) != 0:
			if (self.getMessageCount() > 10):
				sql = "SELECT * FROM " + self.messageTableName + " WHERE no > " + str(self.getMessageCount() - 10) + ";"
			else:
				sql = "SELECT * FROM " + self.messageTableName + ";"
			cur = con.execute(sql)
			client.send("LOAD:Loading last chat!".encode("utf-8"))
			time.sleep(1)
			for n, row in enumerate(cur):
				datetime = ""
				nkname = ""
				message = ""
				for m, col in enumerate(row):
					if m == 1:
						datetime = str(col)
					if m == 2:
						nkname = str(col)
					if m == 3:
						message = str(col)
				msg = "LOAD:" + datetime + ": " + nkname + ": " + message
				client.send(msg.encode("utf-8"))
				time.sleep(0.25)
		else:
			sql = "INSERT INTO " + self.clientTableName + " (nickname) VALUES ('" + nickname + "');"
		cur = con.execute(sql)
		con.commit()
		con.close()

	def broadcast(self, message, typeMSG, client = None):
		if self.trackingFlag == True and typeMSG == 0:
			self.reportTE.setTextColor(QColor(0, 0, 0))
			currentTime = datetime.datetime.now()
			self.time = currentTime.strftime("%H:%M:%S")
			self.reportTE.append(self.time + ": " + message.decode("utf-8"))

		if self.recordingFlag != 0 and self.recordingFlag % 2 != 0 and typeMSG == 0:
			currentTime = datetime.datetime.now()
			self.time = currentTime.strftime("%H:%M:%S")
			date1 = currentTime.strftime("%d-%m-%Y")
			file = codecs.open(self.BASE_DIR + "/Server/Records/" + self.recordName, "a", "utf-8")
			file.writelines("\n" + self.time + ": " + message.decode("utf-8"))
			file.close()
		for client1 in self.clients:
			if client1 != client:
				client1.sendall(message)

	def handle(self, client):
		try:
			while self.runnable == True:
				message = client.recv(4096)
				self.broadcast(message, 0, client)
				msg = message.decode("utf-8")
				self.addMessage(msg)

				if msg[:5] == "FILE:":
					self.fileName = msg[5:len(msg)]
					if (self.recordingFlag != 0 and self.recordingFlag % 2 != 0):
						with open(self.BASE_DIR + "/Server/Recieves/" + self.fileName, "wb") as file:
							while True: 
								fileData = client.recv(4096)
								file.write(fileData)
								try:
									self.broadcast(fileData, 2, client)
								except:
									pass
								if len(fileData) < 4096:
									break
					else:
						while True: 
							fileData = client.recv(4096)
							self.broadcast(fileData, 2, client)
							if len(fileData) < 4096:
								break
		except:
			index = self.clients.index(client)
			self.clients.remove(client)
			client.close()
			nickname = self.nicknames[index]
			self.broadcast('Nickname {} left!'.format(nickname).encode('utf-8'), 1)
			self.reportTE.setTextColor(QColor(255, 0, 0))
			currentTime = datetime.datetime.now()
			self.time = currentTime.strftime("%H:%M:%S")
			self.reportTE.append(self.time + ": Nickname "+ nickname +' left!')
			self.nicknames.remove(nickname)
	def receive(self):
		try:
			while self.runnable == True:
				client, address = server.accept()
				self.reportTE.setTextColor(QColor(0, 0, 0))
				currentTime = datetime.datetime.now()
				self.time = currentTime.strftime("%H:%M:%S")
				self.reportTE.append(self.time + ": Connected with " + str(address))
				client.send('NICK'.encode('utf-8'))
				nickname = client.recv(1024).decode('utf-8')
				self.nicknames.append(nickname)
				self.clients.append(client)
				self.reportTE.append("Nickname is " + str(nickname))
				thread1 = threading.Thread(target=self.addNickname, args=(client, nickname))
				thread1.start()
				self.broadcast("{} joined!".format(nickname).encode('utf-8'), 1, client)
				client.send('Connected to server!'.encode('utf-8'))
				thread2 = threading.Thread(target=self.handle, args=(client,))
				thread2.start()
		except:
			self.reportTE.setTextColor(QColor(80, 0, 255))
			self.reportTE.append(self.time + ": " + "An error occured!")
			server.close()

	def runServer(self):
		killPort(self.port)
		server.bind((self.ip, self.port))
		server.listen()
		self.reportTE.setTextColor(QColor(30, 255, 0))
		currentTime = datetime.datetime.now()
		self.time = currentTime.strftime("%H:%M:%S")
		self.reportTE.append(self.time + ": Server is running!")
		self.reportTE.setTextColor(QColor(80, 0, 255))
		self.reportTE.append("Server IP: " + self.ip)
		self.reportTE.append("Server Port: " + str(self.port))
		self.runnable = True
		self.createData()
		self.receive()

	def setupUi(self, ServerWD, ip, port):
		self.ip = ip
		self.port = port

		self.clients = []
		self.nicknames = []

		self.trackingFlag = False
		self.recordingFlag = 0
		self.runnable = False


		self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		self.dataDIR = self.BASE_DIR + "/Server/Data/data.db"
		self.messageTableName = "S" + self.IPTransform() + "_" + str(self.port)
		self.clientTableName = "S" + self.IPTransform() + "_" + str(self.port) + "_clients"

		ServerWD.setObjectName("ServerWD")
		ServerWD.resize(350, 450)
		ServerWD.setMinimumSize(QtCore.QSize(350, 450))
		ServerWD.setMaximumSize(QtCore.QSize(350, 450))
		self.centralwidget = QtWidgets.QWidget(ServerWD)
		self.centralwidget.setObjectName("centralwidget")

		self.dateLB = QtWidgets.QLabel(self.centralwidget)
		self.dateLB.setGeometry(QtCore.QRect(10, 10, 75, 13))
		self.dateLB.setStyleSheet(stylesheet)
		self.dateLB.setObjectName("dateLB")

		self.timeLB = QtWidgets.QLabel(self.centralwidget)
		self.timeLB.setGeometry(QtCore.QRect(290, 10, 65, 13))
		self.timeLB.setStyleSheet(stylesheet)
		self.timeLB.setObjectName("timeLB")

		self.reportTE = QtWidgets.QTextEdit(self.centralwidget)
		self.reportTE.setGeometry(QtCore.QRect(10, 30, 331, 357))
		self.reportTE.setReadOnly(True)
		self.reportTE.setObjectName("reportTE")

		self.trackingBT = QtWidgets.QPushButton(self.centralwidget)
		self.trackingBT.setGeometry(QtCore.QRect(10, 395, 35, 35))
		self.trackingBT.setStyleSheet(stylesheet)
		self.trackingBT.setObjectName("trackingBT")
		self.trackingBT.setToolTip('Tracking the conversation in chat room')

		self.recordBT = QtWidgets.QPushButton(self.centralwidget)
		self.recordBT.setGeometry(QtCore.QRect(305, 395, 35, 35))
		self.recordBT.setStyleSheet(stylesheet1)
		self.recordBT.setObjectName("recordBT")
		self.recordBT.setToolTip('Start tracking the conversation in chat room')

		self.listBT = QtWidgets.QPushButton(self.centralwidget)
		self.listBT.setGeometry(QtCore.QRect(158, 395, 35, 35))
		self.listBT.setStyleSheet(stylesheet2)
		self.listBT.setObjectName("listBT")
		self.listBT.setToolTip('Show all client in chat room')

		ServerWD.setCentralWidget(self.centralwidget)
		self.statusbar = QtWidgets.QStatusBar(ServerWD)
		self.statusbar.setObjectName("statusbar")

		ServerWD.setStatusBar(self.statusbar)

		#Tự động
		self.datetimeThread = threading.Thread(target = self.setCurrentTime)
		self.datetimeThread.start()
		serverThread = threading.Thread(target = self.runServer)
		serverThread.start()
		#Chức năng
		self.trackingBT.clicked.connect(self.changeTrackingFlag)
		self.recordBT.clicked.connect(self.changeRecordingFlag)
		self.listBT.clicked.connect(self.showClientList)

		self.retranslateUi(ServerWD)
		QtCore.QMetaObject.connectSlotsByName(ServerWD)

	def retranslateUi(self, ServerWD):
		_translate = QtCore.QCoreApplication.translate
		ServerWD.setWindowTitle(_translate("ServerWD", "Cloud Chat - Server"))
		self.dateLB.setText(_translate("ServerWD", "TextLabel"))
		self.timeLB.setText(_translate("ServerWD", "TextLabel"))

stylesheet = """
	QLabel {
		font: bold 10px;
		color: #ffffff;
	}

	QPushButton {
		background-image: url(Images/eye.png);
		background-repeat: no-repeat;
		background-position: center;
	}
"""

stylesheet1 = """
	QPushButton {
		background-image: url(Images/record.png);
		background-repeat: no-repeat;
		background-position: center;
	}
"""

stylesheet2 = """
	QPushButton {
		background-image: url(Images/list.png);
		background-repeat: no-repeat;
		background-position: center;
	}
"""

class ServerWindow(QtWidgets.QMainWindow):
	def closeEvent(self, event):
		state = False
		server.close()
		event.accept()

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	ServerWD = ServerWindow()
	ui = Ui_ServerWD()
	ui.setupUi(ServerWD, "127.0.0.1", 55555)
	ServerWD.show()
	sys.exit(app.exec_())

