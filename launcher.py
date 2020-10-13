from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import json
import os
from send2trash import send2trash
from variables import *

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
app.setStyle("fusion")

with open("config.json") as configFile:
	config = json.load(configFile)
	guiStyle = config["guiStyle"]

class saveSheet(QtWidgets.QDialog):
	with open("saveSheet.py","rt") as saveSheet:
		exec(saveSheet.read())

class weaponAdder(QtWidgets.QDialog):
	with open("weaponAdder.py","rt") as saveSheet:
		exec(saveSheet.read())

class magicItemAdder(QtWidgets.QDialog):
	with open("magicItemAdder.py","rt") as saveSheet:
		exec(saveSheet.read())

class mainWindow(QtWidgets.QMainWindow):
	with open("mainWindow.py","rt") as saveSheet:
		exec(saveSheet.read())

mainWindow = mainWindow() # Create an instance of our class
magicItemAdder = magicItemAdder()
weaponAdder = weaponAdder()
saveSheet = saveSheet()
app.exec_() # Start the application