from sqlite3.dbapi2 import connect
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from application.db import Database

class UartDeviceDialog(object):
    def __init__(self):
        super().__init__()
        self.db_con = Database().get_connection()
    
    def setup_ui(self, Dialog):
        self.dialog = Dialog
        self.dialog.setWindowTitle("Configure Uart Device")
        self.dialog.setWindowIcon(QIcon("././icons/uart.png"))
        self.dialog.setFixedSize(200, 250)

        buttons = QDialogButtonBox.Save | QDialogButtonBox.Cancel
        buttonBox = QDialogButtonBox(buttons, Dialog)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.comboBox_port = QComboBox()
        self.comboBox_baudrate = QComboBox()
        self.comboBox_port.addItems([str(i) for i in list(range(10))])        
        self.comboBox_baudrate.addItems([str(i) for i in ['9600', '115200']])
        btn_connect_uart = QPushButton("Connect")
        btn_connect_uart.clicked.connect(self.connect_uart_device)

        formlayout = QFormLayout()
        formlayout.addRow(QLabel("Port: "), self.comboBox_port)
        formlayout.addRow(QLabel("Baudrate: "), self.comboBox_baudrate)
        formlayout.addRow(QLabel(""), btn_connect_uart)

        hbox = QHBoxLayout()
        self.checkbox_enable_logger = QCheckBox('Enable Logging')
        hbox.addWidget(self.checkbox_enable_logger) 

        self.vbox = QVBoxLayout()
        self.groupbox_uart_device = QGroupBox("Uart Device")
        self.groupbox_uart_device.setLayout(formlayout)
        self.groupbox_enable_logging = QGroupBox("Logger")
        self.groupbox_enable_logging.setLayout(hbox)

        self.vbox.addWidget(self.groupbox_uart_device)
        self.vbox.addWidget(self.groupbox_enable_logging)
        self.vbox.addStretch()
        self.vbox.addWidget(buttonBox)        

        self.dialog.setLayout(self.vbox)

    def accept(self):
        if (self.db_con != None):
            self.update_uart_device_database()
        else:
            self.db_con = Database().get_connection()
            self.update_uart_device_database()

    def reject(self):
        self.dialog.close()

    def set_uart_status(self, connection):
        if (self.db_con != None):
            self.update_uart_connection_database(connection)
        else:
            self.db_con = Database().get_connection()
            self.update_uart_connection_database(connection)

        
    def get_uart_status(self):        
        return self.uart_connected

    def update_uart_device_database(self):
        db_cursor = self.db_con.cursor()
        device_name = "COM" + str(self.comboBox_port.currentText())
        device_baudrate = int(self.comboBox_baudrate.currentText())
        device_port = int(self.comboBox_port.currentText())
        device_connection_status = "TRUE"
        enable_logging = "TRUE" if self.checkbox_enable_logger.checkState() == 2 else "FALSE"

        update_settings_query = ("UPDATE SETTINGS SET device_name=?, device_baudrate=?, device_port=?, device_connection_status=?, enable_logging=? WHERE id = 1")
        db_cursor.execute(update_settings_query,(device_name, device_baudrate, device_port, device_connection_status, enable_logging))
        self.db_con.commit()

        print("update_uart device setting to database")    

    def update_uart_connection_database(self, connection):
        db_cursor = self.db_con.cursor()
        
        if (connection != True):
            device_connection_status = "FALSE"
        else:
            device_connection_status = "TRUE"
        
        update_settings_query = ("UPDATE SETTINGS SET device_connection_status=? WHERE id = 1")
        db_cursor.execute(update_settings_query,(device_connection_status,))
        self.db_con.commit()

        print("update uart connection status to database")
    
    


    def connect_uart_device(self):
        pass

