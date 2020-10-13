#Main Window Class


def __init__(self, parent=None): #basic setup
		super(mainWindow, self).__init__() # Call the inherited classes __init__ method
		try:
			uic.loadUi('./gui/'+guiStyle+"/mainWindow.ui", self) # Load the .ui file
		except:
			try:
				uic.loadUi('./gui/classic/mainWindow.ui', self)
			except:
				print("Failed to start")
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
		self.resize(950,600)
		self.setMinimumSize(940, 400)
		self.loadSheetList()

		with open("loadMainWindow.py", "rt") as loading: 
			#load the different elements of the main window ui, by loading a seperate py file that does such.
			exec(loading.read())

		#connect buttons to functions:
		self.spellcaster_toggleButton.clicked.connect(self.spellcasterOrNot)
		self.newCharacter_button.clicked.connect(self.newCharacter)
		self.add_button.clicked.connect(self.addCurrency)
		self.remove_button.clicked.connect(self.removeCurrency)
		self.removeWeapon_button.clicked.connect(self.removingWeapon)
		self.addMagicItem_button.clicked.connect(self.addMagicItem)
		self.removeMagicItem_button.clicked.connect(self.removingMagicItem)
		self.saveCharacter_button.clicked.connect(self.saveSheet)
		self.addWeapon_button.clicked.connect(self.addingWeapon)
		self.removeCharacter_button.clicked.connect(self.removeCharacter)
		self.openCharacter_button.clicked.connect(self.loadSheet)

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