#===============================================================================
#    Copyright 2013 Jonathan Frederickson
#
#     This file is part of meshnet-client.
# 
#     Meshnet-client is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     Meshnet-client is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with meshnet-client.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore
from PyQt4 import uic

class ErrorWindow(QtGui.QMessageBox):
    
    ui = None
    
    def __init__(self, parent, title, message):
        super(ErrorWindow, self).__init__(parent)
        self.setText(QtCore.QString(message))
        self.setWindowTitle(QtCore.QString(title))
        self.show()
        
        
        