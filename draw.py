from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import inf
import shapefile


class Draw(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.q = QPoint()
        self.polygons = []
        self.res = []
        self.algorithm = True

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

    def loadPolygons(self, w, h):
        # Clear polygons
        self.polygons = []
        # Select path
        path = QFileDialog.getOpenFileName(None, "Select Shapefile", "", "SHP files (*.shp)")[0]

        # If nothing selected, end function
        if path == '':
            return

        # Open shapefile
        with shapefile.Reader(path) as shp:
            features = shp.shapes()

        # Min and max coords
        min_x = inf
        max_x = -inf
        min_y = inf
        max_y = -inf

        # Modify each polygon
        polygons_jtsk = []
        for pol_shp in features:
            # Get polygon coordinates
            pol = QPolygon()
            pol_coords = pol_shp.points

            # Save vertexes as QPoint
            for vertex in pol_coords[:-1]:
                # Add point to polygon
                q_point = QPoint()
                x = int(vertex[0])
                y = int(vertex[1])
                q_point.setX(x)
                q_point.setY(y)
                pol.append(q_point)

                # Find min and max
                if x < min_x:
                    min_x = x
                if y < min_y:
                    min_y = y
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y

            # Add polygons into list as QPolygons
            polygons_jtsk.append(pol)

        # Compute dimensions
        x_dim = max_x - min_x
        y_dim = max_y - min_y

        # Compute scale based on dominant side
        window_size_x = w
        window_size_y = h

        if window_size_x / window_size_y < x_dim / y_dim:
            scale = window_size_x / x_dim
            # Descale dy
            y_d = window_size_y * (window_size_x / x_dim) / (window_size_y / y_dim)
        else:
            scale = window_size_y / y_dim
            y_d = window_size_y

        # Transform polygons
        for pol in polygons_jtsk:
            transformed_pol = QPolygon()
            for point in pol:
                new_point = QPoint()
                new_point.setX((point.x() - min_x) * scale // 1)
                new_point.setY(y_d - (point.y() - min_y) * scale // 1)
                transformed_pol.append(new_point)
            self.polygons.append(transformed_pol)

        # Repaint screen
        self.repaint()

    def getQ(self):
        # Get q
        return self.q

    def getPolygons(self):
        # Get polygon
        return self.polygons

    def switchAlgorithm(self):
        # Switch between algorithms
        self.algorithm = not self.algorithm
