def __init__(self, parent=None):
	super(saveSheet, self).__init__() # Call the inherited classes __init__ method

	try:
		uic.loadUi('./gui/'+guiStyle+"/sheetNamer.ui", self) # Load the .ui file
	except:
		try:
			uic.loadUi('sheetNamer.ui', self)
		except:
			print("Failed to start")
			from PyQt5.QtWidgets import QMessageBox
			failure = QMessageBox()
			failure.setWindowTitle("Failure: Critical")
			failure.setText("Failed to start.")
			failure.setIcon(QMessageBox.Critical)
			failure.setStandardButtons(QMessageBox.Ok)
			failure.setDefaultButton(QMessageBox.Retry)
			failureReturnValue=failure.exec_()

	self.setWindowTitle("Set sheet name")
	self.resize(300,200)

	self.sheetName_entry = self.findChild(QtWidgets.QLineEdit, 'sheetName_entry')

	self.cancelSheetName_button = self.findChild(QtWidgets.QPushButton, 'cancelSheetName_button')
	self.cancelSheetName_button.clicked.connect(lambda:saveSheet.close())

	self.setSheetName_button = self.findChild(QtWidgets.QPushButton, 'setSheetName_button')
	self.setSheetName_button.clicked.connect(self.save)

	sheetNameInput = ""
	
def save(self):
	global sheetNameInput
	sheetNameInput = self.sheetName_entry.text()
	global doneSettingName
	doneSettingName = True
	mainWindow.saveSheet()
	self.sheetName_entry.setText("")
	mainWindow.sheetName_label.setText(sheetNameInput.title())
	saveSheet.close()