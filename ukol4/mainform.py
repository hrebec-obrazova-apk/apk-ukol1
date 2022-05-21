from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import *
from booleanoperations import *
from input import *


class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1164, 645)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MainForm)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(MainForm)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.Canvas.sizePolicy().hasHeightForWidth())
        self.Canvas.setSizePolicy(sizePolicy)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(MainForm)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.pushButton = QtWidgets.QPushButton(MainForm)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_5 = QtWidgets.QPushButton(MainForm)
        self.pushButton_5.setObjectName("pushButton_5")
        self.verticalLayout.addWidget(self.pushButton_5)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.label = QtWidgets.QLabel(MainForm)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(MainForm)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.verticalLayout.addWidget(self.comboBox)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(MainForm)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.pushButton_3 = QtWidgets.QPushButton(MainForm)
        self.pushButton_3.setObjectName("pushButton_3")
        self.verticalLayout.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(MainForm)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MainForm)
        self.pushButton_2.clicked.connect(self.clickCreateOverlay) # type: ignore
        self.pushButton_3.clicked.connect(self.clickClear) # type: ignore
        self.pushButton_4.clicked.connect(self.clickClearAll) # type: ignore
        self.pushButton.clicked.connect(self.inputA) # type: ignore
        self.pushButton_5.clicked.connect(self.inputB) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainForm)

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Boolean Operations on Polygons"))
        self.label_2.setText(_translate("MainForm", "Input shapefile:"))
        self.pushButton.setText(_translate("MainForm", "Polygon A"))
        self.pushButton_5.setText(_translate("MainForm", "Polygon B"))
        self.label.setText(_translate("MainForm", "Boolean operation:"))
        self.comboBox.setItemText(0, _translate("MainForm", "Union"))
        self.comboBox.setItemText(1, _translate("MainForm", "Intersection"))
        self.comboBox.setItemText(2, _translate("MainForm", "Difference A-B"))
        self.comboBox.setItemText(3, _translate("MainForm", "Difference B-A"))
        self.pushButton_2.setText(_translate("MainForm", "Create overlay"))
        self.pushButton_3.setText(_translate("MainForm", "Clear"))
        self.pushButton_4.setText(_translate("MainForm", "Clear All"))

    def inputA(self):
        self.Canvas.setA(Input().loadFile())
        self.Canvas.repaint()

    def inputB(self):

        self.Canvas.setB(Input().loadFile())
        self.Canvas.repaint()

    def clickCreateOverlay(self):
        #Create overlay
        # Get Polygons
        polA, polB = self.Canvas.getPolygons()

        # Get type of Boolean operation
        idx_BO = self.comboBox.currentIndex()
        BO = BooleanOperation(idx_BO)

        # Create overlay
        a = Algorithms()
        edges = a.createOverlay(polA, polB, BO)

        # Draw result
        self.Canvas.setResults(edges)

        self.Canvas.repaint()

    def clickClear(self):
        self.Canvas.clearResults()
        self.Canvas.repaint()

    def clickClearAll(self):
        self.Canvas.clearCanvas()
        self.Canvas.repaint()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QWidget()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())
