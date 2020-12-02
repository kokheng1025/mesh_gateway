import os
import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import * 
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *

from application import style
from application.uart_device_dialog import UartDeviceDialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mesh Gateway")
        self.setWindowIcon(QIcon("././icons/app.png"))
        self.setGeometry(450, 150, 1350, 750)
        self.setFixedSize(self.size())

        self.UI()
        self.show()
    
    def UI(self):       
        self.set_toolbar()
        self.set_statusbar()
        self.uart_ui = UartDeviceDialog()


    def set_toolbar(self):
        self.tb = self.addToolBar("Tool Bar")
        self.tb.setToolButtonStyle(Qt.ToolButtonTextUnderIcon)
        self.configure_uart = QAction(QIcon("././icons/uart.png"), "UART", self)
        self.tb.addAction(self.configure_uart)
        self.configure_uart.triggered.connect(self.configure_uart_device)
        self.tb.addSeparator()
        self.configure_mesh_key = QAction(QIcon("././icons/mesh_key.png"), "Key", self)
        self.tb.addAction(self.configure_mesh_key)
        #self.configure_mesh_key.triggered.connect(self.configure_mesh_key)
        self.tb.addSeparator()
        self.configure_provision = QAction(QIcon("././icons/provision.png"), "Provision", self)
        self.tb.addAction(self.configure_provision)
        #self.configure_provision.triggered.connect(self.configure_provision)
        self.tb.addSeparator()
        self.delete_node = QAction(QIcon("././icons/delete_node.png"), "Delete", self)
        self.tb.addAction(self.delete_node)
        #self.delete_node.triggered.connect(self.delete_node)
        self.tb.addSeparator()
        self.mesh_message = QAction(QIcon("././icons/message.png"), "Message", self)
        self.tb.addAction(self.mesh_message)
        #self.mesh_message.triggered.connect(self.send_mesh_message)
        self.tb.addSeparator()
        self.add_groups = QAction(QIcon("././icons/groups.png"), "Groups", self)
        self.tb.addAction(self.add_groups)
        #self.add_groups.triggered.connect(self.add_node_into_groups)
        self.tb.addSeparator()

    def set_statusbar(self):
        self.status = QStatusBar()
        self.status_uart=QLabel()
        self.status_uart.setPixmap(QPixmap("././icons/switch_off.png")) 
        self.status.addPermanentWidget(self.status_uart, stretch=0)
        self.setStatusBar(self.status)
        #self.status.showMessage("hello world.")

    def configure_uart_device(self):
        dialog = QDialog(None, Qt.WindowSystemMenuHint)       
        self.uart_ui.setup_ui(dialog)
        #self.uart_ui.set_uart_status(False)
        dialog.exec_()
        dialog.deleteLater()