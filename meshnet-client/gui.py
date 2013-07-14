import sys
from PyQt4 import QtGui
from PyQt4 import uic
from admin import AdminInterface
    
class MainWindow(QtGui.QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        global admin
        admin = AdminInterface()
        self.initUI()
        
    def initUI(self):
        ui = uic.loadUi('mainwindow.ui', self)
        self.setWindowIcon(QtGui.QIcon('marylandmesh.png'))
        self.show()
        ui.actionAdd_Peer.triggered.connect(self.addPeer)
    
    def addPeer(self):
        peerWindow = AddPeerWindow()
        peerWindow.setModal(True)
        peerWindow.exec_()

class AddPeerWindow(QtGui.QDialog):
    
    ui = None
    
    def __init__(self):
        super(AddPeerWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowIcon(QtGui.QIcon('marylandmesh.png'))
        self.setWindowTitle('Add Peer')
        self.ui = uic.loadUi('addpeer.ui', self)
        self.ui.accepted.connect(self.addPeer)
        self.ui.plainTextEdit.setHidden(True)
        self.ui.jsonLabel.setHidden(True)
        
    def addPeer(self):
        name = str(self.ui.nameField.text())
        key = str(self.ui.keyField.text())
        pw = str(self.ui.passField.text())
        v4 = str(self.ui.v4Field.text())
        port = str(self.ui.portField.text())
        
        admin.addPeer(key, pw, v4, port)
        
    def addPeerFromJson(self):
        print 'stuff'
        
        

def main():
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('Meshnet Client')
    w = MainWindow()
    sys.exit(app.exec_())
        
if __name__ == '__main__':
    main()

