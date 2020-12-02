# -*- coding: UTF-8 -*-
# !/usr/bin/env python

import os
import sys

from PyQt5 import QtWidgets

from application.main_window import MainWindow

def main():
    App = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(App.exec_())

if __name__ == '__main__':
    main()