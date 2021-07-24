from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from ClientWD import Ui_ClientWD

class Ui_JoinDialog(object):
    def showError(self):
        msg = QMessageBox()
        msg.setWindowTitle("Error!")
        msg.setIcon(QMessageBox.Critical)
        msg.setText("IP or Port is invalid!")
        msg.setStandardButtons(QMessageBox.Ok)
        x = msg.exec_()

    def getNickname(self):
        return str(self.nicknameLE.text())

    def getIP(self):
        return str(self.ipLE.text())

    def getPort(self):
        try:
            return int(self.portLE.text())
        except:
            pass

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
        if self.portChecking() == True and self.IPChecking() == True:
            w = MyWindow(self.getNickname(), self.getIP(), self.getPort())
            w.show();
        else:
            self.showError()

    def setupUi(self, JoinDialog):
        JoinDialog.setObjectName("JoinDialog")
        JoinDialog.resize(300, 450)
        JoinDialog.setMinimumSize(QtCore.QSize(300, 450))
        JoinDialog.setMaximumSize(QtCore.QSize(300, 450))

        self.joinLB = QtWidgets.QLabel(JoinDialog)
        self.joinLB.setGeometry(QtCore.QRect(10, 10, 280, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.joinLB.setFont(font)
        self.joinLB.setObjectName("joinLB")
        self.joinLB.setStyleSheet(stylesheet1)
        self.joinLB.setAlignment(QtCore.Qt.AlignCenter)

        self.portLB = QtWidgets.QLabel(JoinDialog)
        self.portLB.setGeometry(QtCore.QRect(10, 290, 100, 30))
        self.portLB.setStyleSheet(stylesheet)
        self.portLB.setObjectName("portLB")
        self.portLB.setAlignment(QtCore.Qt.AlignCenter)

        self.nicknameLE = QtWidgets.QLineEdit(JoinDialog)
        self.nicknameLE.setGeometry(QtCore.QRect(10, 120, 281, 30))
        self.nicknameLE.setCursorPosition(0)
        self.nicknameLE.setObjectName("nicknameLE")

        self.ipLB = QtWidgets.QLabel(JoinDialog)
        self.ipLB.setGeometry(QtCore.QRect(10, 180, 100, 30))
        self.ipLB.setStyleSheet(stylesheet)
        self.ipLB.setObjectName("ipLB")
        self.ipLB.setAlignment(QtCore.Qt.AlignCenter)

        self.ipLE = QtWidgets.QLineEdit(JoinDialog)
        self.ipLE.setGeometry(QtCore.QRect(10, 230, 281, 30))
        self.ipLE.setCursorPosition(0)
        self.ipLE.setObjectName("ipLE")

        self.portLE = QtWidgets.QLineEdit(JoinDialog)
        self.portLE.setGeometry(QtCore.QRect(10, 340, 281, 30))
        self.portLE.setObjectName("portLE")

        self.nicknameLB = QtWidgets.QLabel(JoinDialog)
        self.nicknameLB.setGeometry(QtCore.QRect(10, 70, 100, 30))
        self.nicknameLB.setStyleSheet(stylesheet)
        self.nicknameLB.setObjectName("nicknameLB")
        self.nicknameLB.setAlignment(QtCore.Qt.AlignCenter)

        self.buttonBox = QtWidgets.QDialogButtonBox(JoinDialog)
        self.buttonBox.setGeometry(QtCore.QRect(130, 410, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        #Chức năng
        self.buttonBox.accepted.connect(self.buttonOKClicked)
        self.retranslateUi(JoinDialog)
        QtCore.QMetaObject.connectSlotsByName(JoinDialog)
        self.buttonBox.accepted.connect(JoinDialog.accept)
        self.buttonBox.rejected.connect(JoinDialog.reject)

    def retranslateUi(self, JoinDialog):
        _translate = QtCore.QCoreApplication.translate
        JoinDialog.setWindowTitle(_translate("JoinDialog", "Cloud Chat"))
        self.joinLB.setText(_translate("JoinDialog", "Join Server"))
        self.portLB.setText(_translate("JoinDialog", "Port server"))
        self.ipLB.setText(_translate("JoinDialog", "IP server"))
        self.nicknameLB.setText(_translate("JoinDialog", "Nickname"))

class MyWindow(QtWidgets.QMainWindow, Ui_ClientWD):
    def __init__(self, nickname, ip, port):
        super().__init__()
        self.setupUi(self, nickname, ip, port)

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
    JoinDialog = QtWidgets.QDialog()
    ui = Ui_JoinDialog()
    ui.setupUi(JoinDialog)
    JoinDialog.show()
    sys.exit(app.exec_())
