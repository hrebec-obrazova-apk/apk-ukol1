from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *


# Winding number algorithm
class Winding_num:
    def __init__(self):
        pass

    def getPointAndLinePosition(self, a: QPoint, p1: QPoint, p2: QPoint):
        # Analyze position point and line
        eps = 1.0e-10

        # Coordinate differences
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = a.x() - p1.x()
        vy = a.y() - p1.y()

        # Calculating determinant
        t = ux * vy - vx * uy

        # Point in left halfplane
        if t > eps:
            return 1

        # Point in right halfplane
        if t < -eps:
            return 0

        # Collinear point
        return -1

    def get2LinesAngle(self, p1: QPoint, p2: QPoint, p3: QPoint, p4: QPoint):
        # Get angle between 2 vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Dot product
        uv = ux * vx + uy * vy

        # Norms
        nu = (ux ** 2 + uy ** 2) ** 0.5
        nv = (vx ** 2 + vy ** 2) ** 0.5

        # Angle
        # Point is on a vertex (one norm is zero)
        if nu * nv == 0:
            return 0
        # Removing rounding problem
        angle = (uv / (nu * nv))
        if angle > 1:
            angle = 1
        return abs(acos(angle))

    def getPositionPointAndPolygon(self, q: QPoint, pol: QPolygon) -> int:
        # Analyzes position of the point and polygon
        n = len(pol)
        omega_sum = 0

        # Loop through polygon nodes
        for i in range(n):

            # Analyze position of q and pi, pi+1
            pos = self.getPointAndLinePosition(q, pol[i], pol[(i + 1) % n])

            # Angle between q and pi, pi+1
            omega = self.get2LinesAngle(q, pol[i], q, pol[(i + 1) % n])

            # Computing winding number
            if pos == 1:
                # Point in the left halfplane
                omega_sum += omega
            elif pos == 0:
                # Point in the right halfplane
                omega_sum -= omega

            else:
                # Point is collinear
                x_check = (q.x() - pol[i].x()) * (q.x() - pol[(i + 1) % n].x())
                y_check = (q.y() - pol[i].y()) * (q.y() - pol[(i + 1) % n].y())

                if x_check <= 0 and y_check <= 0:
                    return 1

        # Point q inside polygon
        epsilon = 1.0e-10

        if abs(abs(omega_sum) - 2 * pi) < epsilon:
            return 1

        # Point q outside polygon
        return 0


# Ray crossing algorithm
class Ray_cross:
    def __init__(self):
        pass

    def setLocalCoordinates(self, p: QPoint, q: QPoint):
        p_shifted = QPoint()

        # get shift of coordinate system
        dx = q.x()
        dy = q.y()

        # Compute local coordinates of point P
        x = p.x() - dx
        y = p.y() - dy

        # Point with new coordinates
        p_shifted.setX(x)
        p_shifted.setY(y)

        return p_shifted

    def getCrossingStatusU(self, p1: QPoint, p2: QPoint):
        # Analyze P1-P2 line crossing with Q-ray in the upper halfplane
        if (p1.y() > 0) != (p2.y() > 0):
            return True
        return False

    def getCrossingStatusL(self, p1: QPoint, p2: QPoint):
        # Analyze P1-P2 line crossing with Q-ray in the lower halfplane
        if (p1.y() < 0) != (p2.y() < 0):
            return True
        return False

    def getPositionPointAndPolygon(self,  q: QPoint, pol: QPolygon):
        # Get number of crossing between Q-ray and edges of polygon
        k_r = 0
        k_l = 0
        n = len(pol)

        # Change coordinates of points to local coordinates
        for i in range(n):
            p1 = self.setLocalCoordinates(pol[(i + 1) % n], q)  # p[i]
            p2 = self.setLocalCoordinates(pol[i], q)  # p[i-1]

            # Point on vertex
            epsilon = 1.0e-10
            if abs(0 - p1.x()) < epsilon and abs(0 - p1.y()) < epsilon:
                return 1

            # Get number of crossings of the right Q-rey
            if self.getCrossingStatusU(p1, p2):
                # Get crossing
                x_m = (p1.x() * p2.y() - p2.x() * p1.y()) / (p1.y() - p2.y())

                # Sum of crossings
                if x_m > 0:
                    k_r += 1

            # Get number of crossings of the left Q-rey
            if self.getCrossingStatusL(p1, p2):
                # Get crossing
                x_m = (p1.x() * p2.y() - p2.x() * p1.y()) / (p1.y() - p2.y())

                # Sum of crossings
                if x_m < 0:
                    k_l += 1

        # Point on the edge of polygon
        if k_l % 2 != k_r % 2:
            return 1

        # Point inside of polygon
        elif k_r % 2 == 1:
            return 1

        # Point outside of polygon
        else:
            return 0