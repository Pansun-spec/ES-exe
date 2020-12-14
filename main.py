# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setGeometry(100, 200, 623, 300)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(10, -20, 600, 311))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(25, 40, 81, 18))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(455, 40, 150, 18))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(230, 35, 88, 27))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_2.setGeometry(QtCore.QRect(475, 190, 110, 27))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.btn2_click)
        self.pushButton_3 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_3.setGeometry(QtCore.QRect(475, 240, 110, 27))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.pushButton_4 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton_4.setGeometry(475, 140, 110, 27)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.topological)
        self.textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit.setGeometry(QtCore.QRect(20, 80, 80, 211))
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.groupBox)
        self.textEdit_2.setGeometry(QtCore.QRect(110, 80, 331, 211))
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setReadOnly(True)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.move(460, 90)
        self.lineEdit.setReadOnly(True)
        self.pushButton.clicked.connect(self.go)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def btn2_click(self):
        if self.pushButton_2.text() != "input":
            self.pushButton_2.setText("input")
        else:
            self.pushButton_2.setText("Modify the БЗ")

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "ЕС-Типы темперамента человека"))
        self.label.setText(_translate("Form", "Enter facts"))
        self.label_2.setText(_translate("Form", "Show inference results"))
        self.pushButton.setText(_translate("Form", "Reason"))
        self.pushButton_2.setText(_translate("Form", "Modify the БЗ"))
        self.pushButton_3.setText(_translate("Form", "Exit"))
        self.pushButton_4.setText(_translate("From", "Organize the БЗ"))


    def topological(self):
        Q = []
        P = []
        ans = ""
        for line in open('RD.txt'):
            line = line.strip('\n')
            if line == '':
                continue
            line = line.split(' ')
            Q.append(line[line.__len__() - 1])
            del (line[line.__len__() - 1])
            P.append(line)


        inn = []
        for i in P:
            sum = 0
            for x in i:
                if Q.count(x) > 0:
                    sum += Q.count(x)
            inn.append(sum)

        while (1):
            x = 0
            if inn.count(-1) == inn.__len__():
                break
            for i in inn:
                if i == 0:
                    str = ' '.join(P[x])
                    # print("%s %s" %(str, Q[x]))
                    ans = ans + str + " " + Q[x] + "\n"
                    # print("%s -- %s" %(P[x],Q[x]))
                    inn[x] = -1
                    y = 0
                    for j in P:
                        if j.count(Q[x]) == 1:
                            inn[y] -= 1
                        y += 1
                x += 1
        print(ans)


        fw = open('RD.txt', 'w', buffering=1)
        fw.write(ans)
        fw.flush()
        fw.close()

    # 进行推理
    def go(self, flag=True):
        self.Q = []
        self.P = []
        fo = open('RD.txt', 'r', encoding='utf-8-sig')
        for line in fo:
            line = line.strip('\n')
            if line == '':
                continue
            line = line.split(' ')
            self.Q.append(line[line.__len__() - 1])
            del (line[line.__len__() - 1])
            self.P.append(line)
        fo.close()
        print("press the go button")
        self.lines = self.textEdit.toPlainText()
        self.lines = self.lines.split('\n')
        self.DB = set(self.lines)
        print(self.DB)
        self.str = ""
        print(self.str)
        flag = True
        temp = ""
        for x in self.P:
            if ListInSet(x, self.DB):
                self.DB.add(self.Q[self.P.index(x)])
                temp = self.Q[self.P.index(x)]
                flag = False
                # print("%s --> %s" %(x, self.Q[self.P.index(x)]))
                self.str += "%s --> %s\n" % (x, self.Q[self.P.index(x)])

        if flag:
            print("can not reason a single conclusion")
            for x in self.P:  
                if ListOneInSet(x, self.DB):
                    flag1 = False
                    for i in x:
                        if i not in self.DB:
                            btn = s.quest("is it " + i)
                            if btn == QtWidgets.QMessageBox.Ok:
                                self.textEdit.setText(self.textEdit.toPlainText() + "\n" + i)  # 确定则增加到textEdit
                                self.DB.add(i)
                                flag1 = True
                                # self.go(self)
                    if flag1:
                        self.go()
                        return

        self.textEdit_2.setPlainText(self.str)
        print("----------------------")
        print(self.str)
        if flag:
            btn = s.alert("can not reason")
            # if btn == QtWidgets.QMessageBox.Ok:  # 点击确定
            #     self.textEdit.setText(self.textEdit.toPlainText() + "\n确定")
        else:
            self.lineEdit.setText(temp)



def ListOneInSet(li, se):
    for i in li:
        if i in se:
            return True
    return False



def ListInSet(li, se):
    for i in li:
        if i not in se:
            return False
    return True


class SecondWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.setWindowTitle("Modify the БЗ")
        self.setGeometry(725, 200, 300, 300)
        self.textEdit = QtWidgets.QTextEdit(self)
        self.textEdit.setGeometry(8, 2, 284, 286)



    def alert(self, info):
        QtWidgets.QMessageBox.move(self, 200, 200)
        QtWidgets.QMessageBox.information(self, "Information", self.tr(info))


    def quest(self, info):

        QtWidgets.QMessageBox.move(self, 200, 200)
        button = QtWidgets.QMessageBox.question(self, "Question",
                                                self.tr(info),
                                                QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel,
                                                QtWidgets.QMessageBox.Cancel)
        return button

    def handle_click(self):
        if not self.isVisible():

            str = ""
            fo = open('RD.txt', 'r', encoding='utf-8-sig')
            for line in fo:
                line = line.strip('\n')
                if line == '':
                    continue
                str = str + line + "\n"
            fo.close()
            self.textEdit.setText(str)
            self.show()
        else:

            self.str = self.textEdit.toPlainText()
            print(self.str)


            self.fw = open('RD.txt', 'w')
            self.fw.write(self.str)
            self.fw.close()
            self.close()

    def handle_close(self):
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    s = SecondWindow()
    ui.pushButton_2.clicked.connect(s.handle_click)
    sys.exit(app.exec_())


