from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *
from qpoint3d import *
from random import *
import shapefile


class Input:
    def __init__(self):
        self.points = []
        self.scale = 0
        pass

    def loadFile(self, w, h):
        path = QFileDialog.getOpenFileName(None, "Select Shapefile", "", "SHP files (*.shp)")[0]

        # If nothing selected, end function
        if path == '':
            return self.points, self.scale

        # Open shapefile and load position and attributes
        with shapefile.Reader(path) as shp:
            features = shp.shapeRecords()

        # Min and max coords
        min_x = inf
        max_x = -inf
        min_y = inf
        max_y = -inf

        # Modify each points
        p_jtsk = []
        for p_shp in features:
            # Get point coordinates
            p_coords = p_shp.shape.points
            x = p_coords[0][0]
            y = p_coords[0][1]

            # Get height of current point
            z = float(p_shp.record[1])

            p = QPoint3D(x, y, z)
            p_jtsk.append(p)

            # get min and max x and y
            if x < min_x:
                min_x = x
            if y < min_y:
                min_y = y
            if x > max_x:
                max_x = x
            if y > max_y:
                max_y = y

        # Compute dimensions
        x_dim = max_x - min_x
        y_dim = max_y - min_y

        # Compute scale based on dominant side
        b = 50  # boundary
        window_size_x = w - b
        window_size_y = h - b

        if window_size_x / window_size_y < x_dim / y_dim:
            scale = window_size_x / x_dim
            # Descale dy
            y_d = window_size_y * (window_size_x / x_dim) / (window_size_y / y_dim)
        else:
            scale = window_size_y / y_dim
            y_d = window_size_y

        # Transform points
        for p in p_jtsk:
            x = ((p.x() - min_x) * scale) + b / 2
            y = (y_d - (p.y() - min_y) * scale) + b / 2
            z = p.getZ()
            transformed_p = QPoint3D(x, y, z)
            self.points.append(transformed_p)

        self.scale = scale

        return self.points, self.scale
