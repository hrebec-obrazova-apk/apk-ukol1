from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # List of Buildings
        self.pol_list = []

        # List of Enclosing Rectangles
        self.er_list = []

    def paintEvent(self, e: QPaintEvent):
        # Create new object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen and brush - building
        qp.setPen(Qt.GlobalColor.blue)
        qp.setBrush(Qt.GlobalColor.gray)

        # Draw building
        for building in self.pol_list:
            qp.drawPolygon(building)

        # Set pen and brush - enclosing rectangle
        qp.setPen(Qt.GlobalColor.red)
        qp.setBrush(Qt.GlobalColor.transparent)

        # Draw Enclosing rectangle
        for en_rec in self.er_list:
            qp.drawPolygon(en_rec)

        qp.end()

    # Building getter
    def getPolygon(self):
        return self.pol_list

    def setPolygon(self, buildings: list):
        self.pol_list = buildings

    # Enclosing Rectangle setter
    def insertEnclosingRectangle(self, er: QPolygon):
        self.er_list.append(er)
