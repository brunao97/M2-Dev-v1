import app
import ui
import player
import item
import uiToolTip
import net
import wndMgr
import messenger
import guild
import chr
import nonplayer
import localeInfo
import constInfo
from _weakref import proxy

if not hasattr(app, "ENABLE_SEND_TARGET_INFO"):
	app.ENABLE_SEND_TARGET_INFO = 0

# Target Information System - Fallback strings if not defined in localeInfo
if app.ENABLE_SEND_TARGET_INFO:
	# Import fallback strings
	try:
		import targetinfo_strings
		
		# Apply fallbacks for missing TARGET_INFO_* strings
		if not hasattr(localeInfo, "TARGET_INFO_MAX_HP"):
			localeInfo.TARGET_INFO_MAX_HP = targetinfo_strings.TARGET_INFO_MAX_HP
		if not hasattr(localeInfo, "TARGET_INFO_DAMAGE"):
			localeInfo.TARGET_INFO_DAMAGE = targetinfo_strings.TARGET_INFO_DAMAGE
		if not hasattr(localeInfo, "TARGET_INFO_EXP"):
			localeInfo.TARGET_INFO_EXP = targetinfo_strings.TARGET_INFO_EXP
		if not hasattr(localeInfo, "TARGET_INFO_MAINRACE"):
			localeInfo.TARGET_INFO_MAINRACE = targetinfo_strings.TARGET_INFO_MAINRACE
		if not hasattr(localeInfo, "TARGET_INFO_SUBRACE"):
			localeInfo.TARGET_INFO_SUBRACE = targetinfo_strings.TARGET_INFO_SUBRACE
		if not hasattr(localeInfo, "TARGET_INFO_NO_RACE"):
			localeInfo.TARGET_INFO_NO_RACE = targetinfo_strings.TARGET_INFO_NO_RACE
		if not hasattr(localeInfo, "TARGET_INFO_NO_ITEM_TEXT"):
			localeInfo.TARGET_INFO_NO_ITEM_TEXT = targetinfo_strings.TARGET_INFO_NO_ITEM_TEXT
		if not hasattr(localeInfo, "TARGET_INFO_STONE_NAME"):
			localeInfo.TARGET_INFO_STONE_NAME = targetinfo_strings.TARGET_INFO_STONE_NAME
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ANIMAL"):
			localeInfo.TARGET_INFO_RACE_ANIMAL = targetinfo_strings.TARGET_INFO_RACE_ANIMAL
		if not hasattr(localeInfo, "TARGET_INFO_RACE_UNDEAD"):
			localeInfo.TARGET_INFO_RACE_UNDEAD = targetinfo_strings.TARGET_INFO_RACE_UNDEAD
		if not hasattr(localeInfo, "TARGET_INFO_RACE_DEVIL"):
			localeInfo.TARGET_INFO_RACE_DEVIL = targetinfo_strings.TARGET_INFO_RACE_DEVIL
		if not hasattr(localeInfo, "TARGET_INFO_RACE_HUMAN"):
			localeInfo.TARGET_INFO_RACE_HUMAN = targetinfo_strings.TARGET_INFO_RACE_HUMAN
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ORC"):
			localeInfo.TARGET_INFO_RACE_ORC = targetinfo_strings.TARGET_INFO_RACE_ORC
		if not hasattr(localeInfo, "TARGET_INFO_RACE_MILGYO"):
			localeInfo.TARGET_INFO_RACE_MILGYO = targetinfo_strings.TARGET_INFO_RACE_MILGYO
		if not hasattr(localeInfo, "TARGET_INFO_RACE_METIN"):
			localeInfo.TARGET_INFO_RACE_METIN = targetinfo_strings.TARGET_INFO_RACE_METIN
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ELEC"):
			localeInfo.TARGET_INFO_RACE_ELEC = targetinfo_strings.TARGET_INFO_RACE_ELEC
		if not hasattr(localeInfo, "TARGET_INFO_RACE_FIRE"):
			localeInfo.TARGET_INFO_RACE_FIRE = targetinfo_strings.TARGET_INFO_RACE_FIRE
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ICE"):
			localeInfo.TARGET_INFO_RACE_ICE = targetinfo_strings.TARGET_INFO_RACE_ICE
		if not hasattr(localeInfo, "TARGET_INFO_RACE_WIND"):
			localeInfo.TARGET_INFO_RACE_WIND = targetinfo_strings.TARGET_INFO_RACE_WIND
		if not hasattr(localeInfo, "TARGET_INFO_RACE_EARTH"):
			localeInfo.TARGET_INFO_RACE_EARTH = targetinfo_strings.TARGET_INFO_RACE_EARTH
		if not hasattr(localeInfo, "TARGET_INFO_RACE_DARK"):
			localeInfo.TARGET_INFO_RACE_DARK = targetinfo_strings.TARGET_INFO_RACE_DARK
	except ImportError:
		# Hardcoded fallbacks if targetinfo_strings.py is not available
		if not hasattr(localeInfo, "TARGET_INFO_MAX_HP"):
			localeInfo.TARGET_INFO_MAX_HP = "Max HP: %s"
		if not hasattr(localeInfo, "TARGET_INFO_DAMAGE"):
			localeInfo.TARGET_INFO_DAMAGE = "Damage: %s - %s"
		if not hasattr(localeInfo, "TARGET_INFO_EXP"):
			localeInfo.TARGET_INFO_EXP = "Experience: %s"
		if not hasattr(localeInfo, "TARGET_INFO_MAINRACE"):
			localeInfo.TARGET_INFO_MAINRACE = "Race: %s"
		if not hasattr(localeInfo, "TARGET_INFO_SUBRACE"):
			localeInfo.TARGET_INFO_SUBRACE = "Subspecies: %s"
		if not hasattr(localeInfo, "TARGET_INFO_NO_RACE"):
			localeInfo.TARGET_INFO_NO_RACE = "None"
		if not hasattr(localeInfo, "TARGET_INFO_NO_ITEM_TEXT"):
			localeInfo.TARGET_INFO_NO_ITEM_TEXT = "No items droppable."
		if not hasattr(localeInfo, "TARGET_INFO_STONE_NAME"):
			localeInfo.TARGET_INFO_STONE_NAME = "Ghoststone"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ANIMAL"):
			localeInfo.TARGET_INFO_RACE_ANIMAL = "Animal"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_UNDEAD"):
			localeInfo.TARGET_INFO_RACE_UNDEAD = "Undead"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_DEVIL"):
			localeInfo.TARGET_INFO_RACE_DEVIL = "Devil"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_HUMAN"):
			localeInfo.TARGET_INFO_RACE_HUMAN = "Half Human"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ORC"):
			localeInfo.TARGET_INFO_RACE_ORC = "Orcs"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_MILGYO"):
			localeInfo.TARGET_INFO_RACE_MILGYO = "Mystic"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_METIN"):
			localeInfo.TARGET_INFO_RACE_METIN = "Stone"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ELEC"):
			localeInfo.TARGET_INFO_RACE_ELEC = "Lightning"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_FIRE"):
			localeInfo.TARGET_INFO_RACE_FIRE = "Fire"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_ICE"):
			localeInfo.TARGET_INFO_RACE_ICE = "Ice"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_WIND"):
			localeInfo.TARGET_INFO_RACE_WIND = "Wind"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_EARTH"):
			localeInfo.TARGET_INFO_RACE_EARTH = "Earth"
		if not hasattr(localeInfo, "TARGET_INFO_RACE_DARK"):
			localeInfo.TARGET_INFO_RACE_DARK = "Darkness"

if app.ENABLE_SEND_TARGET_INFO:
	def HAS_FLAG(value, flag):
		return (value & flag) == flag

class TargetBoard(ui.ThinBoard):

	BUTTON_NAME_LIST = ( 
		localeInfo.TARGET_BUTTON_WHISPER, 
		localeInfo.TARGET_BUTTON_EXCHANGE, 
		localeInfo.TARGET_BUTTON_FIGHT, 
		localeInfo.TARGET_BUTTON_ACCEPT_FIGHT, 
		localeInfo.TARGET_BUTTON_AVENGE, 
		localeInfo.TARGET_BUTTON_FRIEND, 
		localeInfo.TARGET_BUTTON_INVITE_PARTY, 
		localeInfo.TARGET_BUTTON_LEAVE_PARTY, 
		localeInfo.TARGET_BUTTON_EXCLUDE, 
		localeInfo.TARGET_BUTTON_INVITE_GUILD,
		localeInfo.TARGET_BUTTON_DISMOUNT,
		localeInfo.TARGET_BUTTON_EXIT_OBSERVER,
		localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT,
		localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY,
		localeInfo.TARGET_BUTTON_BUILDING_DESTROY,
		localeInfo.TARGET_BUTTON_EMOTION_ALLOW,
		"VOTE_BLOCK_CHAT",
	)

	GRADE_NAME =	{
						nonplayer.PAWN : localeInfo.TARGET_LEVEL_PAWN,
						nonplayer.S_PAWN : localeInfo.TARGET_LEVEL_S_PAWN,
						nonplayer.KNIGHT : localeInfo.TARGET_LEVEL_KNIGHT,
						nonplayer.S_KNIGHT : localeInfo.TARGET_LEVEL_S_KNIGHT,
						nonplayer.BOSS : localeInfo.TARGET_LEVEL_BOSS,
						nonplayer.KING : localeInfo.TARGET_LEVEL_KING,
					}
	EXCHANGE_LIMIT_RANGE = 3000

	if app.ENABLE_SEND_TARGET_INFO:
		class InfoBoard(ui.ThinBoard):
			class TargetListBox(ui.ListBoxExNew):
				def OnRunMouseWheel(self, nLen):
					if self.scrollBar:
						if self.scrollBar.IsShow():
							if nLen > 0:
								self.scrollBar.OnUp()
							else:
								self.scrollBar.OnDown()
							return True
					return False
				
				OnMouseWheel = OnRunMouseWheel

			class ItemListBoxItem(ui.ListBoxExNew.Item):
				def __init__(self, width):
					ui.ListBoxExNew.Item.__init__(self)
					self.SetWindowName("ItemListBoxItem")
					self.parent = None

					image = ui.ExpandedImageBox()
					image.SetParent(self)
					image.AddFlag("not_pick")
					image.Show()
					self.image = image

					nameLine = ui.TextLine()
					nameLine.SetParent(self)
					nameLine.SetPosition(32 + 5, 0)
					nameLine.AddFlag("not_pick")
					nameLine.Show()
					self.nameLine = nameLine

					self.overInEvent = None
					self.overOutEvent = None
					self.overInArgs = None
					self.overOutArgs = None

					self.SetSize(width, 32 + 5)

				def SAFE_SetOverInEvent(self, func, *args):
					self.overInEvent = func
					self.overInArgs = args

				def SAFE_SetOverOutEvent(self, func, *args):
					self.overOutEvent = func
					self.overOutArgs = args

				def OnMouseOverIn(self):
					if self.overInEvent:
						if self.overInArgs:
							self.overInEvent(*self.overInArgs)
						else:
							self.overInEvent()

				def OnMouseOverOut(self):
					if self.overOutEvent:
						if self.overOutArgs:
							self.overOutEvent(*self.overOutArgs)
						else:
							self.overOutEvent()

				def LoadImage(self, image, name = None):
					self.image.LoadImage(image)
					self.SetSize(self.GetWidth(), self.image.GetHeight() + 5 * (self.image.GetHeight() / 32))
					if name != None:
						self.SetText(name)

				def SetText(self, text):
					self.nameLine.SetText(text)

				def RefreshHeight(self):
					ui.ListBoxExNew.Item.RefreshHeight(self)
					self.image.SetRenderingRect(0.0, 0.0 - float(self.removeTop) / float(self.GetHeight()), 0.0, 0.0 - float(self.removeBottom) / float(self.GetHeight()))
					self.image.SetPosition(0, - self.removeTop)

				def OnRunMouseWheel(self, nLen):
					if self.parent:
						try:
							self.parent.OnRunMouseWheel(nLen)
						except:
							pass
					return True

			MAX_ITEM_COUNT = 5

			EXP_BASE_LVDELTA = [
				1,  #  -15 0
				5,  #  -14 1
				10, #  -13 2
				20, #  -12 3
				30, #  -11 4
				50, #  -10 5
				70, #  -9  6
				80, #  -8  7
				85, #  -7  8
				90, #  -6  9
				92, #  -5  10
				94, #  -4  11
				96, #  -3  12
				98, #  -2  13
				100,#  -1  14
				100,#   0  15
				105,#   1  16
				110,#   2  17
				115,#   3  18
				120,#   4  19
				125,#   5  20
				130,#   6  21
				135,#   7  22
				140,#   8  23
				145,#   9  24
				150,#   10 25
				155,#   11 26
				160,#   12 27
				165,#   13 28
				170,#   14 29
				180,#   15 30
			]

			RACE_FLAG_TO_NAME = {
				1 << 0 : localeInfo.TARGET_INFO_RACE_ANIMAL,
				1 << 1 : localeInfo.TARGET_INFO_RACE_UNDEAD,
				1 << 2 : localeInfo.TARGET_INFO_RACE_DEVIL,
				1 << 3 : localeInfo.TARGET_INFO_RACE_HUMAN,
				1 << 4 : localeInfo.TARGET_INFO_RACE_ORC,
				1 << 5 : localeInfo.TARGET_INFO_RACE_MILGYO,
			}

			SUB_RACE_FLAG_TO_NAME = {
				1 << 11 : localeInfo.TARGET_INFO_RACE_ELEC,
				1 << 12 : localeInfo.TARGET_INFO_RACE_FIRE,
				1 << 13 : localeInfo.TARGET_INFO_RACE_ICE,
				1 << 14 : localeInfo.TARGET_INFO_RACE_WIND,
				1 << 15 : localeInfo.TARGET_INFO_RACE_EARTH,
				1 << 16 : localeInfo.TARGET_INFO_RACE_DARK,
			}

			STONE_START_VNUM = 28030
			STONE_LAST_VNUM = 28042

			def __init__(self):
				ui.ThinBoard.__init__(self)

				self.race = 0
				self.hasItems = False
				self.itemTooltip = uiToolTip.ItemToolTip()
				self.itemTooltip.HideToolTip()
				self.stoneImg = None
				self.stoneVnum = None
				self.lastStoneVnum = 0
				self.nextStoneIconChange = 0

				self.itemListBox = None
				self.itemScrollBar = None
				self.pendingItems = []
				self.currentDropHeight = 0

				self.yPos = 7
				self.children = []

				self.SetWindowName("InfoBoard")

			def __del__(self):
				ui.ThinBoard.__del__(self)

			def __ResetBoard(self):
				# Clear all children
				for child in self.children:
					child.Hide()
				self.children = []
				
				self.yPos = 7
				self.hasItems = False
				self.stoneImg = None
				self.stoneVnum = None
				self.lastStoneVnum = 0
				self.nextStoneIconChange = 0
				self.itemListBox = None
				self.itemScrollBar = None
				self.pendingItems = []
				self.currentDropHeight = 0

			def OnMouseWheel(self, nLen):
				if self.itemScrollBar:
					if self.itemScrollBar.IsShow():
						if nLen > 0:
							self.itemScrollBar.OnUp()
						else:
							self.itemScrollBar.OnDown()
						return True
				return True

			def __LoadInformation(self, race):
				import dbg
				self.__ResetBoard()
				self.race = race
				self.__LoadInformation_Default(race)
				self.__LoadInformation_Race(race)
				self.__LoadInformation_Drops(race)
				self.SetSize(250, self.yPos + 10)

			def __LoadInformation_Default_GetHitRate(self, race):
				import dbg
				attacker_dx = nonplayer.GetMonsterDX(race)
				attacker_level = nonplayer.GetMonsterLevel(race)

				self_dx = player.GetStatus(player.DX)
				self_level = player.GetStatus(player.LEVEL)

				iARSrc = min(90, (attacker_dx * 4 + attacker_level * 2) / 6)
				iERSrc = min(90, (self_dx * 4 + self_level * 2) / 6)

				fAR = (float(iARSrc) + 210.0) / 300.0
				fER = (float(iERSrc) * 2 + 5) / (float(iERSrc) + 95) * 3.0 / 10.0

				return fAR - fER

			def __LoadInformation_Default(self, race):
				import dbg
				try:
					self.AppendSeperator()
					self.AppendTextLine(localeInfo.TARGET_INFO_MAX_HP % str(nonplayer.GetMonsterMaxHP(race)))

					# calc att damage
					monsterLevel = nonplayer.GetMonsterLevel(race)
					fHitRate = self.__LoadInformation_Default_GetHitRate(race)
					iDamMin, iDamMax = nonplayer.GetMonsterDamage(race)
					iDamMin = int((iDamMin + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
					iDamMax = int((iDamMax + nonplayer.GetMonsterST(race)) * 2 * fHitRate) + monsterLevel * 2
					iDef = player.GetStatus(player.DEF_GRADE) * (100 + player.GetStatus(player.DEF_BONUS)) / 100
					fDamMulti = nonplayer.GetMonsterDamageMultiply(race)
					iDamMin = int(max(0, iDamMin - iDef) * fDamMulti)
					iDamMax = int(max(0, iDamMax - iDef) * fDamMulti)
					if iDamMin < 1:
						iDamMin = 1
					if iDamMax < 5:
						iDamMax = 5
					self.AppendTextLine(localeInfo.TARGET_INFO_DAMAGE % (str(iDamMin), str(iDamMax)))

					idx = min(len(self.EXP_BASE_LVDELTA) - 1, max(0, (monsterLevel + 15) - player.GetStatus(player.LEVEL)))
					iExp = nonplayer.GetMonsterExp(race) * self.EXP_BASE_LVDELTA[idx] / 100
					self.AppendTextLine(localeInfo.TARGET_INFO_EXP % str(iExp))
					dbg.TraceError("TARGET_INFO: __LoadInformation_Default completed successfully")
				except Exception, e:
					dbg.TraceError("TARGET_INFO: __LoadInformation_Default ERROR: %s" % str(e))

			def __LoadInformation_Race(self, race):
				import dbg
				dbg.TraceError("TARGET_INFO: __LoadInformation_Race called for race %d" % race)
				try:
					dwRaceFlag = nonplayer.GetMonsterRaceFlag(race)
					self.AppendSeperator()

					mainrace = ""
					subrace = ""
					for i in xrange(17):
						curFlag = 1 << i
						if HAS_FLAG(dwRaceFlag, curFlag):
							if self.RACE_FLAG_TO_NAME.has_key(curFlag):
								mainrace += self.RACE_FLAG_TO_NAME[curFlag] + ", "
							elif self.SUB_RACE_FLAG_TO_NAME.has_key(curFlag):
								subrace += self.SUB_RACE_FLAG_TO_NAME[curFlag] + ", "
					if nonplayer.IsMonsterStone(race):
						mainrace += localeInfo.TARGET_INFO_RACE_METIN + ", "
					if mainrace == "":
						mainrace = localeInfo.TARGET_INFO_NO_RACE
					else:
						mainrace = mainrace[:-2]
					if subrace == "":
						subrace = localeInfo.TARGET_INFO_NO_RACE
					else:
						subrace = subrace[:-2]

					self.AppendTextLine(localeInfo.TARGET_INFO_MAINRACE % mainrace)
					self.AppendTextLine(localeInfo.TARGET_INFO_SUBRACE % subrace)
				except Exception, e:
					dbg.TraceError("TARGET_INFO: __LoadInformation_Race ERROR: %s" % str(e))

			def __LoadInformation_Drops(self, race):
				import dbg
				self.AppendSeperator()

				if race in constInfo.MONSTER_INFO_DATA:
					if len(constInfo.MONSTER_INFO_DATA[race]["items"]) == 0:
						self.AppendTextLine("No drops")
					else:
						self.hasItems = True
						self.itemListBox = self.TargetListBox(32 + 5, self.MAX_ITEM_COUNT)
						self.itemListBox.SetSize(self.GetWidth() - 15 * 2 - ui.ScrollBar.SCROLLBAR_WIDTH, (32 + 5) * self.MAX_ITEM_COUNT)
						self.AppendWindow(self.itemListBox, 15)
						self.itemListBox.SetBasePos(0)

						self.itemScrollBar = ui.ScrollBar()
						self.itemScrollBar.SetParent(self)
						listBoxX, listBoxY = self.itemListBox.GetLocalPosition()
						self.itemScrollBar.SetPosition(listBoxX + self.itemListBox.GetWidth(), listBoxY)
						self.itemScrollBar.SetScrollBarSize(32 * self.MAX_ITEM_COUNT + 5 * (self.MAX_ITEM_COUNT - 1))
						
						itemCount = len(constInfo.MONSTER_INFO_DATA[race]["items"])
						if itemCount > self.MAX_ITEM_COUNT:
							self.itemScrollBar.SetMiddleBarSize(float(self.MAX_ITEM_COUNT) / float(itemCount))
						else:
							self.itemScrollBar.SetMiddleBarSize(1.0)
						
						self.itemScrollBar.Show()
						self.itemListBox.SetScrollBar(self.itemScrollBar)
						self.children.append(self.itemScrollBar)

						self.pendingItems = constInfo.MONSTER_INFO_DATA[race]["items"][:]
						self.currentDropHeight = 0

				else:
					self.AppendTextLine("No drops")

			def AppendTextLine(self, text):
				textLine = ui.TextLine()
				textLine.SetParent(self)
				textLine.SetWindowHorizontalAlignCenter()
				textLine.SetHorizontalAlignCenter()
				textLine.SetText(text)
				textLine.SetPosition(0, self.yPos)
				textLine.Show()

				self.children.append(textLine)
				self.yPos += 17

			def AppendSeperator(self):
				img = ui.ImageBox()
				img.LoadImage("d:/ymir work/ui/seperator.tga")
				self.AppendWindow(img)
				x, y = img.GetLocalPosition()
				img.SetPosition(x, y - 15)
				self.yPos -= 15

			def AppendItem(self, listBox, vnums, count):
				if type(vnums) == int:
					vnum = vnums
				else:
					vnum = vnums[0]

				item.SelectItem(vnum)
				itemName = item.GetItemName()
				if type(vnums) != int and len(vnums) > 1:
					vnums = sorted(vnums)
					realName = itemName[:itemName.find("+")]
					if item.GetItemType() == item.ITEM_TYPE_METIN:
						realName = "Stone"
						itemName = realName + "+0 - +4"
					else:
						itemName = realName + "+" + str(vnums[0] % 10) + " - +" + str(vnums[len(vnums) - 1] % 10)
					vnum = vnums[len(vnums) - 1]

				myItem = self.ItemListBoxItem(listBox.GetWidth())
				myItem.LoadImage(item.GetIconImageFileName())
				if count <= 1:
					myItem.SetText(itemName)
				else:
					myItem.SetText("%dx %s" % (count, itemName))
				myItem.SAFE_SetOverInEvent(self.OnShowItemTooltip, vnum)
				myItem.SAFE_SetOverOutEvent(self.OnHideItemTooltip)
				myItem.parent = proxy(listBox)
				listBox.AppendItem(myItem)

				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.stoneImg = myItem
					self.stoneVnum = vnums
					self.lastStoneVnum = self.STONE_LAST_VNUM + vnums[len(vnums) - 1] % 1000 / 100 * 100

				return myItem.GetHeight()

			def OnShowItemTooltip(self, vnum):
				item.SelectItem(vnum)
				if item.GetItemType() == item.ITEM_TYPE_METIN:
					self.itemTooltip.isStone = True
					self.itemTooltip.isBook = False
					self.itemTooltip.isBook2 = False
					self.itemTooltip.SetItemToolTip(self.lastStoneVnum)
				else:
					self.itemTooltip.isStone = False
					self.itemTooltip.isBook = True
					self.itemTooltip.isBook2 = True
					self.itemTooltip.SetItemToolTip(vnum)

			def OnHideItemTooltip(self):
				self.itemTooltip.HideToolTip()

			def AppendWindow(self, wnd, x = 0, width = 0, height = 0):
				if width == 0:
					width = wnd.GetWidth()
				if height == 0:
					height = wnd.GetHeight()

				wnd.SetParent(self)
				if x == 0:
					wnd.SetPosition((self.GetWidth() - width) / 2, self.yPos)
				else:
					wnd.SetPosition(x, self.yPos)
				wnd.Show()

				self.children.append(wnd)
				self.yPos += height + 5

			def OnUpdate(self):
				if self.stoneImg != None and self.stoneVnum != None and app.GetTime() >= self.nextStoneIconChange:
					nextImg = self.lastStoneVnum + 1
					if nextImg % 100 > self.STONE_LAST_VNUM % 100:
						nextImg -= (self.STONE_LAST_VNUM - self.STONE_START_VNUM) + 1
					self.lastStoneVnum = nextImg
					self.nextStoneIconChange = app.GetTime() + 2.5

					item.SelectItem(nextImg)
					itemName = item.GetItemName()
					realName = itemName[:itemName.find("+")]
					realName = realName + "+0 - +4"
					self.stoneImg.LoadImage(item.GetIconImageFileName(), realName)

				if self.pendingItems:
					BATCH_SIZE = 5
					batch = self.pendingItems[:BATCH_SIZE]
					self.pendingItems = self.pendingItems[BATCH_SIZE:]
					
					for curItem in batch:
						if curItem.has_key("vnum_list"):
							self.currentDropHeight += self.AppendItem(self.itemListBox, curItem["vnum_list"], curItem["count"])
						else:
							self.currentDropHeight += self.AppendItem(self.itemListBox, curItem["vnum"], curItem["count"])
					
					if self.currentDropHeight > 0:
						self.itemScrollBar.SetMiddleBarSize(float(self.MAX_ITEM_COUNT) / float(self.currentDropHeight / (32 + 5)))
					
					if hasattr(self.itemListBox, "basePos"):
						self.itemListBox.SetBasePos(self.itemListBox.basePos)

					if self.itemTooltip.IsShow() and self.itemTooltip.isStone:
						self.itemTooltip.SetItemToolTip(self.lastStoneVnum)

			def OnRunMouseWheel(self, nLen):
				if self.itemScrollBar:
					if self.itemScrollBar.IsShow():
						if nLen > 0:
							self.itemScrollBar.OnUp()
						else:
							self.itemScrollBar.OnDown()
						return True
				return False

	def __init__(self):
		ui.ThinBoard.__init__(self)

		name = ui.TextLine()
		name.SetParent(self)
		name.SetDefaultFontName()
		name.SetOutline()
		name.Show()

		hpGauge = ui.Gauge()
		hpGauge.SetParent(self)
		hpGauge.MakeGauge(130, "red")
		hpGauge.Hide()

		hpPercentageText = ui.TextLine()
		hpPercentageText.SetParent(self)
		hpPercentageText.SetDefaultFontName()
		hpPercentageText.SetOutline()
		hpPercentageText.Hide()

		closeButton = ui.Button()
		closeButton.SetParent(self)
		closeButton.SetUpVisual("d:/ymir work/ui/public/close_button_01.sub")
		closeButton.SetOverVisual("d:/ymir work/ui/public/close_button_02.sub")
		closeButton.SetDownVisual("d:/ymir work/ui/public/close_button_03.sub")
		closeButton.SetPosition(30, 13)

		if localeInfo.IsARABIC():
			hpGauge.SetPosition(55, 17)
			hpGauge.SetWindowHorizontalAlignLeft()
			closeButton.SetWindowHorizontalAlignLeft()
		else:
			hpGauge.SetPosition(175, 17)
			hpGauge.SetWindowHorizontalAlignRight()
			hpPercentageText.SetWindowHorizontalAlignRight()
			hpPercentageText.SetPosition(200, 13)
			closeButton.SetWindowHorizontalAlignRight()

		closeButton.SetEvent(ui.__mem_func__(self.OnPressedCloseButton))
		closeButton.Show()

		self.buttonDict = {}
		self.showingButtonList = []
		for buttonName in self.BUTTON_NAME_LIST:
			button = ui.Button()
			button.SetParent(self)
		
			if localeInfo.IsARABIC():
				button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
			else:
				button.SetUpVisual("d:/ymir work/ui/public/small_thin_button_01.sub")
				button.SetOverVisual("d:/ymir work/ui/public/small_thin_button_02.sub")
				button.SetDownVisual("d:/ymir work/ui/public/small_thin_button_03.sub")
			
			button.SetWindowHorizontalAlignCenter()
			button.SetText(buttonName)
			button.Hide()
			self.buttonDict[buttonName] = button
			self.showingButtonList.append(button)

		self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER].SetEvent(ui.__mem_func__(self.OnWhisper))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE].SetEvent(ui.__mem_func__(self.OnExchange))
		self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_ACCEPT_FIGHT].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_AVENGE].SetEvent(ui.__mem_func__(self.OnPVP))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_FRIEND].SetEvent(ui.__mem_func__(self.OnAppendToMessenger))
		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyInvite))
		self.buttonDict[localeInfo.TARGET_BUTTON_LEAVE_PARTY].SetEvent(ui.__mem_func__(self.OnPartyExit))
		self.buttonDict[localeInfo.TARGET_BUTTON_EXCLUDE].SetEvent(ui.__mem_func__(self.OnPartyRemove))

		self.buttonDict[localeInfo.TARGET_BUTTON_INVITE_GUILD].SAFE_SetEvent(self.__OnGuildAddMember)
		self.buttonDict[localeInfo.TARGET_BUTTON_DISMOUNT].SAFE_SetEvent(self.__OnDismount)
		self.buttonDict[localeInfo.TARGET_BUTTON_EXIT_OBSERVER].SAFE_SetEvent(self.__OnExitObserver)
		self.buttonDict[localeInfo.TARGET_BUTTON_VIEW_EQUIPMENT].SAFE_SetEvent(self.__OnViewEquipment)
		self.buttonDict[localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY].SAFE_SetEvent(self.__OnRequestParty)
		self.buttonDict[localeInfo.TARGET_BUTTON_BUILDING_DESTROY].SAFE_SetEvent(self.__OnDestroyBuilding)
		self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW].SAFE_SetEvent(self.__OnEmotionAllow)
		
		self.buttonDict["VOTE_BLOCK_CHAT"].SetEvent(ui.__mem_func__(self.__OnVoteBlockChat))

		if app.ENABLE_SEND_TARGET_INFO:
			infoButton = ui.Button()
			infoButton.SetParent(self)
			infoButton.SetUpVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			infoButton.SetOverVisual("d:/ymir work/ui/pattern/q_mark_02.tga")
			infoButton.SetDownVisual("d:/ymir work/ui/pattern/q_mark_01.tga")
			infoButton.SetEvent(ui.__mem_func__(self.OnPressedInfoButton))
			infoButton.Hide()

			infoBoard = self.InfoBoard()
			infoBoard.Hide()
			infoButton.showWnd = infoBoard

		self.name = name
		self.hpGauge = hpGauge
		self.hpPercentageText = hpPercentageText
		self.closeButton = closeButton
		self.nameString = 0
		self.nameLength = 0
		self.vid = 0
		self.eventWhisper = None
		self.isShowButton = False

		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton = infoButton
			self.infoBoard = infoBoard

		self.__Initialize()
		self.ResetTargetBoard()

	def __del__(self):
		ui.ThinBoard.__del__(self)

		print "===================================================== DESTROYED TARGET BOARD"

	def __Initialize(self):
		self.nameString = ""
		self.nameLength = 0
		self.vid = 0
		self.isShowButton = False
		if app.ENABLE_SEND_TARGET_INFO:
			self.raceNum = 0

	def Destroy(self):
		self.eventWhisper = None
		self.closeButton = None
		self.showingButtonList = None
		self.buttonDict = None
		self.name = None
		self.hpGauge = None
		self.__Initialize()

	def OnPressedCloseButton(self):
		self.Close()

	if app.ENABLE_SEND_TARGET_INFO:
		def RefreshMonsterInfoBoard(self):
			if self.raceNum:
				self.infoBoard._InfoBoard__LoadInformation(self.raceNum)

		def OnPressedInfoButton(self):
			if self.infoButton.showWnd.IsShow():
				self.infoButton.showWnd.Hide()
			else:
				if self.raceNum:
					self.infoBoard._InfoBoard__LoadInformation(self.raceNum)
				
				boardX, boardY = self.GetLocalPosition()
				targetBoardWidth = self.GetWidth()
				targetBoardHeight = self.GetHeight()
				infoBoardWidth = self.infoButton.showWnd.GetWidth()
				
				# Calcular posicao centralizada abaixo
				newX = boardX + (targetBoardWidth - infoBoardWidth) / 2
				newY = boardY + targetBoardHeight
				
				self.infoButton.showWnd.SetPosition(newX, newY)
				self.infoButton.showWnd.Show()

	def Close(self):
		self.__Initialize()
		player.ClearTarget()
		if app.ENABLE_SEND_TARGET_INFO:
			if self.infoBoard:
				self.infoBoard.Hide()
		self.Hide()

	def Open(self, vid, name):
		if vid:
			if not constInfo.GET_VIEW_OTHER_EMPIRE_PLAYER_TARGET_BOARD():
				if not player.IsSameEmpire(vid):
					self.Hide()
					return

			if vid != self.GetTargetVID():
				self.ResetTargetBoard()
				self.SetTargetVID(vid)
				self.SetTargetName(name)

			if player.IsMainCharacterIndex(vid):
				self.__ShowMainCharacterMenu()		
			elif chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
				self.Hide()
			else:
				self.RefreshButton()
				self.Show()
		else:
			self.HideAllButton()
			self.__ShowButton(localeInfo.TARGET_BUTTON_WHISPER)
			self.__ShowButton("VOTE_BLOCK_CHAT")
			self.__ArrangeButtonPosition()
			self.SetTargetName(name)
			self.Show()
			
	def Refresh(self):
		if self.IsShow():
			if self.IsShowButton():			
				self.RefreshButton()		

	def RefreshByVID(self, vid):
		if vid == self.GetTargetVID():			
			self.Refresh()
			
	def RefreshByName(self, name):
		if name == self.GetTargetName():
			self.Refresh()

	def __ShowMainCharacterMenu(self):
		canShow=0

		self.HideAllButton()

		if player.IsMountingHorse():
			self.__ShowButton(localeInfo.TARGET_BUTTON_DISMOUNT)
			canShow=1

		if player.IsObserverMode():
			self.__ShowButton(localeInfo.TARGET_BUTTON_EXIT_OBSERVER)
			canShow=1

		if canShow:
			self.__ArrangeButtonPosition()
			self.Show()
		else:
			self.Hide()
			
	def __ShowNameOnlyMenu(self):
		self.HideAllButton()

	def SetWhisperEvent(self, event):
		self.eventWhisper = event

	def UpdatePosition(self):
		self.SetPosition(wndMgr.GetScreenWidth()/2 - self.GetWidth()/2, 10)

	def ResetTargetBoard(self):

		for btn in self.buttonDict.values():
			btn.Hide()

		self.__Initialize()

		self.name.SetPosition(0, 13)
		self.name.SetHorizontalAlignCenter()
		self.name.SetWindowHorizontalAlignCenter()
		self.hpGauge.Hide()
		if hasattr(self, "hpPercentageText"):
			self.hpPercentageText.Hide()
		self.SetSize(250, 40)

		if app.ENABLE_SEND_TARGET_INFO:
			self.infoButton.Hide()
			self.infoBoard.Hide()

	def SetTargetVID(self, vid):
		self.vid = vid

	def SetEnemyVID(self, vid):
		self.SetTargetVID(vid)

		name = chr.GetNameByVID(vid)
		level = nonplayer.GetLevelByVID(vid)
		grade = nonplayer.GetGradeByVID(vid)

		nameFront = ""
		if -1 != level:
			nameFront += "Lv." + str(level) + " "
		if self.GRADE_NAME.has_key(grade):
			nameFront += "(" + self.GRADE_NAME[grade] + ") "

		self.SetTargetName(nameFront + name)

		if app.ENABLE_SEND_TARGET_INFO:
			race = nonplayer.GetRaceNumByVID(vid)
			self.raceNum = race
			if race:
				# Posicionar o botão (?) ao lado do nome
				textWidth, textHeight = self.name.GetTextSize()
				# O texto está em Y=13. Ajustando o botão para ficar centralizado verticalmente com o texto.
				self.infoButton.SetPosition(23 + textWidth + 5, 12)
				self.infoButton.Show()
				# Solicitar drops ao servidor
				net.SendTargetInfoLoad(vid)
				# Carregar informações
				self.infoBoard._InfoBoard__LoadInformation(race)
				self.infoBoard.Hide()  # Começa escondido, aparece ao clicar no (?)
			else:
				self.infoButton.Hide()
				self.infoBoard.Hide()

	def GetTargetVID(self):
		return self.vid

	def GetTargetName(self):
		return self.nameString

	def SetTargetName(self, name):
		self.nameString = name
		self.nameLength = len(name)
		self.name.SetText(name)

	def SetHP(self, hpPercentage):
		if not self.hpGauge.IsShow():

			self.SetSize(200 + 7*self.nameLength, self.GetHeight())

			if localeInfo.IsARABIC():
				self.name.SetPosition( self.GetWidth()-23, 13)
			else:
				self.name.SetPosition(23, 13)

			self.name.SetWindowHorizontalAlignLeft()
			self.name.SetHorizontalAlignLeft()
			self.hpGauge.Show()
			self.UpdatePosition()

		self.hpGauge.SetPercentage(hpPercentage, 100)
		self.hpPercentageText.SetText("%d%%" % hpPercentage)
		self.hpPercentageText.Show()

	def ShowDefaultButton(self):

		self.isShowButton = True
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_WHISPER])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_FIGHT])
		self.showingButtonList.append(self.buttonDict[localeInfo.TARGET_BUTTON_EMOTION_ALLOW])
		for button in self.showingButtonList:
			button.Show()

	def HideAllButton(self):
		self.isShowButton = False
		for button in self.showingButtonList:
			button.Hide()
		self.showingButtonList = []

	def __ShowButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		self.buttonDict[name].Show()
		self.showingButtonList.append(self.buttonDict[name])

	def __HideButton(self, name):

		if not self.buttonDict.has_key(name):
			return

		button = self.buttonDict[name]
		button.Hide()

		for btnInList in self.showingButtonList:
			if btnInList == button:
				self.showingButtonList.remove(button)
				break

	def OnWhisper(self):
		if None != self.eventWhisper:
			self.eventWhisper(self.nameString)

	def OnExchange(self):
		net.SendExchangeStartPacket(self.vid)

	def OnPVP(self):
		net.SendChatPacket("/pvp %d" % (self.vid))

	def OnAppendToMessenger(self):
		net.SendMessengerAddByVIDPacket(self.vid)

	def OnPartyInvite(self):
		net.SendPartyInvitePacket(self.vid)

	def OnPartyExit(self):
		net.SendPartyExitPacket()

	def OnPartyRemove(self):
		net.SendPartyRemovePacket(self.vid)

	def __OnGuildAddMember(self):
		net.SendGuildAddMemberPacket(self.vid)

	def __OnDismount(self):
		net.SendChatPacket("/unmount")

	def __OnExitObserver(self):
		net.SendChatPacket("/observer_exit")

	def __OnViewEquipment(self):
		net.SendChatPacket("/view_equip " + str(self.vid))

	def __OnRequestParty(self):
		net.SendChatPacket("/party_request " + str(self.vid))

	def __OnDestroyBuilding(self):
		net.SendChatPacket("/build d %d" % (self.vid))

	def __OnEmotionAllow(self):
		net.SendChatPacket("/emotion_allow %d" % (self.vid))
		
	def __OnVoteBlockChat(self):
		cmd = "/vote_block_chat %s" % (self.nameString)
		net.SendChatPacket(cmd)

	def OnPressEscapeKey(self):
		self.OnPressedCloseButton()
		return True

	def IsShowButton(self):
		return self.isShowButton

	def RefreshButton(self):

		self.HideAllButton()

		if chr.INSTANCE_TYPE_BUILDING == chr.GetInstanceType(self.vid):
			#self.__ShowButton(localeInfo.TARGET_BUTTON_BUILDING_DESTROY)
			#self.__ArrangeButtonPosition()
			return
		
		if player.IsPVPInstance(self.vid) or player.IsObserverMode():
			# PVP_INFO_SIZE_BUG_FIX
			self.SetSize(200 + 7*self.nameLength, 40)
			self.UpdatePosition()
			# END_OF_PVP_INFO_SIZE_BUG_FIX			
			return	

		self.ShowDefaultButton()

		if guild.MainPlayerHasAuthority(guild.AUTH_ADD_MEMBER):
			if not guild.IsMemberByName(self.nameString):
				if 0 == chr.GetGuildID(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_GUILD)

		if not messenger.IsFriendByName(self.nameString):
			self.__ShowButton(localeInfo.TARGET_BUTTON_FRIEND)

		if player.IsPartyMember(self.vid):

			self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if player.IsPartyLeader(self.vid):
				self.__ShowButton(localeInfo.TARGET_BUTTON_LEAVE_PARTY)
			elif player.IsPartyLeader(player.GetMainCharacterIndex()):
				self.__ShowButton(localeInfo.TARGET_BUTTON_EXCLUDE)

		else:
			if player.IsPartyMember(player.GetMainCharacterIndex()):
				if player.IsPartyLeader(player.GetMainCharacterIndex()):
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
			else:
				if chr.IsPartyMember(self.vid):
					self.__ShowButton(localeInfo.TARGET_BUTTON_REQUEST_ENTER_PARTY)
				else:
					self.__ShowButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)

			if player.IsRevengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_AVENGE)
			elif player.IsChallengeInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)
				self.__ShowButton(localeInfo.TARGET_BUTTON_ACCEPT_FIGHT)
			elif player.IsCantFightInstance(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

			if not player.IsSameEmpire(self.vid):
				self.__HideButton(localeInfo.TARGET_BUTTON_INVITE_PARTY)
				self.__HideButton(localeInfo.TARGET_BUTTON_FRIEND)
				self.__HideButton(localeInfo.TARGET_BUTTON_FIGHT)

		distance = player.GetCharacterDistance(self.vid)
		if distance > self.EXCHANGE_LIMIT_RANGE:
			self.__HideButton(localeInfo.TARGET_BUTTON_EXCHANGE)
			self.__ArrangeButtonPosition()

		self.__ArrangeButtonPosition()

	def __ArrangeButtonPosition(self):
		showingButtonCount = len(self.showingButtonList)

		pos = -(showingButtonCount / 2) * 68
		if 0 == showingButtonCount % 2:
			pos += 34

		for button in self.showingButtonList:
			button.SetPosition(pos, 33)
			pos += 68

		self.SetSize(max(150, showingButtonCount * 75), 65)
		self.UpdatePosition()

	def OnUpdate(self):
		if self.isShowButton:

			exchangeButton = self.buttonDict[localeInfo.TARGET_BUTTON_EXCHANGE]
			distance = player.GetCharacterDistance(self.vid)

			if distance < 0:
				return

			if exchangeButton.IsShow():
				if distance > self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()

			else:
				if distance < self.EXCHANGE_LIMIT_RANGE:
					self.RefreshButton()
