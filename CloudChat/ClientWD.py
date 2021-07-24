from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QColor
from plyer import notification
import threading
import datetime
import socket
import codecs
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class Ui_ClientWD(object):
    def setCurrentTime(self):
        while True:
            currentTime = datetime.datetime.now()
            self.date = currentTime.strftime("%d/%m/%Y")
            self.time = currentTime.strftime("%H:%M:%S")
            self.dateLB.setText(self.date)
            self.timeLB.setText(self.time)

    def closeEvent(self, event):
        close = QMessageBox()
        close.setText("Are you sure?")
        close.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        close = close.exec()
        if close == QMessageBox.Yes:
            self.runnable = False
            event.accept()
        else:
            event.ignore()

    def notifyMessage(self, message):
        index = 0
        for i in range(len(message)):
            if message[i] == ":":
                index = i + 1
        client = message[:index]
        msg = message[index:]
        notification.notify(
            title=client,
            message=msg,
            timeout=10,
            app_name='Cloud Chat',
            app_icon='',
        )

    def changeNotificationState(self):
        if (self.notificationState == False):
            self.notificationState = True
            self.notificationBT.setStyleSheet(stylesheet3)
            self.notificationBT.setToolTip('Turn off notification')
        else:
            self.notificationState = False
            self.notificationBT.setStyleSheet(stylesheet2)
            self.notificationBT.setToolTip('Turn on notification')

    def browseFile(self):
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        fname = QFileDialog.getOpenFileName(QFileDialog(), 'Open file', BASE_DIR)
        self.filePath = fname[0]
        if self.filePath != "":
            index = 0
            for i in range(len(self.filePath) - 1, 0, -1):
                if self.filePath[i] == "/":
                    index = i + 1
                    break
            self.fileName = self.filePath[index:len(self.filePath)]
            self.chatBoxTE.setTextColor(QColor(0, 255, 255))
            currentTime = datetime.datetime.now()
            self.time = currentTime.strftime("%H:%M:%S")
            self.chatBoxTE.append(self.time + ": " + "Sending: " + self.fileName)
            client.send(str('FILE:' + self.fileName).encode('utf-8'))
            currentTime = datetime.datetime.now()
            with codecs.open(self.filePath, "rb") as file:
                while True:
                    fileData = file.read(4096)
                    if not fileData: 
                        break
                    client.sendall(fileData)
            currentTime = datetime.datetime.now()
            self.time = currentTime.strftime("%H:%M:%S")
            self.chatBoxTE.append(self.time + ": " + "File sending completed!")
    

    def receive(self):
        try:
            while self.runnable == True:
                BASE_DIR = os.path.dirname(os.path.abspath(__file__))
                message = client.recv(4096).decode('utf-8')
                if message == 'NICK':
                    client.send(self.nickname.encode('utf-8'))
                elif message[:5] == 'LOAD:':
                    self.chatBoxTE.setTextColor(QColor(0, 0, 0))
                    self.chatBoxTE.append(message[5:len(message)])
                elif message[:5] == 'FILE:':
                    fileName = message[5:len(message)]
                    self.chatBoxTE.setTextColor(QColor(0, 255, 255))
                    currentTime = datetime.datetime.now()
                    self.time = currentTime.strftime("%H:%M:%S")
                    self.chatBoxTE.append(self.time + ": Receiving file: " + fileName)
                    with codecs.open(BASE_DIR + "/Client/Receives/" + fileName, "wb") as file:
                        while True:
                            fileData = client.recv(4096)
                            file.write(fileData)
                            if len(fileData) < 4096: 
                                break
                        self.chatBoxTE.setTextColor(QColor(0, 255, 255))
                        currentTime = datetime.datetime.now()
                        self.time = currentTime.strftime("%H:%M:%S")
                        self.chatBoxTE.append(self.time + ": " + "File saving completed!")
                        if (self.notificationState == True):
                            self.notifyMessage("File saving completed: " + fileName)
                else:
                    if message == "":
                        self.chatBoxTE.setTextColor(QColor(80, 0, 255))
                        self.chatBoxTE.append(self.time + ": " + "An error occured!")
                        break
                    self.chatBoxTE.setTextColor(QColor(80, 0, 255))
                    self.chatBoxTE.append(self.time + ": " + message)
                    if (self.notificationState == True):
                        self.notifyMessage(message)
        except:
            self.chatBoxTE.setTextColor(QColor(80, 0, 255))
            self.chatBoxTE.append(self.time + ": " + "An error occured!")
            self.threat = True
        finally:
            client.close()

    def showMessage(self):
        if self.threat == False:
            if self.messageLE.text() != "":
                currentTime = datetime.datetime.now()
                self.time = currentTime.strftime("%H:%M:%S")
                message = self.nickname + ": " + self.messageLE.text()
                self.chatBoxTE.setTextColor(QColor(0, 0, 0))
                self.chatBoxTE.append(self.time + ": " + "You: " + self.messageLE.text())
                self.messageLE.clear()
                client.send(message.encode('utf-8'))

    def runClient(self):
        try:
            client.connect((self.ip, self.port))
            self.runnable = True
            self.receive()
            client.close()
        except:
            self.chatBoxTE.setTextColor(QColor(255, 0, 0))
            self.chatBoxTE.append("Server is not online! Please close this program and try again!")
            self.threat = True

    def setupUi(self, ClientWD, nickname, ip, port):
        self.threat = False
        self.nickname = nickname
        self.ip = ip
        self.port = port

        self.notificationState = False
        self.runnable = False

        ClientWD.setObjectName("ClientWD")
        ClientWD.resize(350, 450)
        ClientWD.setMinimumSize(QtCore.QSize(350, 450))
        ClientWD.setMaximumSize(QtCore.QSize(350, 450))
        self.centralwidget = QtWidgets.QWidget(ClientWD)
        self.centralwidget.setObjectName("centralwidget")

        self.dateLB = QtWidgets.QLabel(self.centralwidget)
        self.dateLB.setGeometry(QtCore.QRect(10, 10, 75, 13))
        self.dateLB.setStyleSheet(stylesheet)
        self.dateLB.setObjectName("dateLB")

        self.timeLB = QtWidgets.QLabel(self.centralwidget)
        self.timeLB.setGeometry(QtCore.QRect(290, 10, 65, 13))
        self.timeLB.setStyleSheet(stylesheet)
        self.timeLB.setObjectName("timeLB")

        self.messageLE = QtWidgets.QLineEdit(self.centralwidget)
        self.messageLE.setGeometry(QtCore.QRect(10, 387, 271, 41))
        self.messageLE.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignCenter)
        self.messageLE.setObjectName("messageLE")

        self.chatBoxTE = QtWidgets.QTextEdit(self.centralwidget)
        self.chatBoxTE.setGeometry(QtCore.QRect(10, 30, 331, 302))
        self.chatBoxTE.setReadOnly(True)
        self.chatBoxTE.setObjectName("chatBoxTE")

        self.sendBT = QtWidgets.QPushButton(self.centralwidget)
        self.sendBT.setGeometry(QtCore.QRect(290, 386, 51, 43))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sendBT.setFont(font)
        self.sendBT.setAutoDefault(True)
        self.sendBT.setDefault(True)
        self.sendBT.setFlat(False)
        self.sendBT.setObjectName("sendBT")
        self.sendBT.setStyleSheet(stylesheet)
        self.sendBT.setToolTip('Send message')

        self.sendFileBT = QtWidgets.QPushButton(self.centralwidget)
        self.sendFileBT.setGeometry(QtCore.QRect(10, 342, 35, 35))
        self.sendFileBT.setObjectName("sendFileBT")
        self.sendFileBT.setStyleSheet(stylesheet1)
        self.sendFileBT.setToolTip('Send file')

        self.notificationBT = QtWidgets.QPushButton(self.centralwidget)
        self.notificationBT.setGeometry(QtCore.QRect(55, 342, 35, 35))
        self.notificationBT.setObjectName("notificationBT")
        self.notificationBT.setStyleSheet(stylesheet2)
        self.notificationBT.setToolTip('Turn on notification')

        ClientWD.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(ClientWD)
        self.statusbar.setObjectName("statusbar")
        ClientWD.setStatusBar(self.statusbar)

        #Tự động
        self.datetimeThread = threading.Thread(target = self.setCurrentTime)
        self.datetimeThread.start()
        clientThread = threading.Thread(target = self.runClient)
        clientThread.start()
        
        #Chức năng
        self.sendBT.clicked.connect(self.showMessage)
        self.sendFileBT.clicked.connect(self.browseFile)
        self.notificationBT.clicked.connect(self.changeNotificationState)

        self.retranslateUi(ClientWD)
        QtCore.QMetaObject.connectSlotsByName(ClientWD)

    def retranslateUi(self, ClientWD):
        _translate = QtCore.QCoreApplication.translate
        ClientWD.setWindowTitle(_translate("ClientWD", "Cloud Chat - " + self.nickname))
        self.dateLB.setText(_translate("ClientWD", "TextLabel"))
        self.timeLB.setText(_translate("ClientWD", "TextLabel"))
        self.sendBT.setShortcut(_translate("ClientWD", "Enter"))

stylesheet = """
    QLabel {
        font: bold 10px;
        color: #ffffff;
    }

    QPushButton {
        background-image: url(Images/paper_plane.png);
        background-repeat: no-repeat;
        background-position: center;
    }
"""

stylesheet1 = """
    QPushButton {
        background-image: url(Images/attach.png);
        background-repeat: no-repeat;
        background-position: center;
    }
"""

stylesheet2 = """
    QPushButton {
        background-image: url(Images/un_notification.png);
        background-repeat: no-repeat;
        background-position: center;
    }
"""

stylesheet3 = """
    QPushButton {
        background-image: url(Images/notification.png);
        background-repeat: no-repeat;
        background-position: center;
    }
"""

class ClientWindow(QtWidgets.QMainWindow):
    def closeEvent(self, event):
        client.close()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ClientWD = ClientWindow()
    ui = Ui_ClientWD()
    ui.setupUi(ClientWD, "Wind", "127.0.0.1", 55555)
    ClientWD.show()
    sys.exit(app.exec_())
    
