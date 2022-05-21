from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from edge import *
from typing import List
from qpointfb import *

class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.polA : List[QPointFB] = []
        self.polB : List[QPointFB] = []
        self.res : List[Edge] = []

    def paintEvent(self, e: QPaintEvent):

        # Create graphic object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen
        pen = QPen()
        pen.setColor(Qt.GlobalColor.darkGreen)
        pen.setWidth(2)
        qp.setPen(pen)

        #Draw polygon A
        q_polA = QPolygonF()
        for p in self.polA:
            q_polA.append(p)
        qp.drawPolygon(q_polA)

        pen.setColor(Qt.GlobalColor.darkBlue)
        pen.setWidth(2)
        qp.setPen(pen)

        #Draw polygon B
        q_polB = QPolygonF()
        for p in self.polB:
            q_polB.append(p)
        qp.drawPolygon(q_polB)

        # Draw results
        pen.setColor(Qt.GlobalColor.red)
        pen.setWidth(3)
        qp.setPen(pen)

        for e in self.res:
            qp.drawLine(e.getStart(), e.getEnd())

        # End draw
        qp.end()

    def getPolygons(self):
        return self.polA, self.polB

    def setA(self, pol):
        self.polA = pol

    def setB(self, pol):
        self.polB = pol

    def setResults(self, edges):
        self.res = edges

    def clearResults(self):
        self.res.clear()

    def clearCanvas(self):
        self.polA.clear()
        self.polB.clear()
        self.res.clear()


