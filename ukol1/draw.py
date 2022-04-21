from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *


class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = QPoint()
        self.polygons = []
        self.res = []

    def mousePressEvent(self, e: QMouseEvent):
        # Get cursor position
        x = int(e.position().x())
        y = int(e.position().y())

        # Create new point
        self.q.setX(x)
        self.q.setY(y)

        # Repaint screen
        self.repaint()

    def paintEvent(self, e: QPaintEvent):
        # Create new object
        qp = QPainter(self)

        # Draw polygons
        i = 0
        for pol in self.polygons:
            # Start draw
            qp.begin(self)

            if len(self.res) > 0 and self.res[i] == 1:
                # Set pen and brush - inside polygon
                qp.setPen(Qt.GlobalColor.green)
                qp.setBrush(Qt.GlobalColor.magenta)
            else:
                # Set pen and brush - outside polygon
                qp.setPen(Qt.GlobalColor.green)
                qp.setBrush(Qt.GlobalColor.darkCyan)

            qp.drawPolygon(pol)
            i += 1
            qp.end()

        # Start draw
        qp.begin(self)

        # Set pen and brush - point
        qp.setPen(Qt.GlobalColor.black)
        qp.setBrush(Qt.GlobalColor.darkRed)

        # Draw ellipse
        r = 3
        qp.drawEllipse(self.q.x() - r, self.q.y() - r, 2 * r, 2 * r)
        # End draw
        qp.end()

    def getQ(self):
        # Get q
        return self.q

    def getPolygons(self):
        # Get polygon
        return self.polygons