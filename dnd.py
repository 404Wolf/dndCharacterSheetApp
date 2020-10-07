from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
import json
import os
from send2trash import send2trash

magicItemRefresh = False
weaponRefresh = False
statChange = False
times = False
doneSettingName = False
loadTemplate = False
firstRun = True

pendingMagicItem = {}
template = {}
pendingWeapon = {}

magicItemCounter = 1
weaponCounter = 1
x = 1

skills = {
"acrobatics":"dexterity",
"animalHandling":"wisdom",
"arcana":"intelligence",
"athletics":"strength",
"deception":"charisma",
"history":"intelligence",
"insight":"wisdom",
"intimidation":"charisma",
"investigation":"intelligence",
"medicine":"wisdom",
"nature":"intelligence",
"perception":"wisdom",
"performance":"charisma",
"persuasion":"charisma",
"religion":"intelligence",
"sleightOfHand":"dexterity",
"stealth":"dexterity",
"survival":"wisdom"
}

spellSlots = ["levelZero_entry1",
"levelZero_entry2","levelZero_entry3","levelZero_entry4","levelZero_entry5",
"levelZero_entry6","levelZero_entry7","levelOne_entry1","levelOne_entry2",
"levelOne_entry3","levelOne_entry4","levelOne_entry5","levelOne_entry6",
"levelOne_entry7","levelTwo_entry1","levelTwo_entry2","levelTwo_entry3",
"levelTwo_entry4","levelTwo_entry5","levelTwo_entry6","levelTwo_entry7",
"levelThree_entry1","levelThree_entry2","levelThree_entry3","levelThree_entry4",
"levelThree_entry5","levelThree_entry6","levelThree_entry7","levelFour_entry1",
"levelFour_entry2","levelFour_entry3","levelFour_entry4","levelFour_entry5",
"levelFour_entry6","levelFour_entry7","levelFive_entry1","levelFive_entry2",
"levelFive_entry3","levelFive_entry4","levelFive_entry5","levelFive_entry6",
"levelFive_entry7","levelSix_entry1","levelSix_entry2","levelSix_entry3",
"levelSix_entry4","levelSix_entry5","levelSix_entry6","levelSix_entry7",
"levelSeven_entry1","levelSeven_entry2","levelSeven_entry3","levelSeven_entry4",
"levelSeven_entry5","levelSeven_entry6","levelSeven_entry7","levelEight_entry1",
"levelEight_entry2","levelEight_entry3","levelEight_entry4","levelEight_entry5",
"levelEight_entry6","levelEight_entry7","levelNine_entry1","levelNine_entry2",
"levelNine_entry3","levelNine_entry4","levelNine_entry5","levelNine_entry6",
"levelNine_entry7"]

with open("config.json") as configFile:
	config = json.load(configFile)
	guiStyle = config["guiStyle"]

class saveSheet(QtWidgets.QDialog):
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

class weaponAdder(QtWidgets.QDialog):
	QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)


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
		app.setStyle("fusion")

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

class magicItemAdder(QtWidgets.QDialog):
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

class mainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent=None):
		super(mainWindow, self).__init__() # Call the inherited classes __init__ method
		try:
			uic.loadUi('./gui/'+guiStyle+"/mainWindow.ui", self) # Load the .ui file
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
		self.setWindowIcon(QtGui.QIcon('./resources/icon.ico'))

		self.setWindowTitle("DND Character Sheet Viewer")
		self.resize(1000,600)
		self.setMinimumSize(970, 400)
		self.loadSheetList()

		#push buttons (normal buttons)
		spellCasterShadow = QtWidgets.QGraphicsDropShadowEffect()
		spellCasterShadow.setBlurRadius(20)
		spellCasterShadow.setOffset(1)
		spellCasterShadow.setColor(QtGui.QColor(43, 43, 43, 120))
		self.spellcaster_toggleButton = self.findChild(QtWidgets.QPushButton, 'spellcaster_toggleButton')
		self.spellcaster_toggleButton.clicked.connect(self.spellcasterOrNot)
		#self.spellcaster_toggleButton.setGraphicsEffect(spellCasterShadow)

		self.add_button = self.findChild(QtWidgets.QPushButton, 'add_button')
		self.add_button.clicked.connect(self.addCurrency)

		self.newCharacter_button = self.findChild(QtWidgets.QPushButton, "newCharacter_button")
		self.newCharacter_button.clicked.connect(self.newCharacter)
		
		self.remove_button = self.findChild(QtWidgets.QPushButton, 'remove_button')
		self.remove_button.clicked.connect(self.removeCurrency)

		self.addMagicItem_button = self.findChild(QtWidgets.QPushButton, 'addMagicItem_button')
		self.addMagicItem_button.clicked.connect(self.addMagicItem)

		self.removeMagicItem_button = self.findChild(QtWidgets.QPushButton, 'removeMagicItem_button')
		self.removeMagicItem_button.clicked.connect(self.removingMagicItem)

		self.addWeapon_button = self.findChild(QtWidgets.QPushButton, 'addWeapon_button')
		self.addWeapon_button.clicked.connect(self.addingWeapon)

		self.removeWeapon_button = self.findChild(QtWidgets.QPushButton, 'removeWeapon_button')
		self.removeWeapon_button.clicked.connect(self.removingWeapon)

		saveCharacterShadow = QtWidgets.QGraphicsDropShadowEffect()
		saveCharacterShadow.setBlurRadius(20)
		saveCharacterShadow.setOffset(1)
		self.saveCharacter_button = self.findChild(QtWidgets.QPushButton,'saveCharacter_button')
		self.saveCharacter_button.clicked.connect(self.saveSheet)
		#self.saveCharacter_button.setGraphicsEffect(saveCharacterShadow)

		newCharacterShadow = QtWidgets.QGraphicsDropShadowEffect()
		newCharacterShadow.setBlurRadius(20)
		newCharacterShadow.setOffset(1)
		self.removeCharacter_button = self.findChild(QtWidgets.QPushButton,'removeCharacter_button')
		self.removeCharacter_button.clicked.connect(self.removeCharacter)
		#self.removeCharacter_button.setGraphicsEffect(newCharacterShadow)

		openCharacterShadow = QtWidgets.QGraphicsDropShadowEffect()
		openCharacterShadow.setBlurRadius(20)
		openCharacterShadow.setOffset(1)
		self.openCharacter_button = self.findChild(QtWidgets.QPushButton,'openCharacter_button')
		self.openCharacter_button.clicked.connect(self.loadSheet)
		#self.openCharacter_button.setGraphicsEffect(openCharacterShadow)

		self.levelFourHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelFourHelp_button3')
		self.levelFourHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelFourHelp_button1')
		self.levelFourHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelFourHelp_button4')
		self.levelFourHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelFourHelp_button5')
		self.levelFourHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelFourHelp_button2')
		self.levelFourHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelFourHelp_button7')
		self.levelFourHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelFourHelp_button6')
		self.levelFiveHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelFiveHelp_button4')
		self.levelFiveHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelFiveHelp_button5')
		self.levelFiveHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelFiveHelp_button7')
		self.levelFiveHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelFiveHelp_button6')
		self.levelFiveHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelFiveHelp_button2')
		self.levelFiveHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelFiveHelp_button1')
		self.levelFiveHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelFiveHelp_button3')
		self.levelSixHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelSixHelp_button7')
		self.levelSixHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelSixHelp_button6')
		self.levelSixHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelSixHelp_button5')
		self.levelSixHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelSixHelp_button4')
		self.levelSixHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelSixHelp_button3')
		self.levelSixHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelSixHelp_button2')
		self.levelSixHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelSixHelp_button1')
		self.levelSevenHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelSevenHelp_button6')
		self.levelSevenHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelSevenHelp_button7')
		self.levelSevenHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelSevenHelp_button2')
		self.levelSevenHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelSevenHelp_button1')
		self.levelSevenHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelSevenHelp_button3')
		self.levelSevenHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelSevenHelp_button4')
		self.levelSevenHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelSevenHelp_button5')
		self.levelOneHelp_button2_3 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button2_3')
		self.levelOneHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button3')
		self.levelOneHelp_button4_3 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button4_3')
		self.levelOneHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button5')
		self.levelOneHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button6')
		self.levelOneHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button1')
		self.levelOneHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button7')
		self.levelZeroHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button1')
		self.levelZeroHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button2')
		self.levelZeroHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button6')
		self.levelZeroHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button4')
		self.levelZeroHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button7')
		self.levelZeroHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button5')
		self.levelZeroHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button3')
		self.levelZeroHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button1')
		self.levelZeroHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button3')
		self.levelZeroHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button6')
		self.levelZeroHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button2')
		self.levelZeroHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button5')
		self.levelZeroHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button4')
		self.levelZeroHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelZeroHelp_button7')
		self.levelOneHelp_button5_4 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button5_4')
		self.levelOneHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button6')
		self.levelOneHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button1')
		self.levelOneHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button4')
		self.levelOneHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button2')
		self.levelOneHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button7')
		self.levelOneHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelOneHelp_button3')
		self.levelEightHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelEightHelp_button1')
		self.levelEightHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelEightHelp_button3')
		self.levelEightHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelEightHelp_button4')
		self.levelEightHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelEightHelp_button6')
		self.levelEightHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelEightHelp_button7')
		self.levelEightHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelEightHelp_button5')
		self.levelEightHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelEightHelp_button2')
		self.levelNineHelp_button3 = self.findChild(QtWidgets.QPushButton, 'levelNineHelp_button3')
		self.levelNineHelp_button2 = self.findChild(QtWidgets.QPushButton, 'levelNineHelp_button2')
		self.levelNineHelp_button4 = self.findChild(QtWidgets.QPushButton, 'levelNineHelp_button4')
		self.levelNineHelp_button5 = self.findChild(QtWidgets.QPushButton, 'levelNineHelp_button5')
		self.levelNineHelp_button6 = self.findChild(QtWidgets.QPushButton, 'levelNineHelp_button6')
		self.levelNineHelp_button7 = self.findChild(QtWidgets.QPushButton, 'levelNineHelp_button7')
		self.levelNineHelp_button1 = self.findChild(QtWidgets.QPushButton, 'levelNineHelp_button1')


		#spin boxes (integer entry boxes)
		self.XP_entry = self.findChild(QtWidgets.QSpinBox, 'XP_entry')
		self.level_entry = self.findChild(QtWidgets.QSpinBox, 'level_entry')
		self.proficiencyBonus_entry = self.findChild(QtWidgets.QSpinBox, 'proficiencyBonus_entry')
		self.armorClass_entry = self.findChild(QtWidgets.QSpinBox, 'armorClass_entry')
		self.typeOfHitDice_entry = self.findChild(QtWidgets.QSpinBox, 'typeOfHitDice_entry')
		self.spinBox_3 = self.findChild(QtWidgets.QSpinBox, 'spinBox_3')
		self.spinBox_4 = self.findChild(QtWidgets.QSpinBox, 'spinBox_4')
		self.initiativeBoost_entry = self.findChild(QtWidgets.QSpinBox, 'initiativeBoost_entry')
		self.speed_entry = self.findChild(QtWidgets.QSpinBox, 'speed_entry')
		self.spinBox = self.findChild(QtWidgets.QSpinBox, 'spinBox')
		self.strength_entry = self.findChild(QtWidgets.QSpinBox, 'strength_entry')
		self.dexterity_entry = self.findChild(QtWidgets.QSpinBox, 'dexterity_entry')
		self.wisdom_entry = self.findChild(QtWidgets.QSpinBox, 'wisdom_entry')
		self.constitution_entry = self.findChild(QtWidgets.QSpinBox, 'constitution_entry')
		self.intelligence_entry = self.findChild(QtWidgets.QSpinBox, 'intelligence_entry')
		self.charisma_entry = self.findChild(QtWidgets.QSpinBox, 'charisma_entry')
		self.cp_entry = self.findChild(QtWidgets.QSpinBox, 'cp_entry')
		self.ep_entry = self.findChild(QtWidgets.QSpinBox, 'ep_entry')
		self.sp_entry = self.findChild(QtWidgets.QSpinBox, 'sp_entry')
		self.gp_entry = self.findChild(QtWidgets.QSpinBox, 'gp_entry')
		self.pp_entry = self.findChild(QtWidgets.QSpinBox, 'pp_entry')
		self.add_entry = self.findChild(QtWidgets.QSpinBox, 'add_entry')
		self.remove_entry = self.findChild(QtWidgets.QSpinBox, 'remove_entry')
		self.persuasionBoost_entry = self.findChild(QtWidgets.QSpinBox, 'persuasionBoost_entry')
		self.perceptionBoost_entry = self.findChild(QtWidgets.QSpinBox, 'perceptionBoost_entry')
		self.performanceBoost_entry = self.findChild(QtWidgets.QSpinBox, 'performanceBoost_entry')
		self.religionBoost_entry = self.findChild(QtWidgets.QSpinBox, 'religionBoost_entry')
		self.slightOfHandBoost_entry = self.findChild(QtWidgets.QSpinBox, 'slightOfHandBoost_entry')
		self.stealthBoost_entry = self.findChild(QtWidgets.QSpinBox, 'stealthBoost_entry')
		self.natureBoost_entry = self.findChild(QtWidgets.QSpinBox, 'natureBoost_entry')
		self.survivalBoost_entry = self.findChild(QtWidgets.QSpinBox, 'survivalBoost_entry')
		self.arcanaBoost_entry = self.findChild(QtWidgets.QSpinBox, 'arcanaBoost_entry')
		self.athleticsBoost_entry = self.findChild(QtWidgets.QSpinBox, 'athleticsBoost_entry')
		self.animalHandling_entry = self.findChild(QtWidgets.QSpinBox, 'animalHandling_entry')
		self.insightBoost_entry = self.findChild(QtWidgets.QSpinBox, 'insightBoost_entry')
		self.intimidationBoost_entry = self.findChild(QtWidgets.QSpinBox, 'intimidationBoost_entry')
		self.deceptionBoost_entry = self.findChild(QtWidgets.QSpinBox, 'deceptionBoost_entry')
		self.acrobaticsBoost_entry = self.findChild(QtWidgets.QSpinBox, 'acrobaticsBoost_entry')
		self.medicineBoost_entry = self.findChild(QtWidgets.QSpinBox, 'medicineBoost_entry')
		self.investigationBoost_entry = self.findChild(QtWidgets.QSpinBox, 'investigationBoost_entry')
		self.historyBoost_entry = self.findChild(QtWidgets.QSpinBox, 'historyBoost_entry')
		self.heightFeet_entry = self.findChild(QtWidgets.QSpinBox, 'heightFeet_entry')
		self.heightInches_entry = self.findChild(QtWidgets.QSpinBox, 'heightInches_entry')
		self.weightPounds_entry = self.findChild(QtWidgets.QSpinBox, 'weightPounds_entry')
		self.age_entry = self.findChild(QtWidgets.QSpinBox, 'age_entry')
		self.removeMagicItem_entry = self.findChild(QtWidgets.QSpinBox, 'removeMagicItem_entry')
		self.removeWeapon_entry = self.findChild(QtWidgets.QSpinBox, 'removeWeapon_entry')


		#labels
		titleShadow = QtWidgets.QGraphicsDropShadowEffect()
		titleShadow.setBlurRadius(20)
		titleShadow.setOffset(1)
		self.dndCharacterSheetViewer_label = self.findChild(QtWidgets.QLabel,'dndCharacterSheetViewer_label')
		#self.dndCharacterSheetViewer_label.setGraphicsEffect(titleShadow)

		sheetNameShadow = QtWidgets.QGraphicsDropShadowEffect()
		sheetNameShadow.setBlurRadius(20)
		sheetNameShadow.setOffset(1)
		self.sheetName_label = self.findChild(QtWidgets.QLabel,'sheetName_label')
		#self.sheetName_label.setGraphicsEffect(sheetNameShadow)

		self.physicalAppearence_label = self.findChild(QtWidgets.QLabel, 'physicalAppearence_label')
		self.race_label = self.findChild(QtWidgets.QLabel, 'race_label')
		self.level_label = self.findChild(QtWidgets.QLabel, 'level_label')
		self.characterName_label = self.findChild(QtWidgets.QLabel, 'characterName_label')
		self.playerName_label = self.findChild(QtWidgets.QLabel, 'playerName_label')
		self.class_label = self.findChild(QtWidgets.QLabel, 'class_label')
		self.background_label = self.findChild(QtWidgets.QLabel, 'background_label')
		self.XP_label = self.findChild(QtWidgets.QLabel, 'XP_label')
		self.alignment_label = self.findChild(QtWidgets.QLabel, 'alignment_label')
		self.proficiencyBonus_label = self.findChild(QtWidgets.QLabel, 'proficiencyBonus_label')
		self.inspiration_label = self.findChild(QtWidgets.QLabel, 'inspiration_label')
		self.fail_label = self.findChild(QtWidgets.QLabel, 'fail_label')
		self.success_label = self.findChild(QtWidgets.QLabel, 'success_label')
		self.deathSaves_label = self.findChild(QtWidgets.QLabel, 'deathSaves_label')
		self.armorClass_label = self.findChild(QtWidgets.QLabel, 'armorClass_label')
		self.armorType_label = self.findChild(QtWidgets.QLabel, 'armorType_label')
		self.hitPoints_label = self.findChild(QtWidgets.QLabel, 'hitPoints_label')
		self.maxHP_label = self.findChild(QtWidgets.QLabel, 'maxHP_label')
		self.currentHP_label = self.findChild(QtWidgets.QLabel, 'currentHP_label')
		self.tempHP_label = self.findChild(QtWidgets.QLabel, 'tempHP_label')
		self.initiative_label = self.findChild(QtWidgets.QLabel, 'initiative_label')
		self.initiativeScore_label = self.findChild(QtWidgets.QLabel, 'initiativeScore_label')
		self.initiativeBoost_label = self.findChild(QtWidgets.QLabel, 'initiativeBoost_label')
		self.initiativeScore_label = self.findChild(QtWidgets.QLabel, 'initiativeScore_label')
		self.speed_label = self.findChild(QtWidgets.QLabel, 'speed_label')
		self.hitDice_label = self.findChild(QtWidgets.QLabel, 'hitDice_label')
		self.numberOfHitDice_label = self.findChild(QtWidgets.QLabel, 'numberOfHitDice_label')
		self.dHitDice_label = self.findChild(QtWidgets.QLabel, 'dHitDice_label')
		self.modifiers_label_upper = self.findChild(QtWidgets.QLabel, 'modifiers_label_upper')
		self.dexteritySaveModifier_label = self.findChild(QtWidgets.QLabel, 'dexteritySaveModifier_label')
		self.wisdomSaveModifier_label = self.findChild(QtWidgets.QLabel, 'wisdomSaveModifier_label')
		self.charismaSaveModifier_label = self.findChild(QtWidgets.QLabel, 'charismaSaveModifier_label')
		self.strengthSaveModifier_label = self.findChild(QtWidgets.QLabel, 'strengthSaveModifier_label')
		self.intelligenceSaveModifier_label = self.findChild(QtWidgets.QLabel, 'intelligenceSaveModifier_label')
		self.scores_label_upper = self.findChild(QtWidgets.QLabel, 'scores_label_upper')
		self.constitution_label = self.findChild(QtWidgets.QLabel, 'constitution_label')
		self.strength_modifier = self.findChild(QtWidgets.QLabel, 'strength_modifier')
		self.constitution_modifier = self.findChild(QtWidgets.QLabel, 'constitution_modifier')
		self.stats_label_upper = self.findChild(QtWidgets.QLabel, 'stats_label_upper')
		self.intelligence_modifier = self.findChild(QtWidgets.QLabel, 'intelligence_modifier')
		self.dexterity_modifier = self.findChild(QtWidgets.QLabel, 'dexterity_modifier')
		self.wisdom_modifier = self.findChild(QtWidgets.QLabel, 'wisdom_modifier')
		self.charisma_modifier = self.findChild(QtWidgets.QLabel, 'charisma_modifier')
		self.constitutionSaveModifier_label = self.findChild(QtWidgets.QLabel, 'constitutionSaveModifier_label')
		self.strength_label = self.findChild(QtWidgets.QLabel, 'strength_label')
		self.dexterity_label = self.findChild(QtWidgets.QLabel, 'dexterity_label')
		self.wisdom_label = self.findChild(QtWidgets.QLabel, 'wisdom_label')
		self.intelligence_label = self.findChild(QtWidgets.QLabel, 'intelligence_label')
		self.charisma_label = self.findChild(QtWidgets.QLabel, 'charisma_label')
		self.saves_label_upper = self.findChild(QtWidgets.QLabel, 'saves_label_upper')
		self.add_label = self.findChild(QtWidgets.QLabel, 'add_label')
		self.remove_label = self.findChild(QtWidgets.QLabel, 'remove_label')
		self.currency_labelsc = self.findChild(QtWidgets.QLabel, 'currency_labelsc')
		self.proficiencies_label = self.findChild(QtWidgets.QLabel, 'proficiencies_label')
		self.languages_label = self.findChild(QtWidgets.QLabel, 'languages_label')
		self.misc_textArea = self.findChild(QtWidgets.QLabel, 'misc_textArea_3')
		self.skills_label = self.findChild(QtWidgets.QLabel, 'skills_label')
		self.athleticsModifier_label = self.findChild(QtWidgets.QLabel, 'athleticsModifier_label')
		self.deceptionStatUsed_label = self.findChild(QtWidgets.QLabel, 'deceptionStatUsed_label')
		self.acrobaticsStatUsed_label = self.findChild(QtWidgets.QLabel, 'acrobaticsStatUsed_label')
		self.boost_label = self.findChild(QtWidgets.QLabel, 'boost_label')
		self.medicineStatUsed_label = self.findChild(QtWidgets.QLabel, 'medicineStatUsed_label')
		self.investigationModifier_label = self.findChild(QtWidgets.QLabel, 'investigationModifier_label')
		self.acrobaticsModifier_label = self.findChild(QtWidgets.QLabel, 'acrobaticsModifier_label')
		self.athleticsStatUsed_label = self.findChild(QtWidgets.QLabel, 'athleticsStatUsed_label')
		self.investigationStatUsed_label = self.findChild(QtWidgets.QLabel, 'investigationStatUsed_label')
		self.stat_label = self.findChild(QtWidgets.QLabel, 'stat_label')
		self.intimidationStatUsed_label = self.findChild(QtWidgets.QLabel, 'intimidationStatUsed_label')
		self.insightModifier_label = self.findChild(QtWidgets.QLabel, 'insightModifier_label')
		self.arcanaStatUsed_label = self.findChild(QtWidgets.QLabel, 'arcanaStatUsed_label')
		self.modifier_label = self.findChild(QtWidgets.QLabel, 'modifier_label')
		self.historyModifier_label = self.findChild(QtWidgets.QLabel, 'historyModifier_label')
		self.medicineModifier_label = self.findChild(QtWidgets.QLabel, 'medicineModifier_label')
		self.personalityTraits_label = self.findChild(QtWidgets.QLabel, 'personalityTraits_label')
		self.ideals_label = self.findChild(QtWidgets.QLabel, 'ideals_label')
		self.bonds_label = self.findChild(QtWidgets.QLabel, 'bonds_label')
		self.flaws_label = self.findChild(QtWidgets.QLabel, 'flaws_label')
		self.equipment_label = self.findChild(QtWidgets.QLabel, 'equipment_label')
		self.FeaturesAndTraits_label = self.findChild(QtWidgets.QLabel, 'FeaturesAndTraits_label')
		self.physicalAppearence_label = self.findChild(QtWidgets.QLabel, 'physicalAppearence_label')
		self.feet_label = self.findChild(QtWidgets.QLabel, 'feet_label')
		self.inches_label = self.findChild(QtWidgets.QLabel, 'inches_label')
		self.pounds_label = self.findChild(QtWidgets.QLabel, 'pounds_label')
		self.eyes_label = self.findChild(QtWidgets.QLabel, 'eyes_label')
		self.hair_label = self.findChild(QtWidgets.QLabel, 'hair_label')
		self.miscPhysicalAppearenceNotes_label = self.findChild(QtWidgets.QLabel, 'miscPhysicalAppearenceNotes_label')
		self.age_label = self.findChild(QtWidgets.QLabel, 'age_label')
		self.weight_label = self.findChild(QtWidgets.QLabel, 'weight_label')
		self.height_label = self.findChild(QtWidgets.QLabel, 'height_label')
		self.treasureAndMagicItems_label = self.findChild(QtWidgets.QLabel, 'treasureAndMagicItems_label')
		self.miscNotesLabel = self.findChild(QtWidgets.QLabel, 'miscNotesLabel')
		self.characterBackstory_label = self.findChild(QtWidgets.QLabel, 'characterBackstory_label')
		self.allieandOrganizations_label = self.findChild(QtWidgets.QLabel, 'allieandOrganizations_label')
		self.lore_label = self.findChild(QtWidgets.QLabel, 'lore_label')
		self.spellcasting_label = self.findChild(QtWidgets.QLabel, 'spellcasting_label')
		self.spellAbilityValue_label = self.findChild(QtWidgets.QLabel, 'spellAbilityValue_label')
		self.spellSaveDC_label = self.findChild(QtWidgets.QLabel, 'spellSaveDC_label')
		self.spellAbility_label = self.findChild(QtWidgets.QLabel, 'spellAbility_label')
		self.spellAttackBonus_label = self.findChild(QtWidgets.QLabel, 'spellAttackBonus_label')
		self.spellSaveDCValue_label = self.findChild(QtWidgets.QLabel, 'spellSaveDCValue_label')
		self.spellAttackBonusValue_label = self.findChild(QtWidgets.QLabel, 'spellAttackBonusValue_label')
		self.spellScrollSpacer = self.findChild(QtWidgets.QLabel, 'spellScrollSpacer')

		#line edit areas
		self.race_entry = self.findChild(QtWidgets.QLineEdit, 'race_entry')
		self.characterName_entry = self.findChild(QtWidgets.QLineEdit, 'characterName_entry')
		self.background_entry = self.findChild(QtWidgets.QLineEdit, 'background_entry')
		self.playerName_entry = self.findChild(QtWidgets.QLineEdit, 'playerName_entry')
		self.class_entry = self.findChild(QtWidgets.QLineEdit, 'class_entry')
		self.armorType_label = self.findChild(QtWidgets.QLineEdit, 'armorType_label')

		#combo boxes (dropdown menues)
		self.alignment_entry = self.findChild(QtWidgets.QComboBox, 'alignment_entry')
		self.addType_entry = self.findChild(QtWidgets.QComboBox, 'addType_entry')
		self.removeType_entry = self.findChild(QtWidgets.QComboBox, 'removeType_entry')
		#self.spellAbilityType_entry = self.findChild(QtWidgets.QComboBox, 'spellAbilityType_entry')

		openDropdownShadow = QtWidgets.QGraphicsDropShadowEffect()
		openDropdownShadow.setBlurRadius(20)
		openDropdownShadow.setOffset(1)
		openDropdownShadow.setColor(QtGui.QColor(43, 43, 43, 120))
		self.openCharacter_comboBox = self.findChild(QtWidgets.QComboBox, 'openCharacter_comboBox')
		#self.openCharacter_comboBox.setGraphicsEffect(openDropdownShadow)


		#scroll areas
		self.scrollArea = self.findChild(QtWidgets.QScrollArea, 'scrollArea')
		self.proficiencies_scrollArea = self.findChild(QtWidgets.QScrollArea, 'proficiencies_scrollArea')
		#self.spellArea = self.findChild(QtWidgets.QScrollArea, 'spellArea')

		#text edit areas
		self.language_textArea = self.findChild(QtWidgets.QTextEdit, 'language_textArea')
		self.misc_textArea = self.findChild(QtWidgets.QTextEdit, 'misc_textArea')
		self.toolsAndEquipment_textArea = self.findChild(QtWidgets.QTextEdit, 'toolsAndEquipment_textArea')
		self.weaponsAndArmor_textArea = self.findChild(QtWidgets.QTextEdit, 'weaponsAndArmor_textArea')
		self.personalityTraits_textEdit = self.findChild(QtWidgets.QTextEdit, 'personalityTraits_textEdit')
		self.ideals_textEdit = self.findChild(QtWidgets.QTextEdit, 'ideals_textEdit')
		self.bonds_textEdit = self.findChild(QtWidgets.QTextEdit, 'bonds_textEdit')
		self.flaws_textEdit = self.findChild(QtWidgets.QTextEdit, 'flaws_textEdit')
		self.equipment_textArea = self.findChild(QtWidgets.QTextEdit, 'equipment_textArea')
		self.FeaturesAndTraits_textArea = self.findChild(QtWidgets.QTextEdit, 'FeaturesAndTraits_textArea')
		self.alliesAndOrganizations_textArea = self.findChild(QtWidgets.QTextEdit, 'alliesAndOrganizations_textArea')
		self.miscNotes_textArea = self.findChild(QtWidgets.QTextEdit, 'miscNotes_textArea')
		self.characterBackstory_textArea = self.findChild(QtWidgets.QTextEdit, 'characterBackstory_textArea')
		self.addItemDescription = self.findChild(QtWidgets.QTextEdit, 'addItemDescription')
		self.magicItemsBox_textEdit = self.findChild(QtWidgets.QTextEdit, 'magicItemsBox_textEdit')
		self.weapons_textArea = self.findChild(QtWidgets.QTextEdit, 'weapons_textArea')

		self.inspiration_entry = self.findChild(QtWidgets.QCheckBox, 'inspiration_entry')

		
		for skill in skills:
			exec("""self.{skill}_checkBox = self.findChild(QtWidgets.QCheckBox, '{skill}_checkBox')""".format(skill=skill))
			exec("""self.{skill}Modifier_label = self.findChild(QtWidgets.QLabel, '{skill}Modifier_label')""".format(skill=skill))

		self.success_checkBox1 = self.findChild(QtWidgets.QCheckBox, 'success_checkBox1')
		self.success_checkBox2 = self.findChild(QtWidgets.QCheckBox, 'success_checkBox2')
		self.success_checkBox3 = self.findChild(QtWidgets.QCheckBox, 'success_checkBox3')
		self.fail_checkBox1 = self.findChild(QtWidgets.QCheckBox, 'fail_checkBox1')
		self.fail_checkBox3 = self.findChild(QtWidgets.QCheckBox, 'fail_checkBox3')
		self.fail_checkBox2 = self.findChild(QtWidgets.QCheckBox, 'fail_checkBox2')

		#frames:
		frameShadow = QtWidgets.QGraphicsDropShadowEffect()
		frameShadow.setBlurRadius(30)
		frameShadow.setOffset(2)
		frameShadow.setColor(QtGui.QColor(30, 30, 30, 160))
		self.frame = self.findChild(QtWidgets.QFrame, "frame")
		#self.frame.setGraphicsEffect(frameShadow)

		frameShadow13 = QtWidgets.QGraphicsDropShadowEffect()
		frameShadow13.setBlurRadius(30)
		frameShadow13.setOffset(2)
		frameShadow13.setColor(QtGui.QColor(30, 30, 30, 160))
		self.frame_13 = self.findChild(QtWidgets.QFrame, "frame_13")
		#self.frame_13.setGraphicsEffect(frameShadow13)

		self.statusBar().setStyleSheet("""background-color: white;
		font: MS Shell Dlg 2, 8pt;
		""")

		self.timer=QtCore.QTimer()
		self.timer.timeout.connect(self.looping)
		self.timer.start(10)

		#showing the GUI
		self.show()

		#all functions defined below Weapons tools armor languages death saves
	def passivePerception(self):
		self.passivePerception_entry.setText(str(10+wisdomMod))

	def uponStatChange(self):
		global statChange
		if statChange:
			self.weaponLoader()
			statChange=False

	def removingWeapon(self):
		numberToRemove = str(self.removeWeapon_entry.value())

		try:
			del pendingWeapon[int(numberToRemove)]
		except:
			print("Failure: error removing item")
			from PyQt5.QtWidgets import QMessageBox
			failure = QMessageBox()
			failure.resize(700,500)
			failure.setWindowTitle("Failure: Critical")
			failure.setText("Failure: error removing item")
			failure.setInformativeText('Check to see if you entered a valid number.')
			failure.setIcon(QMessageBox.Critical)
			failure.setStandardButtons(QMessageBox.Ok)
			failureReturnValue=failure.exec_()

		self.weaponLoader()

	def addingWeapon(self):
		weaponAdder.show()

	def removingMagicItem(self):
		numberToRemove = str(self.removeMagicItem_entry.value())

		try:
			del pendingMagicItem[int(numberToRemove)]
		except:
			print("Failure: error removing item")
			from PyQt5.QtWidgets import QMessageBox
			failure = QMessageBox()
			failure.resize(700,500)
			failure.setWindowTitle("Failure: Critical")
			failure.setText("Failure: error removing item")
			failure.setInformativeText('Check to see if you entered a valid number.')
			failure.setIcon(QMessageBox.Critical)
			failure.setStandardButtons(QMessageBox.Ok)
			failureReturnValue=failure.exec_()

		self.magicItemLoader()

	def weaponErrorChecker(self):
		global weaponRefresh
		global weaponCounter
		if weaponRefresh:
			def popup(text):
				print("Failure: "+text)
				from PyQt5.QtWidgets import QMessageBox
				failure = QMessageBox()
				failure.setWindowTitle("Failure: Critical")
				failure.setText(text)
				failure.setIcon(QMessageBox.Critical)
				failure.setStandardButtons(QMessageBox.Retry|QMessageBox.Cancel)
				failure.setDefaultButton(QMessageBox.Retry)
				failureReturnValue=failure.exec_()

				if failureReturnValue == QMessageBox.Cancel:
					failure.close()
					weaponAdder.close()
					weaponRefresh=False
					del pendingWeapon[str(weaponCounter-1)]
					return
				if failureReturnValue == QMessageBox.Retry:
					failure.close()
					weaponRefresh=False
					del pendingWeapon[str(weaponCounter-1)]
					return
			try:
				if len(pendingWeapon[str(weaponCounter-1)]['name']) <= 1:
					popup("Missing weapon name field.")
					weaponRefresh=False
					return
				else:
					self.weaponLoader()
			except:
				pass
		weaponRefresh=False

	def magicItemErrorChecker(self):
		global magicItemRefresh
		global magicItemCounter
		if magicItemRefresh:
			def popup(text):
				print("Failure: "+text)
				from PyQt5.QtWidgets import QMessageBox
				failure = QMessageBox()
				failure.setWindowTitle("Failure: Critical")
				failure.setText(text)
				failure.setIcon(QMessageBox.Critical)
				failure.setStandardButtons(QMessageBox.Retry|QMessageBox.Cancel)
				failure.setDefaultButton(QMessageBox.Retry)
				failureReturnValue=failure.exec_()

				if failureReturnValue == QMessageBox.Cancel:
					failure.close()
					magicItemAdder.close()
					magicItemRefresh=False
					del pendingMagicItem[str(magicItemCounter-1)]
					return
				if failureReturnValue == QMessageBox.Retry:
					failure.close()
					magicItemRefresh=False
					del pendingMagicItem[str(magicItemCounter-1)]
					return
			if len(json.dumps(pendingMagicItem)) < 5:
				return
			elif len(pendingMagicItem[str(magicItemCounter-1)]['name']) <= 1:
				popup("Missing name field.")
				magicItemRefresh=False
				return
			elif len(pendingMagicItem[str(magicItemCounter-1)]['description']) <= 1:
				popup("Missing description field.")
				magicItemRefresh=False
				return
			else:
				self.magicItemLoader()
		magicItemRefresh=False

	def magicItemLoader(self):
		y=1
		global pendingMagicItem
		for magicItemNumber,magicItemDict in pendingMagicItem.items():
			if magicItemNumber != y:
				temp = {}
				y=1
				for magicItemNumber,magicItemDict in pendingMagicItem.items():
					temp[y] = magicItemDict
					y+=1
				del pendingMagicItem
				pendingMagicItem = {}
				pendingMagicItem = temp
				del temp
			y+=1

		temp=""
		for magicItemNumber,magicItemDict in pendingMagicItem.items():

			if magicItemDict['attunement'] == 1:
				filler = " (requires attunement)</em></h4>\n"
			else:
				filler = "</em></h4>\n"

			temp += """<html><body><h2>#{number} {name}</h2>\n<hr />\n<h4>{type}.&nbsp;<em>{rarity}{filler}<p>{description}</p>
		\n<br><br></body></html>\n""".format(
			type=magicItemDict['type'],
			rarity=magicItemDict['rarity'],
			name=magicItemDict['name'],
			number=str(magicItemNumber),
			filler=filler,
			description=magicItemDict['description'].replace("\n","<br>"))

		self.magicItemsBox_textEdit = self.findChild(QtWidgets.QTextEdit, 'magicItemsBox_textEdit')

		magicItemAdder.close()

		self.magicItemsBox_textEdit.setHtml(str(temp))
		del temp

	def weaponLoader(self):
		y=1
		global pendingWeapon
		for weaponNumber,weaponDict in pendingWeapon.items():
			if weaponNumber != y:
				temp = {}
				y=1
				for weaponNumber,magicItemDict in pendingWeapon.items():
					temp[y] = magicItemDict
					y+=1
				del pendingWeapon
				pendingWeapon = {}
				pendingWeapon = temp
				del temp
			y+=1

		temp=""

		for weaponNumber,weaponDict in pendingWeapon.items():
			if weaponDict['abilityModifier'] == 'Strength':
				if weaponDict['proficient'] == 1:
					hitModifier = strengthMod+proficiencyVal
				else:
					hitModifier = strengthMod

			if weaponDict['abilityModifier'] == 'Dexterity':
				if weaponDict['proficient'] == 1:
					hitModifier = dexterityMod+proficiencyVal
				else:
					hitModifier = dexterityMod

			if weaponDict['abilityModifier'] == 'Constitution':
				if weaponDict['proficient'] == 1:
					hitModifier = constitutionMod+proficiencyVal
				else:
					hitModifier = constitutionMod

			if weaponDict['abilityModifier'] == 'Intelligence':
				if weaponDict['proficient'] == 1:
					hitModifier = intelligenceMod+proficiencyVal
				else:
					hitModifier = intelligenceMod

			if weaponDict['abilityModifier'] == 'Wisdom':
				if weaponDict['proficient'] == 1:
					hitModifier = wisdomMod+proficiencyVal
				else:
					hitModifier = wisdomMod

			if weaponDict['abilityModifier'] == 'Charisma':
				if weaponDict['proficient'] == 1:
					hitModifier = charismaMod+proficiencyVal
				else:
					hitModifier = charismaMod

			propertiesString = ""

			if weaponDict['ammunition'] == 1:
				propertiesString += "ammunition, "
			if weaponDict['finesse'] == 1:
				propertiesString += "finesse, "
			if weaponDict['heavy'] == 1:
				propertiesString += "heavy, "
			if weaponDict['light'] == 1:
				propertiesString += "light, "
			if weaponDict['loading'] == 1:
				propertiesString += "loading, "
			if weaponDict['range'] == 1:
				propertiesString += "range, "
			if weaponDict['reach'] == 1:
				propertiesString += "reach, "
			if weaponDict['special'] == 1:
				propertiesString += "special, "
			if weaponDict['thrown'] == 1:
				propertiesString += "thrown, "
			if weaponDict['twoHanded'] == 1:
				propertiesString += "two handed, "
			if weaponDict['versatile'] == 1:
				propertiesString += "versatile, "

			try:
				propertiesString=(propertiesString[0].upper()+propertiesString[1:])
			except:
				propertiesString=""
			try:
				propertiesString=propertiesString[:-2]
			except:
				pass

			propertiesList = propertiesString.split(" ")
			propertiesString=""
			propertiesList[0]=propertiesList[0].title()
			for property_ in propertiesList:
				propertiesString+=(" "+property_)

			temp += """<span style="font-family:'rockwell'; font-size:10pt"><p>{name} (+{hitModifier} to hit)
			{numberOfDice}D{typeOfDice} {damageType}.  &nbsp;<em>{propertiesString}</em></p></span>
			<span style="font-family:'rockwell'; font-size:7pt"><p>{description}</p></span><hr>""".format(
			name=weaponDict['name'].title(),
			hitModifier=hitModifier,
			numberOfDice=weaponDict['numberOfDice'],
			typeOfDice=weaponDict['typeOfDice'],
			damageType=weaponDict['damageType'],
			propertiesString=propertiesString,
			description=weaponDict['description']
			)

		self.weapons_textArea = self.findChild(QtWidgets.QTextEdit, 'weapons_textArea')
		self.weapons_textArea.setHtml(str(temp))
		weaponAdder.close()
		del temp

	def addMagicItem(self):
		magicItemAdder.show()

	def deathSavesUpTo(self):
		if self.success_checkBox2.isChecked():
			self.success_checkBox1.setChecked(True)
		if self.success_checkBox3.isChecked():
			self.success_checkBox2.setChecked(True)
		if self.fail_checkBox2.isChecked():
			self.fail_checkBox1.setChecked(True)
		if self.fail_checkBox3.isChecked():
			self.fail_checkBox2.setChecked(True)

	def addCurrency(self):
		typeToAdd = self.addType_entry.currentText()
		amountToAdd = self.add_entry.value()

		if typeToAdd == "CP":
			self.cp_entry.setValue(self.cp_entry.value()+amountToAdd)
		elif typeToAdd == "SP":
			self.sp_entry.setValue(self.sp_entry.value()+amountToAdd)
		elif typeToAdd == "EP":
			self.ep_entry.setValue(self.ep_entry.value()+amountToAdd)
		elif typeToAdd == "GP":
			self.gp_entry.setValue(self.gp_entry.value()+amountToAdd)
		elif typeToAdd == "PP":
			self.pp_entry.setValue(self.pp_entry.value()+amountToAdd)

	def removeCurrency(self):
		typeToAdd = self.removeType_entry.currentText()
		amountToRemove = self.remove_entry.value()

		if typeToAdd == "CP":
			self.cp_entry.setValue(self.cp_entry.value()-amountToRemove)
		elif typeToAdd == "SP":
			self.sp_entry.setValue(self.sp_entry.value()-amountToRemove)
		elif typeToAdd == "EP":
			self.ep_entry.setValue(self.ep_entry.value()-amountToRemove)
		elif typeToAdd == "GP":
			self.gp_entry.setValue(self.gp_entry.value()-amountToRemove)
		elif typeToAdd == "PP":
			self.pp_entry.setValue(self.pp_entry.value()-amountToRemove)
	
	def statToModifierInt(self,stat):
		try:
			stat = int(stat)
		except:
			stat = 10
		return int((stat-10)/2)

	def makeVars(self):
		global strengthMod
		global dexterityMod
		global constitutionMod
		global intelligenceMod
		global wisdomMod
		global charismaMod
		global proficiencyVal
		global times
		global statChange

		if times:
			oldStrengthMod=strengthMod
			oldDexterityMod=dexterityMod
			oldConstitutionMod=constitutionMod
			oldIntelligenceMod=intelligenceMod
			oldWisdomMod=wisdomMod
			oldCharismaMod=charismaMod
			oldProficiencyVal=proficiencyVal

		strengthMod = self.statToModifierInt(self.strength_entry.value())
		dexterityMod = self.statToModifierInt(self.dexterity_entry.value())
		constitutionMod = self.statToModifierInt(self.constitution_entry.value())
		intelligenceMod = self.statToModifierInt(self.intelligence_entry.value())
		wisdomMod = self.statToModifierInt(self.wisdom_entry.value())
		charismaMod = self.statToModifierInt(self.charisma_entry.value())
		proficiencyVal = self.proficiencyBonus_entry.value()

		if times:
			if oldStrengthMod != strengthMod:
				statChange = True
			if oldDexterityMod != dexterityMod:
				statChange = True
			if oldConstitutionMod != constitutionMod:
				statChange = True
			if oldIntelligenceMod != intelligenceMod:
				statChange = True
			if oldWisdomMod != wisdomMod:
				statChange = True
			if oldCharismaMod != charismaMod:
				statChange = True
			if oldProficiencyVal != proficiencyVal:
				statChange = True

		times = True

	def addPlus(self,arg):
		arg=str(arg)
		if "-" in str(arg):
			return str(arg)
		else:
			return "+"+str(arg)

	def modifiers(self):
		self.strength_modifier.setText(self.addPlus(strengthMod))
		self.dexterity_modifier.setText(self.addPlus(dexterityMod))
		self.constitution_modifier.setText(self.addPlus(constitutionMod))
		self.intelligence_modifier.setText(self.addPlus(intelligenceMod))
		self.wisdom_modifier.setText(self.addPlus(wisdomMod))
		self.charisma_modifier.setText(self.addPlus(charismaMod))

	def spellcasterOrNot(self):
		if self.spellcaster_toggleButton.isChecked():
			self.spellArea.show()
		else:
			self.spellArea.hide()

	def spellcalcs(self): ###SPELLING!! dextErity
		temp = self.spellAbilityType_entry.currentText()
		if temp == "Strength":
			self.spellAbilityValue_label.setText(self.addPlus(strengthMod))
			self.spellSaveDCValue_label.setText("DC"+str(8+strengthMod+proficiencyVal))
			self.spellAttackBonusValue_label.setText("+"+str(strengthMod+proficiencyVal))
		elif temp == "Dextarity":
			self.spellAbilityValue_label.setText(self.addPlus(dexterityMod))
			self.spellSaveDCValue_label.setText("DC "+str(8+dexterityMod+proficiencyVal))
			self.spellAttackBonusValue_label.setText("+"+str(dexterityMod+proficiencyVal))
		elif temp == "Constitution":
			self.spellAbilityValue_label.setText(self.addPlus(constitutionMod))
			self.spellSaveDCValue_label.setText("DC "+str(8+constitutionMod+proficiencyVal))
			self.spellAttackBonusValue_label.setText("+"+str(constitutionMod+proficiencyVal))
		elif temp == "Intelligence":
			self.spellAbilityValue_label.setText(self.addPlus(intelligenceMod))
			self.spellSaveDCValue_label.setText("DC "+str(8+intelligenceMod+proficiencyVal))
			self.spellAttackBonusValue_label.setText("+"+str(intelligenceMod+proficiencyVal))
		elif temp == "Wisdom":
			self.spellAbilityValue_label.setText(self.addPlus(wisdomMod))
			self.spellSaveDCValue_label.setText("DC "+str(8+wisdomMod+proficiencyVal))
			self.spellAttackBonusValue_label.setText("+"+str(wisdomMod+proficiencyVal))
		elif temp == "Charisma":
			self.spellAbilityValue_label.setText(self.addPlus(charismaMod))
			self.spellSaveDCValue_label.setText("DC "+str(8+charismaMod+proficiencyVal))
			self.spellAttackBonusValue_label.setText("+"+str(charismaMod+proficiencyVal))

	def saves(self):
		prof = int(self.proficiencyBonus_entry.text())

		if self.strengthSave_checkBox.isChecked():
			self.strengthSaveModifier_label.setText(self.addPlus(strengthMod+proficiencyVal))
		else:
			self.strengthSaveModifier_label.setText(self.addPlus(strengthMod))

		if self.dexteritySave_checkBox.isChecked():
			self.dexteritySaveModifier_label.setText(self.addPlus(dexterityMod+proficiencyVal))
		else:
			self.dexteritySaveModifier_label.setText(self.addPlus(dexterityMod))

		if self.constitutionSave_checkBox.isChecked():
			self.constitutionSaveModifier_label.setText(self.addPlus(constitutionMod+proficiencyVal))
		else:
			self.constitutionSaveModifier_label.setText(self.addPlus(constitutionMod))

		if self.intelligenceSave_checkBox.isChecked():
			self.intelligenceSaveModifier_label.setText(self.addPlus(intelligenceMod+proficiencyVal))
		else:
			self.intelligenceSaveModifier_label.setText(self.addPlus(intelligenceMod))

		if self.wisdomSave_checkBox.isChecked():
			self.wisdomSaveModifier_label.setText(self.addPlus(wisdomMod+proficiencyVal))
		else:
			self.wisdomSaveModifier_label.setText(self.addPlus(wisdomMod))

		if self.charismaSave_checkBox.isChecked():
			self.charismaSaveModifier_label.setText(self.addPlus(charismaMod+proficiencyVal))
		else:
			self.charismaSaveModifier_label.setText(self.addPlus(charismaMod))

	def setInitiative(self):
		temp=dexterityMod
		temp+=self.initiativeBoost_entry.value()
		temp=self.addPlus(temp)
		self.initiativeScore_label.setText(temp)

	def setHitDice(self):
		self.numberOfHitDice_label.setText(self.level_entry.text())

	def setSkillModifiers(self):
		if self.acrobatics_checkBox.isChecked():
			self.acrobaticsModifier_label.setText(self.addPlus(dexterityMod+proficiencyVal))
		else:
			self.acrobaticsModifier_label.setText(self.addPlus(dexterityMod))

		if self.animalHandling_checkBox.isChecked():
			self.animalHandlingModifier_label.setText(self.addPlus(wisdomMod+proficiencyVal))
		else:
			self.animalHandlingModifier_label.setText(self.addPlus(wisdomMod))

		if self.arcana_checkBox.isChecked():
			self.arcanaModifier_label.setText(self.addPlus(intelligenceMod+proficiencyVal))
		else:
			self.arcanaModifier_label.setText(self.addPlus(intelligenceMod))

		if self.athletics_checkBox.isChecked():
			self.athleticsModifier_label.setText(self.addPlus(strengthMod+proficiencyVal))
		else:
			self.athleticsModifier_label.setText(self.addPlus(strengthMod))

		if self.deception_checkBox.isChecked():
			self.deceptionModifier_label.setText(self.addPlus(charismaMod+proficiencyVal))
		else:
			self.deceptionModifier_label.setText(self.addPlus(charismaMod))

		if self.history_checkBox.isChecked():
			self.historyModifier_label.setText(self.addPlus(intelligenceMod+proficiencyVal))
		else:
			self.historyModifier_label.setText(self.addPlus(intelligenceMod))

		if self.insight_checkBox.isChecked():
			self.insightModifier_label.setText(self.addPlus(wisdomMod+proficiencyVal))
		else:
			self.insightModifier_label.setText(self.addPlus(wisdomMod))

		if self.intimidation_checkBox.isChecked():
			self.intimidationModifier_label.setText(self.addPlus(charismaMod+proficiencyVal))
		else:
			self.intimidationModifier_label.setText(self.addPlus(charismaMod))

		if self.investigation_checkBox.isChecked():
			self.investigationModifier_label.setText(self.addPlus(intelligenceMod+proficiencyVal))
		else:
			self.investigationModifier_label.setText(self.addPlus(intelligenceMod))

		if self.medicine_checkBox.isChecked():
			self.medicineModifier_label.setText(self.addPlus(wisdomMod+proficiencyVal))
		else:
			self.medicineModifier_label.setText(self.addPlus(wisdomMod))

		if self.nature_checkBox.isChecked():
			self.natureModifier_label.setText(self.addPlus(intelligenceMod+proficiencyVal))
		else:
			self.natureModifier_label.setText(self.addPlus(intelligenceMod))

		if self.perception_checkBox.isChecked():
			self.perceptionModifier_label.setText(self.addPlus(wisdomMod+proficiencyVal))
		else:
			self.perceptionModifier_label.setText(self.addPlus(wisdomMod))

		if self.performance_checkBox.isChecked():
			self.performanceModifier_label.setText(self.addPlus(charismaMod+proficiencyVal))
		else:
			self.performanceModifier_label.setText(self.addPlus(charismaMod))

		if self.persuasion_checkBox.isChecked():
			self.persuasionModifier_label.setText(self.addPlus(charismaMod+proficiencyVal))
		else:
			self.persuasionModifier_label.setText(self.addPlus(charismaMod))

		if self.religion_checkBox.isChecked():
			self.religionModifier_label.setText(self.addPlus(intelligenceMod+proficiencyVal))
		else:
			self.religionModifier_label.setText(self.addPlus(intelligenceMod))

		if self.sleightOfHand_checkBox.isChecked():
			self.sleightOfHandModifier_label.setText(self.addPlus(dexterityMod+proficiencyVal))
		else:
			self.sleightOfHandModifier_label.setText(self.addPlus(dexterityMod))

		if self.stealth_checkBox.isChecked():
			self.stealthModifier_label.setText(self.addPlus(dexterityMod+proficiencyVal))
		else:
			self.stealthModifier_label.setText(self.addPlus(dexterityMod))

		if self.survival_checkBox.isChecked():
			self.survivalModifier_label.setText(self.addPlus(wisdomMod+proficiencyVal))
		else:
			self.survivalModifier_label.setText(self.addPlus(wisdomMod))

	def removeCharacter(self):
		if self.sheetName_label.text() != "New Sheet":
			send2trash(".\\saves\\"+self.sheetName_label.text()+".json")
			global loadTemplate
			loadTemplate = True
			self.loadSheet()
			loadTemplate = False
			self.sheetName_label.setText("New Sheet")
			self.loadSheetList()

	def loadSheetList(self):
		self.openCharacter_comboBox.clear()
		sheets = os.listdir("./saves")
		sheets.remove("template.json")
		for sheet in sheets:
			sheets[sheets.index(sheet)] = sheet[:-5].title().replace("_"," ")
		self.openCharacter_comboBox.addItems(sheets)
		del sheets
		global firstRun
		if firstRun:
			self.sheetName_label.setText("New Sheet")
			firstRun = False

	def loadSheet(self):
		global loadTemplate
		if not loadTemplate:
			sheetName = self.openCharacter_comboBox.currentText()
			self.sheetName_label.setText(sheetName)
			with open("./saves/"+sheetName+".json") as loadedSheetFile:
				loadedSheet = json.load(loadedSheetFile)

			with open("config.json") as configFile:
				config = json.load(configFile)
				config["lastSheet"] = str(sheetName)
			with open("config.json","w") as configFile:
				json.dump(config,configFile,indent=4)
		else:
			sheetName = self.openCharacter_comboBox.currentText()
			self.sheetName_label.setText("New Sheet")
			with open("./saves/template.json") as loadedSheetFile:
				loadedSheet = json.load(loadedSheetFile)

		def toBool(binary):
			if binary == 1:
				return True
			else:
				return False

		self.characterName_entry.setText(loadedSheet["characterName"])
		self.playerName_entry.setText(loadedSheet["playerName"])
		self.alignment_entry.setCurrentText(loadedSheet["alignment"])
		self.class_entry.setText(loadedSheet["class"])
		self.race_entry.setText(loadedSheet["race"])
		self.background_entry.setText(loadedSheet["background"])
		self.level_entry.setValue(loadedSheet["level"])
		self.XP_entry.setValue(loadedSheet["XP"])

		self.FeaturesAndTraits_textArea.setPlainText(loadedSheet["featuresAndTraits"])

		self.strength_entry.setValue(loadedSheet["stats"]["strength"]["score"])		
		self.strengthSave_checkBox.setChecked(toBool(loadedSheet["stats"]["strength"]["save"]))

		self.dexterity_entry.setValue(loadedSheet["stats"]["dexterity"]["score"])
		self.dexteritySave_checkBox.setChecked(toBool(loadedSheet["stats"]["dexterity"]["save"]))

		self.constitution_entry.setValue(loadedSheet["stats"]["constitution"]["score"])
		self.constitutionSave_checkBox.setChecked(toBool(loadedSheet["stats"]["constitution"]["save"]))

		self.intelligence_entry.setValue(loadedSheet["stats"]["intelligence"]["score"])
		self.intelligenceSave_checkBox.setChecked(toBool(loadedSheet["stats"]["intelligence"]["save"]))

		self.wisdom_entry.setValue(loadedSheet["stats"]["wisdom"]["score"])
		self.wisdomSave_checkBox.setChecked(toBool(loadedSheet["stats"]["wisdom"]["save"]))

		self.charisma_entry.setValue(loadedSheet["stats"]["charisma"]["score"])
		self.charismaSave_checkBox.setChecked(toBool(loadedSheet["stats"]["charisma"]["save"]))

		global skills

		for skill in skills:
			exec("""self.{skill}_checkBox.setChecked(toBool(loadedSheet["skills"]["{skill}"]["proficiency"]))\nself.{skill}Boost_entry.setValue(loadedSheet["skills"]["{skill}"]["boost"])\n\n""".format(skill=skill))

		self.weaponsAndArmor_textArea.setPlainText(loadedSheet["proficiencies"]["weaponsAndArmor"])
		self.toolsAndEquipment_textArea.setPlainText(loadedSheet["proficiencies"]["toolsAndEquipment"])
		self.language_textArea.setPlainText(loadedSheet["proficiencies"]["languages"])
		self.misc_textArea_6.setPlainText(loadedSheet["proficiencies"]["misc"])

		self.armorType_entry.setText(loadedSheet["armor"]["armorType"])
		self.armorClass_entry.setValue(loadedSheet["armor"]["armorClass"])

		self.age_entry.setValue(loadedSheet["appearance"]["age"])
		self.heightFeet_entry.setValue(loadedSheet["appearance"]["height"]["feet"])
		self.heightInches_entry.setValue(loadedSheet["appearance"]["height"]["inches"])
		self.weightPounds_entry.setValue(loadedSheet["appearance"]["weight"])
		self.eyes_entry.setText(loadedSheet["appearance"]["eyes"])
		self.hair_entry.setText(loadedSheet["appearance"]["hair"])
		self.miscAppearence_entry.setText(loadedSheet["appearance"]["misc"])

		self.characterBackstory_textArea.setPlainText(loadedSheet["lore"]["characterBackstory"])
		self.alliesAndOrganizations_textArea.setPlainText(loadedSheet["lore"]["alliesAndOrganizations"])

		self.spellcaster_toggleButton.setChecked(toBool(loadedSheet["spellcasting"]["spellcaster"]))

		global spellSlots

		for level in spellSlots:
			exec(
				"""self.{spellSlot}.setText(loadedSheet["spellcasting"]["spellSlots"]["{spellSlot}"]["text"])\n""".format(
					spellSlot=level))
			exec(
				"""self.{checkbox}.setChecked(toBool(loadedSheet["spellcasting"]["spellSlots"]["{spellSlot}"]["prepared"]))\n""".format(
					spellSlot=level,checkbox=level.replace("entry","checkBox")))

		self.weaponsAndArmor_textArea.setText(loadedSheet["proficiencies"]["weaponsAndArmor"])
		self.toolsAndEquipment_textArea.setText(loadedSheet["proficiencies"]["toolsAndEquipment"])
		self.language_textArea.setText(loadedSheet["proficiencies"]["languages"])
		self.misc_textArea_6.setText(loadedSheet["proficiencies"]["misc"])

		self.cp_entry.setValue(loadedSheet["equipment"]["currency"]["CP"])
		self.sp_entry.setValue(loadedSheet["equipment"]["currency"]["SP"])
		self.ep_entry.setValue(loadedSheet["equipment"]["currency"]["EP"])
		self.gp_entry.setValue(loadedSheet["equipment"]["currency"]["GP"])
		self.pp_entry.setValue(loadedSheet["equipment"]["currency"]["PP"])

		self.equipment_textArea.setPlainText(loadedSheet["equipment"]["equipmentText"])
		self.FeaturesAndTraits_textArea.setPlainText(loadedSheet["featuresAndTraits"])

		if loadedSheet["deathSaves"]["fail"] == 0:
			self.fail_checkBox3.setChecked(False)
			self.fail_checkBox2.setChecked(False)
			self.fail_checkBox1.setChecked(False)
		elif loadedSheet["deathSaves"]["fail"] == 1:
			self.fail_checkBox3.setChecked(False)
			self.fail_checkBox2.setChecked(False)
			self.fail_checkBox1.setChecked(True)
		elif loadedSheet["deathSaves"]["fail"] == 2:
			self.fail_checkBox3.setChecked(False)
			self.fail_checkBox2.setChecked(True)
		elif loadedSheet["deathSaves"]["fail"] == 3:
			self.fail_checkBox3.setChecked(True)

		if loadedSheet["deathSaves"]["success"] == 0:
			self.success_checkBox1.setChecked(False)
			self.success_checkBox2.setChecked(False)
			self.success_checkBox1.setChecked(False)
		elif loadedSheet["deathSaves"]["success"] == 1:
			self.success_checkBox3.setChecked(False)
			self.success_checkBox2.setChecked(False)
			self.success_checkBox1.setChecked(True)
		elif loadedSheet["deathSaves"]["success"] == 2:
			self.success_checkBox3.setChecked(False)
			self.success_checkBox2.setChecked(True)
		elif loadedSheet["deathSaves"]["success"] == 3:
			self.success_checkBox3.setChecked(True)

		self.speed_entry.setValue(loadedSheet["speed"])

		global pendingMagicItem
		global magicItemCounter
		global magicItemRefresh
		pendingMagicItem = loadedSheet["magicItems"]
		magicItemCounter = loadedSheet["magicItemCounter"]
		magicItemRefresh = True

		global pendingWeapon
		global weaponCounter
		global weaponRefresh
		pendingWeapon = loadedSheet["weapons"]
		weaponCounter = loadedSheet["weaponCounter"]
		weaponRefresh = True

		self.miscNotes_textArea.setPlainText(loadedSheet["miscNotes"])

		self.spellAbilityType_entry.setCurrentText(loadedSheet["spellcasting"]["spellAbilityType"])

	def saveSheet(self):
		global sheetNameInput
		global doneSettingName
		if self.sheetName_label.text() == "New Sheet":
			saveSheet.show()
		else:
			sheetNameInput = self.sheetName_label.text()
			doneSettingName = True
		if not doneSettingName:
			print("failed to save")
			return
		with open("./saves/template.json") as templateFile:
				savingFile = json.load(templateFile)

		def toInt(bool_):
			if bool_:
				return 1
			else:
				return 0

		savingFile["characterName"] = self.characterName_entry.text()
		savingFile["playerName"] = self.playerName_entry.text()
		savingFile["alignment"] = self.alignment_entry.currentText()
		savingFile["class"] = self.class_entry.text()
		savingFile["race"] = self.race_entry.text()
		savingFile["background"] = self.background_entry.text()
		savingFile["level"] = self.level_entry.value()
		savingFile["XP"] = self.XP_entry.value()

		savingFile["proficiencyBonus"] = self.proficiencyBonus_entry.value()
		savingFile["inspiration"] = self.proficiencyBonus_entry.value()

		savingFile["spellcasting"]["spellcaster"] = toInt(self.spellcaster_toggleButton.isChecked())
		savingFile["spellcasting"]["spellAbilityType"] = self.spellAbilityType_entry.currentText()

		global spellSlots

		for level in spellSlots:
			exec("""self.{checkbox} = self.findChild(QtWidgets.QCheckBox, '{checkbox}')""".format(checkbox=level.replace("entry","checkbox")))
			exec("""savingFile["spellcasting"]["spellSlots"]["{level}"]["text"] = self.{level}.text()""".format(level=level))
			exec("""savingFile["spellcasting"]["spellSlots"]["{level}"]["prepared"] = toInt(self.{checkbox}.isChecked())""".format(level=level,checkbox=level.replace("entry","checkBox")))
		
		savingFile["armor"]["armorClass"] = self.armorClass_entry.value()
		savingFile["armor"]["armorType"] = self.armorType_entry.text()

		savingFile["hitPoints"]["max"] = self.maxHP_entry.text()
		savingFile["hitPoints"]["current"] = self.currentHP_entry.text()
		savingFile["hitPoints"]["temp"] = self.tempHP_entry.text()

		savingFile["initiativeBoost"] = self.initiativeBoost_entry.value()
		savingFile["hitDiceType"] = self.hitDiceType.value()
		savingFile["speed"] = self.speed_entry.value()

		if self.fail_checkBox3.isChecked():
			savingFile["deathSaves"]["fail"] = 3
		elif self.fail_checkBox2.isChecked():
			savingFile["deathSaves"]["fail"] = 2
		elif self.fail_checkBox1.isChecked():
			savingFile["deathSaves"]["fail"] = 1
		else:
			savingFile["deathSaves"]["fail"] = 0

		if self.success_checkBox3.isChecked():
			savingFile["deathSaves"]["success"] = 3
		elif self.success_checkBox2.isChecked():
			savingFile["deathSaves"]["success"] = 2
		elif self.success_checkBox1.isChecked():
			savingFile["deathSaves"]["success"] = 1
		else:
			savingFile["deathSaves"]["success"] = 0

		savingFile["equipment"]["equipmentText"] = self.equipment_textArea.toPlainText()
		savingFile["equipment"]["currency"]["CP"] = self.cp_entry.value()
		savingFile["equipment"]["currency"]["SP"] = self.sp_entry.value()
		savingFile["equipment"]["currency"]["EP"] = self.ep_entry.value()
		savingFile["equipment"]["currency"]["GP"] = self.gp_entry.value()
		savingFile["equipment"]["currency"]["PP"] = self.pp_entry.value()

		savingFile["magicItemCounter"] = magicItemCounter

		savingFile["magicItems"] = pendingMagicItem
		savingFile["magicItemCounter"] = magicItemCounter
		magicItemRefresh = True

		savingFile["weapons"] = pendingWeapon
		savingFile["weaponCounter"] = weaponCounter
		weaponRefresh = True

		savingFile["weaponCounter"] = weaponCounter

		savingFile["featuresAndTraits"] = self.FeaturesAndTraits_textArea.toPlainText()

		global skills

		for skill in skills:
			exec("""savingFile["skills"]["{skill}"]["proficiency"] = toInt(self.{skill}_checkBox.isChecked())""".format(skill=skill))
			exec("""savingFile["skills"]["{skill}"]["boost"] = self.{skill}Boost_entry.value()""".format(skill=skill))

		currentSheet = self.sheetName_label.text()+".json"
		with open(("./saves/"+sheetNameInput.lower().replace(" ","_")+".json"),"w") as loadedFile:
			json.dump(savingFile, loadedFile, indent=4)
		doneSettingName = True
		self.loadSheetList()

	def newCharacter(self):
		saveSheet.show()
		global loadTemplate
		loadTemplate = True
		self.loadSheet()
		loadTemplate = False

	def looping(self):
		self.makeVars()
		self.modifiers()
		self.saves()
		self.setHitDice()
		self.setInitiative()
		self.setSkillModifiers()
		self.spellcalcs()
		self.spellcasterOrNot()
		self.deathSavesUpTo()
		self.magicItemErrorChecker()
		self.weaponErrorChecker()
		self.uponStatChange()
		self.passivePerception()

	
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
mainWindow = mainWindow() # Create an instance of our class
magicItemAdder = magicItemAdder()
weaponAdder = weaponAdder()
saveSheet = saveSheet()
app.exec_() # Start the application