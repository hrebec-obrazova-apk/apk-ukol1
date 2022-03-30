from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
import shapefile


class Input():
    def __init__(self):
        self.polygons = []
        pass

    def loadFile(self, w, h):
        path = QFileDialog.getOpenFileName(None, "Select Shapefile", "", "SHP files (*.shp)")[0]

        # If nothing selected, end function
        if path == '':
            return self.polygons

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
                new_point.setX(int((point.x() - min_x) * scale))
                new_point.setY(int(y_d - (point.y() - min_y) * scale))
                transformed_pol.append(new_point)
            self.polygons.append(transformed_pol)

        return self.polygons
