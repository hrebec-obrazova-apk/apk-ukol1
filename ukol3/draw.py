from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from random import *

from typing import List
from qpoint3d import *
from edge import *

class Draw (QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.points : List[QPoint3D] = []       #Input points
        self.dt : List[Edge] = []               #Delaunay edges
        self.cont_lines : List[Edge] = []       #Contour lines
        self.slope: List[float] = []            #Slope of triangles faces
        self.aspect: List[float] = []           #Orientation of triangle
        self.cont_lines_step: float = 0         #Step of contour lines

    def getPoints(self):
        return self.points

    def getDT(self):
        return self.dt

    def setPoints(self, points):
        self.points = points

    def setDT(self, dt):
        self.dt = dt

    def setCL(self, cont_lines):
        self.cont_lines = cont_lines

    def setSlope(self, slope):
        self.slope = slope

    def setAspect(self, aspect):
        self.aspect = aspect

    def setStep(self, step):
        self.cont_lines_step = step

    def paintEvent(self, e: QPaintEvent):
        # Create new object
        qp = QPainter(self)

        # Start draw
        qp.begin(self)

        # Set pen and brush - points
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.darkRed)

        # Draw points
        radius = 3
        for p in self.points:
            qp.drawEllipse(int(p.x()- radius), int(p.y()) - radius, 2 * radius, 2 * radius)

        #Draw Delaunay edges
        qp.setPen(Qt.GlobalColor.darkRed)
        for e in self.dt:
            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        # Draw contour lines
        for e in self.cont_lines:

            #Height of contour
            z = e.getStart().getZ()

            # Every fifth contour is bold
            if z % (self.cont_lines_step * 5) == 0:
                pen = QPen(Qt.GlobalColor.red)
                pen.setWidthF(3)
                qp.setPen(pen)
            else:
                pen = QPen(Qt.GlobalColor.black)
                pen.setWidthF(0.5)
                qp.setPen(pen)

            qp.drawLine(int(e.getStart().x()), int(e.getStart().y()), int(e.getEnd().x()), int(e.getEnd().y()))

        # Draw slope
        qp.setPen(Qt.GlobalColor.darkRed)

        for i in range(len(self.slope)):
            # Triangle vertices
            p1 = self.dt[i*3].getStart()
            p2 = self.dt[i*3 + 1].getStart()
            p3 = self.dt[i*3 + 2].getStart()
            p1Q = QPoint(int(p1.x()), int(p1.y()))
            p2Q = QPoint(int(p2.x()), int(p2.y()))
            p3Q = QPoint(int(p3.x()), int(p3.y()))
            pol = QPolygon([p1Q, p2Q, p3Q])

            if self.slope[i] < 0.5:
                qp.setBrush(QColor(0, 100, 0))  # dark green
                qp.drawPolygon(pol)

            elif self.slope[i] < 1.5:
                qp.setBrush(QColor(34, 139, 34))  # green
                qp.drawPolygon(pol)

            elif self.slope[i] < 3:
                qp.setBrush(QColor(50, 205, 50))  # Lime green
                qp.drawPolygon(pol)

            elif self.slope[i] < 6:
                qp.setBrush(QColor(73, 255, 47))  # Yellow-green
                qp.drawPolygon(pol)

            elif self.slope[i] < 15:
                qp.setBrush(QColor(255, 255, 0))  # yellow
                qp.drawPolygon(pol)

            elif self.slope[i] < 30:
                qp.setBrush(QColor(255, 215, 0))  # gold
                qp.drawPolygon(pol)

            elif self.slope[i] < 45:
                qp.setBrush(QColor(255, 140, 0))  # orange
                qp.drawPolygon(pol)

            else:
                qp.setBrush(QColor(255, 69, 0))  # orange-red
                qp.drawPolygon(pol)

        for i in range(len(self.aspect)):
            # Triangle vertices
            p1 = self.dt[i*3].getStart()
            p2 = self.dt[i*3 + 1].getStart()
            p3 = self.dt[i*3 + 2].getStart()
            p1Q = QPoint(int(p1.x()), int(p1.y()))
            p2Q = QPoint(int(p2.x()), int(p2.y()))
            p3Q = QPoint(int(p3.x()), int(p3.y()))
            pol = QPolygon([p1Q, p2Q, p3Q])

            # East
            if self.aspect[i] < 22.5 and self.aspect[i] > -22.5:
                qp.setBrush(Qt.GlobalColor.yellow)
                qp.drawPolygon(pol)

            # South-east
            elif self.aspect[i] > 22.5 and self.aspect[i] < 67.5:
                qp.setBrush(Qt.GlobalColor.green)
                qp.drawPolygon(pol)

            # South
            elif self.aspect[i] > 67.5  and self.aspect[i] < 112.5:
                qp.setBrush(QColor(64, 224, 208)) # light blue
                qp.drawPolygon(pol)

            # South-west
            elif self.aspect[i] > 112.5 and self.aspect[i] < 157.5:
                qp.setBrush(Qt.GlobalColor.blue)
                qp.drawPolygon(pol)

            # West
            elif self.aspect[i] > 157.5 and self.aspect[i] < 180 or self.aspect[i] > -180 and self.aspect[i] < -157.5:
                qp.setBrush(Qt.GlobalColor.darkBlue)
                qp.drawPolygon(pol)

            # north-west
            elif self.aspect[i] > -157.5 and self.aspect[i] < -112.5:
                qp.setBrush(Qt.GlobalColor.magenta)
                qp.drawPolygon(pol)

            # North
            elif self.aspect[i] > -112.5 and self.aspect[i] < -67.5:
                qp.setBrush(Qt.GlobalColor.red)
                qp.drawPolygon(pol)

            # north-east
            elif self.aspect[i] > -67.5 and self.aspect[i] < -22.5:
                qp.setBrush(QColor(255, 165, 0))  # Orange
                qp.drawPolygon(pol)

        # End draw
        qp.end()