
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpointfb import *

from typing import List

class Input:
    def __init__(self):
        self.polygon: List[QPointFB] = []


    def loadFile(self):
        path = QFileDialog.getOpenFileName(None, "Select input textfile", "", "TXT files (*.txt)")[0]

        # If nothing selected, end function
        if path == '':
            return self.polygon

        # Open txt file
        with open(path, 'r') as file:

            for row in file:
                x_str, y_str = row.strip().split()
                x, y = float(x_str), float(y_str)
                vertex = QPointFB(x, y)
                self.polygon.append(vertex)

        return self.polygon