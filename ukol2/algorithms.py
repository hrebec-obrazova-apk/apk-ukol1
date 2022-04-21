from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from math import *


class MinimumAreaEnclosingRectangle:
    def __init__(self):
        pass

    def get2LinesAngle(self, p1: QPoint, p2: QPoint, p3: QPoint, p4: QPoint):
        # Get angle between 2 vectors
        ux = p2.x() - p1.x()
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()

        # Cross product
        uv = ux * vx + uy * vy

        # Norms
        nu = (ux ** 2 + uy ** 2) ** 0.5
        nv = (vx ** 2 + vy ** 2) ** 0.5

        # Angle
        try:
            return abs(acos(uv / (nu * nv)))
        except:
            return 0

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

    def createCHJarvis(self, pol: QPolygon):
        # Create convex hull using Jarvis Scan
        ch = QPolygon()

        # Find pivot
        q = min(pol, key=lambda k: k.y())

        # Initialise Pj, Pj1
        pj = q
        pj1 = QPoint(q.x() - 10, q.y())

        # Appending pivot to convex hull
        ch.append(q)

        # Jarvis scan
        first_pass = True

        while pj != q or first_pass:
            first_pass = False

            # Find point maximizing omega
            omega_max = 0
            index_max = -1

            for index in range(len(pol)):
                # Compute omega angle
                omega = self.get2LinesAngle(pj, pj1, pj, pol[index])

                # Updating maximum
                if omega >= omega_max:
                    omega_max = omega
                    index_max = index

            # Add vertex to convex hull
            ch.append(pol[index_max])

            # Update last two points of ch
            pj1 = pj
            pj = pol[index_max]

        return ch

    def createCHDGraham(self, pol: QPolygon):
        # Create convex hull using Graham Scan

        # Find pivot
        q = min(pol, key=lambda k: k.y())

        # Initialize list of angels, distances and their indices
        omega_list = []
        index_list = []
        d_list = []

        # Initialise Pj, Pj1 to get x-axis
        pj = q
        pj1 = QPoint(q.x() + 10, q.y())

        # Compute all angles between line defined by q and pol[i] and x-axis
        for i in range(len(pol)):
            # skip q
            if pol[i] == q:
                continue

            # Compute angel
            omega_i = self.get2LinesAngle(pj, pj1, pj, pol[i])

            # Compute distance between q and pol[i]
            d_i = ((q.x() - pol[i].x()) ** 2 + (q.y() - pol[i].y()) ** 2) ** 0.5

            # Check if already exists angle with same value
            if omega_i in omega_list:

                # Get its position in list of angels
                idx = omega_list.index(omega_i)

                # If is new angle more distant delete old one and insert new
                if d_i > d_list[idx]:
                    omega_list.append(omega_i)
                    index_list.append(i)
                    d_list.append(d_i)
                    omega_list.pop(idx)
                    index_list.pop(idx)
                    d_list.pop(idx)

            # Add unique angel value
            else:
                omega_list.append(omega_i)
                index_list.append(i)
                d_list.append(d_i)

        # Sort point indices by their value of angel
        index_sort = [x for _, x in sorted(zip(omega_list, index_list))]

        # Get sorted list of points from original
        pol_sorted = []
        for idx in index_sort:
            pol_sorted.append(pol[idx])

        # initialize stack, starting index and number of points to evaluate
        S = []
        j = 1
        n = len(pol_sorted)

        # Add q and first point to stack
        S.append(q)
        S.append(pol_sorted[0])

        # Process all points
        while j < n:

            # Get position of current point and line defined by first 2 points in stack
            if self.getPointAndLinePosition(pol_sorted[j], S[-2], S[-1]) != 0:
                # Add current point to first position in stack if point is not in right halfplane
                S.append(pol_sorted[j])

                # Update current point
                j = j + 1
            # remove first point in stack
            else:
                S.pop()
        # Create convex hull
        ch = QPolygon(S)

        return ch

    def rotate(self, pol: QPolygon, angle: float):
        # Rotate polygon vertices by angle
        pol_rot = QPolygon()

        # Browse points one by one
        for i in range(len(pol)):
            # Apply rotation matrix
            xr = pol[i].x() * cos(angle) - sin(angle) * pol[i].y()
            yr = pol[i].x() * sin(angle) + cos(angle) * pol[i].y()

            # Add point to rotated polygon
            point = QPoint(int(xr), int(yr))
            pol_rot.append(point)

        return pol_rot

    def minMaxBox(self, pol: QPolygon):
        # Creating minmax box and calculating area
        # Finding extreme coordinates
        x_min = min(pol, key=lambda k: k.x()).x()
        x_max = max(pol, key=lambda k: k.x()).x()
        y_min = min(pol, key=lambda k: k.y()).y()
        y_max = max(pol, key=lambda k: k.y()).y()

        # Create vertices of bounding box
        v1 = QPoint(x_min, y_min)
        v2 = QPoint(x_max, y_min)
        v3 = QPoint(x_max, y_max)
        v4 = QPoint(x_min, y_max)

        # Area of rectangle
        a = x_max - x_min
        b = y_max - y_min
        S = a * b

        # Create QPolygon
        minmax_box = QPolygon([v1, v2, v3, v4])

        return S, minmax_box

    def minAreaEnclosingRectangle(self, pol: QPolygon, algorithm: int):
        # Create approximation of building using minimum area enclosing rectangle
        # Create convex hull with chosen algorithm

        if algorithm ==0:
            ch = self.createCHJarvis(pol)
        elif algorithm ==1:
            ch = self.createCHDGraham(pol)

        n_ch = len(ch)

        # Create initial approximation
        sigma_min = 0
        S_min, mmb_min = self.minMaxBox(ch)

        # Process all segments of convex hull
        for i in range(n_ch):
            dx = ch[(i + 1) % n_ch].x() - ch[i].x()
            dy = ch[(i + 1) % n_ch].y() - ch[i].y()

            # Direction of segment
            sigma_i = atan2(dy, dx)

            # Rotate by -sigma_i
            ch_rot = self.rotate(ch, -sigma_i)

            # Create MMB
            S_i, mmb_i = self.minMaxBox(ch_rot)

            # Updating minimum
            if S_i < S_min:
                S_min = S_i
                sigma_min = sigma_i
                mmb_min = mmb_i

        # Rotate mmb_min back by sigma_min
        er = self.rotate(mmb_min, sigma_min)

        # Resize mmb_res, S_mmb = S_building
        er_new = self.resizeRectangle(er, pol)

        return er_new

    def getArea(self, pol: QPolygon):
        # Calculating area of non-convex polygon using LH formula
        n = len(pol)
        S = 0

        for i in range(n):
            dS = pol[i].x() * (pol[(i + 1) % n].y() - pol[(i - 1 + n) % n].y())
            S += dS

        return 0.5 * abs(S)

    def resizeRectangle(self, er: QPolygon, pol: QPolygon):
        # Resize rectangle to S_er = S_pol
        # Calculate area of both polygons
        er_S = self.getArea(er)
        pol_S = self.getArea(pol)

        # Calculate fraction of areas
        k = pol_S / er_S

        # Calculate center of mess
        xc = (er[0].x() + er[1].x() + er[2].x() + er[3].x()) / 4
        yc = (er[0].y() + er[1].y() + er[2].y() + er[3].y()) / 4

        # Calculate directions
        u1x = er[0].x() - xc
        u1y = er[0].y() - yc

        u2x = er[1].x() - xc
        u2y = er[1].y() - yc

        u3x = er[2].x() - xc
        u3y = er[2].y() - yc

        u4x = er[3].x() - xc
        u4y = er[3].y() - yc

        # Calculate new nodes
        v1x = xc + sqrt(k) * u1x
        v2x = xc + sqrt(k) * u2x
        v3x = xc + sqrt(k) * u3x
        v4x = xc + sqrt(k) * u4x

        v1y = yc + sqrt(k) * u1y
        v2y = yc + sqrt(k) * u2y
        v3y = yc + sqrt(k) * u3y
        v4y = yc + sqrt(k) * u4y

        # Create QPoint objects
        v1 = QPoint(int(v1x), int(v1y))
        v2 = QPoint(int(v2x), int(v2y))
        v3 = QPoint(int(v3x), int(v3y))
        v4 = QPoint(int(v4x), int(v4y))

        # Create new polygon
        er_new = QPolygon([v1, v2, v3, v4])

        return er_new


class WallAverage:
    def __init__(self):
        pass

    def rotate(self, pol: QPolygon, angle: float):
        # Rotate polygon vertices by angle
        pol_rot = QPolygon()

        # Browse points one by one
        for i in range(len(pol)):
            # Apply rotation matrix
            xr = pol[i].x() * cos(angle) - sin(angle) * pol[i].y()
            yr = pol[i].x() * sin(angle) + cos(angle) * pol[i].y()

            # Add point to rotated polygon
            point = QPoint(int(xr), int(yr))
            pol_rot.append(point)

        return pol_rot

    def minMaxBox(self, pol: QPolygon):
        # Creating minmax box and calculating area
        # Finding extreme coordinates
        x_min = min(pol, key=lambda k: k.x()).x()
        x_max = max(pol, key=lambda k: k.x()).x()
        y_min = min(pol, key=lambda k: k.y()).y()
        y_max = max(pol, key=lambda k: k.y()).y()

        # Create vertices of bounding box
        v1 = QPoint(x_min, y_min)
        v2 = QPoint(x_max, y_min)
        v3 = QPoint(x_max, y_max)
        v4 = QPoint(x_min, y_max)

        # Create QPolygon
        minmax_box = QPolygon([v1, v2, v3, v4])

        return minmax_box

    def getArea(self, pol: QPolygon):
        # Calculating area of non-convex polygon using LH formula
        n = len(pol)
        S = 0

        for i in range(n):
            dS = pol[i].x() * (pol[(i + 1) % n].y() - pol[(i - 1 + n) % n].y())
            S += dS

        return 0.5 * abs(S)

    def resizeRectangle(self, er: QPolygon, pol: QPolygon):
        # Resize rectangle to S_er = S_pol
        # Calculate area of both polygons
        er_S = self.getArea(er)
        pol_S = self.getArea(pol)

        # Calculate fraction of areas
        k = pol_S / er_S

        # Calculate center of mess
        xc = (er[0].x() + er[1].x() + er[2].x() + er[3].x()) / 4
        yc = (er[0].y() + er[1].y() + er[2].y() + er[3].y()) / 4

        # Calculate directions
        u1x = er[0].x() - xc
        u1y = er[0].y() - yc

        u2x = er[1].x() - xc
        u2y = er[1].y() - yc

        u3x = er[2].x() - xc
        u3y = er[2].y() - yc

        u4x = er[3].x() - xc
        u4y = er[3].y() - yc

        # Calculate new nodes
        v1x = xc + sqrt(k) * u1x
        v2x = xc + sqrt(k) * u2x
        v3x = xc + sqrt(k) * u3x
        v4x = xc + sqrt(k) * u4x

        v1y = yc + sqrt(k) * u1y
        v2y = yc + sqrt(k) * u2y
        v3y = yc + sqrt(k) * u3y
        v4y = yc + sqrt(k) * u4y

        # Create QPoint objects
        v1 = QPoint(int(v1x), int(v1y))
        v2 = QPoint(int(v2x), int(v2y))
        v3 = QPoint(int(v3x), int(v3y))
        v4 = QPoint(int(v4x), int(v4y))

        # Create new polygon
        er_new = QPolygon([v1, v2, v3, v4])

        return er_new

    def computeWallAverage(self, pol: QPolygon):

        # Get sigma
        dx = pol[1 % len(pol)].x() - pol[0].x()
        dy = pol[1 % len(pol)].y() - pol[0].y()
        sigma = atan2(dy, dx)

        # Initialize sums
        sum_w = 0
        sum_r = 0

        # Compute sigma_i
        for i in range(len(pol)):
            dx = pol[(i + 1) % len(pol)].x() - pol[i].x()
            dy = pol[(i + 1) % len(pol)].y() - pol[i].y()

            # Direction of segment
            sigma_i = atan2(dy, dx)

            # Reduce sigma_i by sigma
            dsigma_i = sigma_i - sigma

            # Compute rounded fraction
            ki = round(2 * dsigma_i / pi)

            # Compute residue
            ri = dsigma_i - ki * pi / 2

            # Compute weight from edge norm
            wi = ((pol[(i + 1) % len(pol)].x() - pol[i].x()) ** 2 + (pol[(i + 1) % len(pol)].y() - pol[i].y()) ** 2) ** 0.5

            # Compute sum of weights from norms
            sum_w += wi

            # Compute sum of r scaled by weight
            sum_r += ri * wi

        # Compute building direction
        direction = sigma + sum_r / sum_w

        # Create min max box from polygon reduced by main direction
        pol_reduced = self.rotate(pol, -direction)
        mmb = self.minMaxBox(pol_reduced)

        # Rotate min-max box back
        mmb_rot = self.rotate(mmb, direction)

        # Resize mmb_res, S_mmb = S_building
        mmb_new = self.resizeRectangle(mmb_rot, pol)

        return mmb_new


class LongestEdge:
    def __init__(self):
        pass

    def getLongestEdgeDirection(self, pol: QPolygon):
        # Return direction of the longest edge in polygon
        e_max = -1
        start = QPoint()
        end = QPoint()

        for i in range(len(pol)):
            e = ((pol[(i + 1) % len(pol)].x() - pol[i].x()) ** 2 + (pol[(i + 1) % len(pol)].y() - pol[i].y()) ** 2) ** 0.5

            # Update minimum
            if e > e_max:
                e_max = e

                # Update edge defining point
                start = pol[i]
                end = pol[(i + 1) % len(pol)]

        # Compute direction of the longest edge
        dx = end.x() - start.x()
        dy = end.y() - start.y()
        sigma = atan2(dy, dx)

        return sigma

    def rotate(self, pol: QPolygon, angle: float):
        # Rotate polygon vertices by angle
        pol_rot = QPolygon()

        # Browse points one by one
        for i in range(len(pol)):
            # Apply rotation matrix
            xr = pol[i].x() * cos(angle) - sin(angle) * pol[i].y()
            yr = pol[i].x() * sin(angle) + cos(angle) * pol[i].y()

            # Add point to rotated polygon
            point = QPoint(int(xr), int(yr))
            pol_rot.append(point)

        return pol_rot

    def minMaxBox(self, pol: QPolygon):
        # Creating minmax box and calculating area
        # Finding extreme coordinates
        x_min = min(pol, key=lambda k: k.x()).x()
        x_max = max(pol, key=lambda k: k.x()).x()
        y_min = min(pol, key=lambda k: k.y()).y()
        y_max = max(pol, key=lambda k: k.y()).y()

        # Create vertices of bounding box
        v1 = QPoint(x_min, y_min)
        v2 = QPoint(x_max, y_min)
        v3 = QPoint(x_max, y_max)
        v4 = QPoint(x_min, y_max)

        # Create QPolygon
        minmax_box = QPolygon([v1, v2, v3, v4])

        return minmax_box

    def getArea(self, pol: QPolygon):
        # Calculating area of non-convex polygon using LH formula
        n = len(pol)
        S = 0

        for i in range(n):
            dS = pol[i].x() * (pol[(i + 1) % n].y() - pol[(i - 1 + n) % n].y())
            S += dS

        return 0.5 * abs(S)

    def resizeRectangle(self, er: QPolygon, pol: QPolygon):
        # Resize rectangle to S_er = S_pol
        # Calculate area of both polygons
        er_S = self.getArea(er)
        pol_S = self.getArea(pol)

        # Calculate fraction of areas
        k = pol_S / er_S

        # Calculate center of mess
        xc = (er[0].x() + er[1].x() + er[2].x() + er[3].x()) / 4
        yc = (er[0].y() + er[1].y() + er[2].y() + er[3].y()) / 4

        # Calculate directions
        u1x = er[0].x() - xc
        u1y = er[0].y() - yc

        u2x = er[1].x() - xc
        u2y = er[1].y() - yc

        u3x = er[2].x() - xc
        u3y = er[2].y() - yc

        u4x = er[3].x() - xc
        u4y = er[3].y() - yc

        # Calculate new nodes
        v1x = xc + sqrt(k) * u1x
        v2x = xc + sqrt(k) * u2x
        v3x = xc + sqrt(k) * u3x
        v4x = xc + sqrt(k) * u4x

        v1y = yc + sqrt(k) * u1y
        v2y = yc + sqrt(k) * u2y
        v3y = yc + sqrt(k) * u3y
        v4y = yc + sqrt(k) * u4y

        # Create QPoint objects
        v1 = QPoint(int(v1x), int(v1y))
        v2 = QPoint(int(v2x), int(v2y))
        v3 = QPoint(int(v3x), int(v3y))
        v4 = QPoint(int(v4x), int(v4y))

        # Create new polygon
        er_new = QPolygon([v1, v2, v3, v4])

        return er_new

    def computeLongestEdge(self, pol: QPolygon):
        # Approximate building with min max box in direction of the longest edge
        # Find main direction
        sigma = self.getLongestEdgeDirection(pol)

        # Reduce building by direction its longest edge
        pol_reduced = self.rotate(pol, -sigma)

        # get min-max box
        mmb = self.minMaxBox(pol_reduced)

        # Rotate min-max box back
        mmb_rot = self.rotate(mmb, sigma)

        # Resize mmb_res, S_mmb = S_building
        mmb_new = self.resizeRectangle(mmb_rot, pol)

        return mmb_new