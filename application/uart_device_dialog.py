from sqlite3.dbapi2 import connect
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from application.db import Database
from interactive_pyaci.interactive_pyaci import Interactive 
from interactive_pyaci.aci.aci_uart import Uart

class UartDeviceDialog(object):
    def __init__(self):
        super().__init__()
        self.db_con = Database().get_connection()
        self.device = None
    
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
        self.btn_connect_uart = QPushButton("Connect")
        self.btn_connect_uart.clicked.connect(self.connect_uart_device)

        formlayout = QFormLayout()
        formlayout.addRow(QLabel("Port: "), self.comboBox_port)
        formlayout.addRow(QLabel("Baudrate: "), self.comboBox_baudrate)
        formlayout.addRow(QLabel(""), self.btn_connect_uart)

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

        self.refresh_ui()
    
    def refresh_ui(self):
        self.read_db_uart_device()

        self.comboBox_port.setCurrentText(str(self.device_port))
        self.comboBox_baudrate.setCurrentText(str(self.device_baudrate))
        if self.enable_logging >= 1:
            self.checkbox_enable_logger.setChecked(True)
        else:
            self.checkbox_enable_logger.setChecked(False)
        
        if self.device is not None:
            if self.device.dev_still_running() == True:
                self.btn_connect_uart.setText("Disconnect")

    def accept(self):
        if (self.db_con != None):
            self.update_db_uart_device()
        else:
            self.db_con = Database().get_connection()
            self.update_db_uart_device()

    def reject(self):
        self.dialog.close()

    def set_uart_device_status(self, connection):
        if (self.db_con != None):
            self.update_db_uart_device_connection(connection)
        else:
            self.db_con = Database().get_connection()
            self.update_db_uart_device_connection(connection)
        
    def get_uart_device_status(self):
        if self.device is not None:
            return self.device.dev_still_running()
        else:
            return False
    
    def get_interactive_device(self):
        return self.device

    def connect_uart_device(self):
        self.device_name = "COM" + str(self.comboBox_port.currentText())
        self.device_port = int(self.comboBox_port.currentText())
        self.device_baudrate = int(self.comboBox_baudrate.currentText())
        self.enable_logging = 1 if self.checkbox_enable_logger.checkState() == 2 else 0

        if self.device is None:
            self.device = Interactive(
                            Uart(port=self.device_name, baudrate=self.device_baudrate, device_name=self.device_name), 
                            self.enable_logging)

            if self.device is not None:
                send = self.device.acidev.write_aci_cmd
                self.btn_connect_uart.setText("Disconnect")
                self.update_db_uart_device_connection(True)
        else:
            self.device.close()
            self.device = None
            self.update_db_uart_device_connection(False)

#################################### database #################################################################
    def update_db_uart_device(self):
        db_cursor = self.db_con.cursor()
        self.device_name = "COM" + str(self.comboBox_port.currentText())
        self.device_baudrate = int(self.comboBox_baudrate.currentText())
        self.device_port = int(self.comboBox_port.currentText())
        self.enable_logging = 1 if self.checkbox_enable_logger.checkState() == 2 else 0

        update_settings_query = (
            "UPDATE SETTINGS SET device_name=?, device_baudrate=?, device_port=?, device_connected=?, enable_logging=? WHERE id = 1")
        db_cursor.execute(
            update_settings_query,(self.device_name, self.device_baudrate, self.device_port, self.device_connected, self.enable_logging))
        self.db_con.commit()

    def update_db_uart_device_connection(self, connection):
        db_cursor = self.db_con.cursor()        
        if (connection != True):
            self.device_connected = 0
        else:
            self.device_connected = 1
        
        update_settings_query = ("UPDATE SETTINGS SET device_connected=? WHERE id = 1")
        db_cursor.execute(update_settings_query,(self.device_connected,))
        self.db_con.commit()
    
    def read_db_uart_device(self):
        db_cursor = self.db_con.cursor()
        select_query = "SELECT * FROM SETTINGS WHERE id = 1"
        db_cursor.execute(select_query)
        rows = db_cursor.fetchone()

        self.device_name = rows[1]
        self.device_port = rows[3]
        self.device_baudrate = rows[2]
        self.enable_logging = rows[5]