import pickle
import sys
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication, QLabel,
    QComboBox, QTextEdit, QLineEdit)
from PyQt5.QtCore import Qt


class ScoreDB(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.dbfilename = 'assignment6.dat'
        self.scoredb = []
        self.readScoreDB()
        self.showScoreDB()

    def initUI(self):
        NameLabel = QLabel("Name:", self)
        self.NameEdit = QLineEdit(self)
        AgeLabel = QLabel("Age:", self)
        self.AgeEdit = QLineEdit(self)
        ScoreLabel = QLabel("Score:", self)
        self.ScoreEdit = QLineEdit(self)
        inputHbox = QHBoxLayout()
        inputHbox.addStretch(1)
        inputHbox.addWidget(NameLabel)
        inputHbox.addWidget(self.NameEdit)
        inputHbox.addWidget(AgeLabel)
        inputHbox.addWidget(self.AgeEdit)
        inputHbox.addWidget(ScoreLabel)
        inputHbox.addWidget(self.ScoreEdit)
        AmountLabel = QLabel("Amount:", self)
        self.AmountEdit = QLineEdit(self)
        showLabel = QLabel("Key:", self)
        self.showKeyCombo = QComboBox(self)
        self.showKeyCombo.addItem("Name")
        self.showKeyCombo.addItem("Age")
        self.showKeyCombo.addItem("Score")
        input2Hbox = QHBoxLayout()
        input2Hbox.addStretch(1)
        input2Hbox.addWidget(AmountLabel)
        input2Hbox.addWidget(self.AmountEdit)
        input2Hbox.addWidget(showLabel)
        input2Hbox.addWidget(self.showKeyCombo)
        addButton = QPushButton("Add")
        addButton.clicked.connect(self.addClicked)

        delButton = QPushButton("Del")
        delButton.clicked.connect(self.delClicked)

        findButton = QPushButton("Find")
        findButton.clicked.connect(self.findClicked)

        incButton = QPushButton("Inc")
        incButton.clicked.connect(self.incClicked)

        showButton = QPushButton("show")
        showButton.clicked.connect(self.showClicked)

        commandHbox = QHBoxLayout()

        commandHbox.addStretch(2)
        commandHbox.addWidget(addButton)
        commandHbox.addWidget(delButton)
        commandHbox.addWidget(findButton)
        commandHbox.addWidget(incButton)
        commandHbox.addWidget(showButton)

        resultLabel = QLabel("Result:", self)
        self.resultEdit = QTextEdit()
        vbox = QVBoxLayout()
        vbox.addStretch(10)
        vbox.addLayout(inputHbox)
        vbox.addLayout(input2Hbox)
        vbox.addLayout(commandHbox)
        vbox.addWidget(resultLabel)
        vbox.addWidget(self.resultEdit)
        self.setLayout(vbox)

        self.setGeometry(300, 300, 500, 250)
        self.setWindowTitle('Assignment6')
        self.show()

    def addClicked(self):
        sender = self.sender()

        name = self.NameEdit.text()
        age = int(self.AgeEdit.text())
        score = int(self.ScoreEdit.text())

        record = {'Name':name, 'Age':age, 'Score':score}
        self.scoredb += [record]
        self.showScoreDB()

    def delClicked(self):
        sender = self.sender()
        delKey = self.NameEdit.text()

        self.scoredb[:] = [x for x in self.scoredb
                           if x['Name'] != delKey]
        self.showScoreDB()

    def findClicked(self):

        sender = self.sender()
        findKey = self.NameEdit.text()

        self.findScoreDB(findKey)

    def incClicked(self):

        sender = self.sender()
        incKey = self.NameEdit.text()

        amo = self.AmountEdit.text()
        Amount = int(self.AmountEdit.text()) if amo else 0

        self.incScoreDB(incKey, Amount)
        self.showScoreDB()

    def showClicked(self):

        sender = self.sender()
        self.showScoreDB()

    def showScoreDB(self):

        keyname = str(self.showKeyCombo.currentText())
        msg = ""
        keyname = "Name" if not keyname else keyname

        for p in sorted(self.scoredb,
                        key=lambda  person: person[keyname]):
            for attr in sorted(p):
                msg += attr + "=" + str(p[attr]) + "     \t"
            msg += "\n"

        self.resultEdit.setText(msg)

    def findScoreDB(self, keyname):

        msg = ""
        for p in self.scoredb:
            if p['Name'] != keyname: continue
            for attr in sorted(p):
                msg += attr + "=" + str(p[attr]) + "    \t"
            msg += "\n"

        self.resultEdit.setText(msg)

    def incScoreDB(self, name, amount):

        for p in self.scoredb:
            if p['Name'] != name: continue
            p['Score'] += amount


    def closeEvent(self, event):
        self.writeScoreDB()

    def readScoreDB(self):
        try:
            fH = open(self.dbfilename, 'rb')
        except FileNotFoundError as e:
            self.scoredb = []
            return

        try:
            self.scoredb =  pickle.load(fH)
        except:
            pass
        else:
            pass
        fH.close()


    # write the data into person db
    def writeScoreDB(self):
        fH = open(self.dbfilename, 'wb')
        pickle.dump(self.scoredb, fH)
        fH.close()

    def showScoreDB(self):
        pass


if __name__ == '__main__':    
    app = QApplication(sys.argv)
    ex = ScoreDB()
    sys.exit(app.exec_())

