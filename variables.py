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