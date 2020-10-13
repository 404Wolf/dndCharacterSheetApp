#Weapon Adder Class

def __init__(self, parent=None):
		super(weaponAdder, self).__init__() # Call the inherited classes __init__ method
		try:
			uic.loadUi('./gui/'+guiStyle+"/weaponAdder.ui", self) # Load the .ui file
		except:
			try:
				uic.loadUi('./gui/classic/weaponAdderClassic.ui', self)
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

		self.setWindowTitle("Weapon Adder!")
		self.resize(600,400)

		self.weaponAdderName_entry = self.findChild(QtWidgets.QLineEdit, 'weaponAdderName_entry')
		self.attackBonus_entry = self.findChild(QtWidgets.QSpinBox, 'attackBonus_entry')

		self.weaponAdderDamageType_entry = self.findChild(QtWidgets.QComboBox, 'weaponAdderDamageType_entry')
		self.weight_entry = self.findChild(QtWidgets.QSpinBox, 'weight_entry')
		self.attackBonus_entry = self.findChild(QtWidgets.QSpinBox, 'attackBonus_entry')
		self.weaponAdderNumberOfDice_entry = self.findChild(QtWidgets.QSpinBox, 'weaponAdderNumberOfDice_entry')
		self.weaponAdderTypeOfDice_entry = self.findChild(QtWidgets.QSpinBox, 'weaponAdderTypeOfDice_entry')
		self.attackBonus_entry = self.findChild(QtWidgets.QSpinBox, 'attackBonus_entry')
		self.weaponAdderDescription_textArea = self.findChild(QtWidgets.QTextEdit, 'weaponAdderDescription_textArea')

		self.weaponAdderAdd_button = self.findChild(QtWidgets.QPushButton, 'weaponAdderAdd_button')
		self.weaponAdderAdd_button.clicked.connect(self.finishAddingWeapon)

		self.weaponAdderCancel_button = self.findChild(QtWidgets.QPushButton, 'weaponAdderCancel_button')
		self.weaponAdderCancel_button.clicked.connect(self.abortAddingWeapon)

		#checkboxes:
		self.ammunition_checkBox = self.findChild(QtWidgets.QCheckBox, 'ammunition_checkBox')
		self.finesse_checkBox = self.findChild(QtWidgets.QCheckBox, 'finesse_checkBox')
		self.heavy_checkBox = self.findChild(QtWidgets.QCheckBox, 'heavy_checkBox')
		self.light_checkBox = self.findChild(QtWidgets.QCheckBox, 'light_checkBox')
		self.loading_checkBox = self.findChild(QtWidgets.QCheckBox, 'loading_checkBox')
		self.range_checkBox = self.findChild(QtWidgets.QCheckBox, 'range_checkBox')
		self.reach_checkBox = self.findChild(QtWidgets.QCheckBox, 'reach_checkBox')
		self.special_checkBox = self.findChild(QtWidgets.QCheckBox, 'special_checkBox')
		self.thrown_checkBox = self.findChild(QtWidgets.QCheckBox, 'thrown_checkBox')
		self.twoHanded_checkBox = self.findChild(QtWidgets.QCheckBox, 'twoHanded_checkBox')
		self.versatile_checkBox = self.findChild(QtWidgets.QCheckBox, 'versatile_checkBox')
		self.abilityModifier_entry = self.findChild(QtWidgets.QComboBox, 'abilityModifier_entry')
		self.proficient_checkBox = self.findChild(QtWidgets.QCheckBox, 'proficient_checkBox')

def finishAddingWeapon(self):
	global weaponRefresh
	global pending
	global weaponCounter

	if self.ammunition_checkBox.isChecked():
		ammunition = 1
	else:
		ammunition = 0

	if self.finesse_checkBox.isChecked():
		finesse = 1
	else:
		finesse = 0

	if self.heavy_checkBox.isChecked():
		heavy = 1
	else:
		heavy = 0

	if self.light_checkBox.isChecked():
		light = 1
	else:
		light = 0

	if self.loading_checkBox.isChecked():
		loading = 1
	else:
		loading = 0

	if self.range_checkBox.isChecked():
		range_ = 1
	else:
		range_ = 0

	if self.reach_checkBox.isChecked():
		reach = 1
	else:
		reach = 0

	if self.special_checkBox.isChecked():
		special = 1
	else:
		special = 0

	if self.thrown_checkBox.isChecked():
		thrown = 1
	else:
		thrown = 0

	if self.twoHanded_checkBox.isChecked():
		twoHanded = 1
	else:
		twoHanded = 0

	if self.versatile_checkBox.isChecked():
		versatile = 1
	else:
		versatile = 0

	if self.proficient_checkBox.isChecked():
		proficient = 1
	else:
		proficient = 0

	pending = {
	"name":self.weaponAdderName_entry.text(),
	"proficient":proficient,
	"damageType":self.weaponAdderDamageType_entry.currentText(),
	"abilityModifier":self.abilityModifier_entry.currentText(),
	"weight":self.weight_entry.value(),
	"description":self.weaponAdderDescription_textArea.toPlainText(),
	"attackBonusBoost":self.attackBonus_entry.value(),
	"numberOfDice":self.weaponAdderNumberOfDice_entry.value(),
	"typeOfDice":self.weaponAdderTypeOfDice_entry.value(),
	"ammunition":ammunition,
	"finesse":finesse,
	"heavy":heavy,
	"light":light,
	"loading":loading,
	"range":range_,
	"reach":reach,
	"special":special,
	"thrown":thrown,
	"twoHanded":twoHanded,
	"versatile":versatile,
	}

	pendingWeapon[str(weaponCounter)] = pending
	self.weaponAdderName_entry.setText("")
	self.weight_entry.setValue(0)
	self.weaponAdderDamageType_entry.setCurrentText("Bludgeoning")
	self.attackBonus_entry.setValue(0)
	self.ammunition_checkBox.setCheckState(False)
	self.finesse_checkBox.setCheckState(False)
	self.heavy_checkBox.setCheckState(False)
	self.light_checkBox.setCheckState(False)
	self.loading_checkBox.setCheckState(False)
	self.range_checkBox.setCheckState(False)
	self.reach_checkBox.setCheckState(False)
	self.loading_checkBox.setCheckState(False)
	self.range_checkBox.setCheckState(False)
	self.twoHanded_checkBox.setCheckState(False)
	self.versatile_checkBox.setCheckState(False)


	weaponCounter+=1
	weaponRefresh=True

def abortAddingWeapon(self):
	weaponAdder.close()