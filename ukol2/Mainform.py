from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from input import *
from algorithms import *


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(895, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MainForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.pushButton_3 = QtWidgets.QPushButton(MainForm)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(MainForm)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(MainForm)
        self.comboBox.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.PreventContextMenu)
        self.comboBox.setSizeAdjustPolicy(QtWidgets.QComboBox.SizeAdjustPolicy.AdjustToContents)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        self.label_2 = QtWidgets.QLabel(MainForm)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(MainForm)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout.addWidget(self.comboBox_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton = QtWidgets.QPushButton(MainForm)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton_2 = QtWidgets.QPushButton(MainForm)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MainForm)
        self.pushButton.clicked.connect(self.simplifyClick) # type: ignore
        self.pushButton_2.clicked.connect(self.clearClick) # type: ignore
        self.pushButton_3.clicked.connect(self.input) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "BuildingSimplify"))
        self.pushButton_3.setText(_translate("MainForm", "Input"))
        self.label.setText(_translate("MainForm", "Select method"))
        self.comboBox.setItemText(0, _translate("MainForm", "Minimum BR"))
        self.comboBox.setItemText(1, _translate("MainForm", "Wall Average"))
        self.comboBox.setItemText(2, _translate("MainForm", "Longest Edge"))
        self.label_2.setText(_translate("MainForm", "Select convex hull alg."))
        self.comboBox_2.setItemText(0, _translate("MainForm", "Jarvis Scan"))
        self.comboBox_2.setItemText(1, _translate("MainForm", "Graham Scan"))
        self.pushButton.setText(_translate("MainForm", "Simplify"))
        self.pushButton_2.setText(_translate("MainForm", "Clear"))

    def input(self):
        self.Canvas.er_list = []
        w = self.Canvas.frameGeometry().width()
        h = self.Canvas.frameGeometry().height()
        self.Canvas.setPolygon(Input().loadFile(w, h))

    def simplifyClick(self):
        self.Canvas.er_list = []
        buildings = self.Canvas.getPolygon()
        if self.comboBox.currentIndex() == 0:
            for b in buildings:
                er = MinimumAreaEnclosingRectangle().minAreaEnclosingRectangle(b, self.comboBox_2.currentIndex())
                self.Canvas.insertEnclosingRectangle(er)

        if self.comboBox.currentIndex() == 1:
            for b in buildings:
                er = WallAverage().computeWallAverage(b)
                self.Canvas.insertEnclosingRectangle(er)

        if self.comboBox.currentIndex() == 2:
            for b in buildings:
                er = LongestEdge().computeLongestEdge(b)
                self.Canvas.insertEnclosingRectangle(er)
        self.Canvas.repaint()

    def clearClick(self):
        self.Canvas.er_list = []
        self.Canvas.pol_list = []
        self.Canvas.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QWidget()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
