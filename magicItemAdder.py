#Magic Item Adder Class

def __init__(self, parent=None):
		super(magicItemAdder, self).__init__() # Call the inherited classes __init__ method
		try:
			uic.loadUi('./gui/'+guiStyle+"/magicItemAdder.ui", self) # Load the .ui file
		except:
			try:
				uic.loadUi('./gui/classic/magicItemAdder.ui', self)
			except:
				print("Failed to start")
				from PyQt5.QtWidgets import QMessageBox
				failure = QMessageBox()
				failure.setWindowTitle("Failure: Critical")
				failure.setText("Failed to start.")
				failure.setDescriptiveText("Error: Corrupted config file.")
				failure.setIcon(QMessageBox.Critical)
				failure.setStandardButtons(QMessageBox.Ok)
				failure.setDefaultButton(QMessageBox.Retry)
				failureReturnValue=failure.exec_()

		self.setWindowTitle("Magic Item Adder!")
		self.resize(600,400)

		#push buttons (normal buttons)

		self.magicItemAdderCancel_button = self.findChild(QtWidgets.QPushButton, 'magicItemAdderCancel_button')
		self.magicItemAdderCancel_button.clicked.connect(self.abortAddingMagicItem)

		self.magicItemAdderAdd_button = self.findChild(QtWidgets.QPushButton, 'magicItemAdderAdd_button')
		self.magicItemAdderAdd_button.clicked.connect(self.finishAddingMagicItem)

		#labels
		self.magicItemAdderName_label = self.findChild(QtWidgets.QLabel, 'magicItemAdderName_label')
		self.magicItemAdderType_label = self.findChild(QtWidgets.QLabel, 'magicItemAdderType_label')
		self.magicItemAdderRarity_label = self.findChild(QtWidgets.QLabel, 'magicItemAdderRarity_label')
		self.magicItemAdderDescription_label = self.findChild(QtWidgets.QLabel, 'magicItemAdderDescription_label')

		#line edit areas
		self.magicItemAdderName_entry = self.findChild(QtWidgets.QLineEdit, 'magicItemAdderName_entry')

		#combo boxes (dropdown menues)
		self.magicItemAdderType_entry = self.findChild(QtWidgets.QComboBox, 'magicItemAdderType_entry')
		self.magicItemAdderRarity_entry = self.findChild(QtWidgets.QComboBox, 'magicItemAdderRarity_entry')

		#text edit areas
		self.magicItemAdderDescription_textArea = self.findChild(QtWidgets.QTextEdit, 'magicItemAdderDescription_textArea')

		#check boxes
		self.magicItemAdderAttunement_checkBox = self.findChild(QtWidgets.QCheckBox, 'magicItemAdderAttunement_checkBox')

		mainWindow.magicItemsBox_textEdit = self.findChild(QtWidgets.QTextEdit, 'magicItemsBox_textEdit')
def finishAddingMagicItem(self):
		global magicItemCounter
		global magicItemRefresh
		global pendingMagicItem
		if self.magicItemAdderAttunement_checkBox.isChecked():
			temp = 1
		else:
			temp = 0
		pending = {
		"name":self.magicItemAdderName_entry.text(),
		"type":self.magicItemAdderType_entry.currentText(),
		"rarity":self.magicItemAdderRarity_entry.currentText(),
		"attunement":temp,
		"description":self.magicItemAdderDescription_textArea.toPlainText()
		}
		pendingMagicItem[str(magicItemCounter)] = pending
		self.magicItemAdderName_entry.setText("")
		self.magicItemAdderDescription_textArea.setText("")
		self.magicItemAdderAttunement_checkBox.setCheckState(False)
		magicItemCounter+=1
		magicItemRefresh=True

def abortAddingMagicItem(self):
	magicItemAdder.close()