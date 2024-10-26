import ui,app,chat,chr,net,player,item,skill,time,game,shop,chrmgr,OpenLib,eXLib,MapManager,quest,event,playerSettingModule
import background,constInfo,miniMap,wndMgr,math,uiCommon,grp,FileManager,UIComponents,Movement,OpenLog, Hooks, Data,chrmrgl
import DmgHacks as Dmg
import ChannelSwitcher
from FileManager import boolean
import ChannelSwitcher
import UIComponents,time


class SettingsDialog(ui.ScriptWindow):
	TIME_DEAD = 10
	TIME_POTS = 0.2
	RED_POTIONS_IDS = [27001,27002,27003,27007,27051,27201,27202,27203]
	BLUE_POTIONS_IDS = [27004,27005,27006,27008,27052,27204,27205,27206,63018,27801]
	solucan = [27801]
	spamsecim=0
	spamyeni=0
	spamtext=''
	startmap=app.GetGlobalTime()
	spamtime=0
	spamdelay=0
	intime=app.GetGlobalTime()
	questname='silahlar'
	speedMultiplier2=0	
	WARRIOR = [21900, 21910, 21920, 21930, 21940, 21950, 21960, 21970,  
			21903, 21913, 21923, 21933, 21943, 21953, 21963, 21973] 
		 
	

	ASSASSIN = [21900, 21910, 21920, 21930, 21940, 21950, 21960, 21970,  
		21901, 21911, 21921, 21931, 21941, 21951, 21961, 21971,  
		21902, 21912, 21922, 21932, 21942, 21952, 21962, 21972]  
		
	

	SURA = [21900, 21910, 21920, 21930, 21940, 21950, 21960, 21970] 
		 
	

	SHAMAN = [21904, 21914, 21924, 21934, 21944, 21954, 21964, 21974,  
		21905, 21915, 21925, 21935, 21945, 21955, 21965, 21975] 
		 
	

	WOLFMAN = [
			21906, 21916, 21926, 21936, 21946, 21956, 21966, 21976 
			]
	def __init__(self):
		ui.ScriptWindow.__init__(self)
		self.restartHere = False
		self.restartInCity = False
		self.bluePotions = True
		self.redPotions = True
		self.speedHack = False
		self.antiExpTimerSleep = 0
		self.antiExp = False
		self.minMana = 80
		self.minHealth = 80
		self.speedMultiplier = 0.0
		self.pickItemsFirst = False
		self.lastTimeDead = OpenLib.GetTime()
		self.mapkontrol=""
		self.xa=0
		self.ya=0
		self.isinposition=0
		self.pickUp = False
		self.pickUpRange = 290.0
		self.pickUpSpeed = 0.5
		self.pickFilter = set()
		self.excludeInFilter = True
		self.useRangePickup = False
		self.doNotPickupIfPlayerHere = False
		self.checkIsWallBetweenPlayerAndItem = False
		self.pickItemsIgnorePath = False
		self.MoveSpeedStateCount=0
		self.useOnClickDmg = False
		self.onClickDmgSpeed = 0.0
		Data.time_Settings_timerDmg = OpenLib.GetTime()

		self.wallHack = False
		self.canFarmbotExchangeBool = False
		self.canFarmbotExchangeEnergyBool = False
		self.canFarmbotSellBool = False

		self.sellItems = set()

		self.can_add_waiter = True
		Data.time_Settings_timerPots = 0
		Data.time_Settings_timerDead = 0
		Data.time_Settings_pickUpTimer = 0
		self.LoadSettings()
		self.BuildWindow()
	
	def BuildWindow(self):
		self.Board = ui.BoardWithTitleBar() 
		self.Board.SetPosition(52, 40)
		self.Board.SetSize(300, 370) 
		self.Board.SetTitleName("Settings")
		self.Board.AddFlag("movable")
		self.Board.SetCloseEvent(self.Close)
		self.Board.Hide()
		
		self.comp = UIComponents.Component()

		self.TabWidget = UIComponents.TabWindow(10,30,300-20,370-40,self.Board,['General','Pickup','Attack','Shop', 'Channels'])
		self.generalTab = self.TabWidget.GetTab(0)
		self.pickupTab = self.TabWidget.GetTab(1)
		self.attackTab = self.TabWidget.GetTab(2)
		self.shopTab = self.TabWidget.GetTab(3)
		self.channelsTab = self.TabWidget.GetTab(4)

		self.DmgMenuButton = self.comp.Button(self.attackTab, '', 'Damage Hacks', 120, 150, self.OpenDmgMenu,  eXLib.PATH + 'Terminal/Images/General/dmg_0.tga', eXLib.PATH + 'Terminal/Images/General/dmg_1.tga', eXLib.PATH + 'Terminal/Images/General/dmg_0.tga')
		self.OneHandedButton = self.comp.Button(self.attackTab, '', 'One-Handed', 40, 150, self.SetOneHand, eXLib.PATH + 'Terminal/Images/General/onehand_0.tga', eXLib.PATH + 'Terminal/Images/General/onehand_1.tga', eXLib.PATH + 'Terminal/Images/General/onehand_0.tga')
		self.TwoHandedButton = self.comp.Button(self.attackTab, '', 'Two-Handed', 200, 150, self.SetTwoHand, eXLib.PATH + 'Terminal/Images/General/twohand_0.tga', eXLib.PATH + 'Terminal/Images/General/twohand_1.tga', eXLib.PATH + 'Terminal/Images/General/twohand_0.tga')
		self.dmgButton,self.dmgSlider,self.dmgLabel = UIComponents.GetSliderButtonLabel(self.attackTab,self.OnDmgSpeedMove, '', 'Dmg on selected target (defaults to cloud damage on dagger ninja)', 28, 18,image=eXLib.PATH + 'Terminal/Images/General/monster_1.tga',funcState=self.OnDmgOnOff,defaultValue=int(self.useOnClickDmg),defaultSlider=float(self.onClickDmgSpeed))
		
		##GENERAL
		self.loginBtn = self.comp.OnOffButton(self.generalTab, '\t\t\t\t\t\tAuto Login', '', 20, 160,funcState=self.AutoLoginOnOff,defaultValue=int(self.autoLogin))
		self.reviveBtn = self.comp.OnOffButton(self.generalTab, '\t\t\t\t\t\tAuto Restart', '', 20, 140,funcState=self.ReviveOnOff,defaultValue=int(self.restartHere))
		#self.reviveInCityBtn = self.comp.OnOffButton(self.generalTab, '\t\t\t\t\t\t in city?', '', 120, 140,funcState=self.ReviveInCityOnOff,defaultValue=int(self.restartInCity))
		self.WallHackBtn = self.comp.OnOffButton(self.generalTab, '', 'WallHack', 210, 140, image=eXLib.PATH + 'Terminal/Images/General/wall.tga',funcState=self.WallHackSwich,defaultValue=int(self.wallHack))
		self.antiExpBtn = self.comp.OnOffButton(self.generalTab, '\t\t\t\t\t\tAntiExp', '', 20, 180,funcState=self.startAntiExp,defaultValue=int(self.antiExp))
		
		self.redPotButton,self.SlideRedPot,self.redPotLabel = UIComponents.GetSliderButtonLabel(self.generalTab,self.SlideRedMove, '', 'Use Red Potions', 28, 18,image="icon/item/27002.tga",funcState=self.OnRedOnOff,defaultValue=int(self.redPotions),defaultSlider=float(self.minHealth/100.0))
		self.bluePotButton,self.SlideBluePot,self.bluePotLabel = UIComponents.GetSliderButtonLabel(self.generalTab,self.SlideBlueMove, '', 'Use Blue Potions', 28, 50,image="icon/item/27005.tga",funcState=self.OnBlueOnOff,defaultValue=int(self.bluePotions),defaultSlider=float(self.minMana/100.0))
		self.speedHackButton,self.SlideSpeedHack,self.speedHackLabel = UIComponents.GetSliderButtonLabel(self.generalTab,self.SlideMovSpeedMove, '', 'Use Speed Boost', 28, 82,image="icon/item/27104.tga",funcState=self.OnSpeedHackOnOff,defaultValue=int(self.speedHack),defaultSlider=float(self.speedMultiplier/10))
		self.waitTimeDeadSlotBar, self.waitTimeDeadEditLine = self.comp.EditLine(self.generalTab, '', 130, 235, 25, 15, 3)
		self.waitTimeDeadText = self.comp.TextLine(self.generalTab, 's', 160, 235, self.comp.RGB(255, 255, 255))
		self.waitTimeDeadText2 = self.comp.TextLine(self.generalTab, 'Time to wait after dead:', 20, 235, self.comp.RGB(255, 255, 255))
		self.showKeyBindsBtn = self.comp.Button(self.generalTab, 'KeyBinds', 'Show key binds', 190, 235, self.OnShowKeyBindsButton,
                                             'd:/ymir work/ui/public/Middle_Button_01.sub',
                                             'd:/ymir work/ui/public/Middle_Button_02.sub',
                                             'd:/ymir work/ui/public/Middle_Button_03.sub')
		##PICKUP
		self.pickupButton,self.SlidePickupSpeed,self.speedPickupLabel = UIComponents.GetSliderButtonLabel(self.pickupTab,self.pickupSpeedSlide, '', 'Enable Pickup', 30, 18,image= eXLib.PATH + "Terminal/Images/General/pickup.tga",funcState=self.OnPickupOnOff,defaultValue=int(self.pickUp),defaultSlider=float(self.pickUpSpeed/3.0))
		self.rangePickupButton,self.SliderangePickup,self.rangePickupLabel = UIComponents.GetSliderButtonLabel(self.pickupTab,self.pickupRangeSlide, 'Range', 'Enable Range Pickup', 15, 60,funcState=self.OnRangePickupOnOff,offsetX=30,offsetY=4,defaultValue=int(self.useRangePickup),defaultSlider=float(self.pickUpRange/10000.0))
		self.ItemValueText = self.comp.TextLine(self.pickupTab, 'Search Item:', 15, 270, self.comp.RGB(255, 255, 255))
		self.SearchPickItemButton = self.comp.Button(self.pickupTab, 'Search', '', 210, 268,  self.UpdatePickFilterList, 'd:/ymir work/ui/public/small_Button_01.sub', 'd:/ymir work/ui/public/small_Button_02.sub', 'd:/ymir work/ui/public/small_Button_03.sub')
		self.AddPickItemBtn = self.comp.Button(self.pickupTab, 'Add Item', '', 200, 200, self.OpenPickItemDialog, 'd:/ymir work/ui/public/Middle_Button_01.sub', 'd:/ymir work/ui/public/Middle_Button_02.sub', 'd:/ymir work/ui/public/Middle_Button_03.sub')
		self.PickCancelBtn = self.comp.Button(self.pickupTab, 'Remove', '', 200, 230, self.UIPickRemoveFilterItem, 'd:/ymir work/ui/public/Middle_Button_01.sub', 'd:/ymir work/ui/public/Middle_Button_02.sub', 'd:/ymir work/ui/public/Middle_Button_03.sub')
		self.PickSearchItemSlotBar, self.PickSearchItemEditLine = self.comp.EditLine(self.pickupTab, '', 85, 270, 110, 15, 20)
		self.labelFilter = self.comp.TextLine(self.pickupTab, 'Pickup Filter', 115, 90, self.comp.RGB(255, 255, 0))
		
		self.pickItemsFirstBtn = self.comp.OnOffButton(self.pickupTab, '\t\t\tItems first', 'Will pick items before yang', 180, 150,funcState=self.OnChangePickItemFirst,defaultValue=int(self.pickItemsFirst))
		self.pickItemsIgnorePathBtn = self.comp.OnOffButton(self.pickupTab, '\t\t\tIgnore Block Path', "Doesn't pick items with path blocked", 180, 170,funcState=self.OnChangePickItemsIgnorePath,defaultValue=int(self.pickItemsIgnorePath))
		
		self.PickfilterModeBtn = self.comp.OnOffButton(self.pickupTab, '\t\t\tExclude Items', 'If not selected will only pick items in the list', 180, 130,funcState=self.OnChangePickMode,defaultValue=int(self.excludeInFilter))
		self.doNotPickupIfPlayerNear = self.comp.OnOffButton(self.pickupTab, '\t\t\tAvoid players', 'If you select this option, pickup will work only when there are not any player', 180, 110,funcState=self.OnDoNotPickupIfPlayerNear,defaultValue=int(self.doNotPickupIfPlayerHere))
		#self.checkIsWallBetweenPlayerAndItemBtn = self.comp.OnOffButton(self.pickupTab, '\t\t\tNo lags mode', 'If this option is checked, Terminal will check is wall between player and item', 190, 90,funcState=self.OnDoNotPickupIfPlayerNear,defaultValue=int(self.doNotPickupIfPlayerHere))
		self.PickbarItems, self.PickfileListBox, self.PickScrollBar = self.comp.ListBoxEx2(self.pickupTab, 15, 117, 140, 150)


		##SHOP
		self.labelSell = self.comp.TextLine(self.shopTab, 'Items to always sell', 95, 10, self.comp.RGB(255, 255, 0))
		self.ShopbarItems, self.ShopFileListBox, self.ShopScrollBar = self.comp.ListBoxEx2(self.shopTab, 60, 30, 140, 150)
		self.AddSellItemBtn = self.comp.Button(self.shopTab, 'Add', '', 65, 185, self.OpenSellItemDialog, 'd:/ymir work/ui/public/Middle_Button_01.sub', 'd:/ymir work/ui/public/Middle_Button_02.sub', 'd:/ymir work/ui/public/Middle_Button_03.sub')
		self.SellRemoveBtn = self.comp.Button(self.shopTab, 'Remove', '', 140, 185, self.UISellRemoveFilterItem, 'd:/ymir work/ui/public/Middle_Button_01.sub', 'd:/ymir work/ui/public/Middle_Button_02.sub', 'd:/ymir work/ui/public/Middle_Button_03.sub')
		#self.labelFarmbotOptions = self.comp.TextLine(self.shopTab, 'Farmbot Options', 95, 210, self.comp.RGB(255, 255, 0))
		#self.CanFarmbotExchangeToShop = self.comp.OnOffButton(self.shopTab, '\t\tSell items', '', 60, 225 ,funcState=self.OnCanFarmbotExchangeToShop, defaultValue=self.canFarmbotSellBool)
		#self.CanFarmbotExchangeToEnergy = self.comp.OnOffButton(self.shopTab, '\t\t\t\t\t\t\t\t\t\t\t\tExchange to energy fragments', '', 60, 245,funcState=self.OnCanFarmbotExchangeToEnergy, defaultValue=self.canFarmbotExchangeEnergyBool)
		#self.BtnRedBuy = self.comp.OnOffButton(self.generalTab, '', 'Buy Red Pots', 200, 130, image='icon/item/27002.tga',funcState=self.OnRedBuy,defaultValue=int(self.wallHack))

		## CHANNELS
		self.ChannelSwitcher = ChannelSwitcher.instance
		self.ChannelSwitcher.BuildWindow(self.channelsTab)
		self.ChannelSwitcher.OnRefreshButton()
		for id in sorted(self.ChannelSwitcher.channels):
			setattr(self, 'channel_' + str(id), self.ChannelSwitcher.channels[id]['btn'])


		self.waitTimeDeadEditLine.SetText(str(FileManager.ReadConfig("timeAfterDead")))

		##Init labels
		self.UpdatePickFilterList()
		self.UpdateSellFilterList()
		self.pickupSpeedSlide()
		self.pickupRangeSlide()
		self.SlideRedMove()
		self.SlideBlueMove()
		self.SlideMovSpeedMove()
		self.OnDmgSpeedMove()

	def LoadSettings(self):
		#OpenLog.DebugPrint("Loading Settings")
		self.autoLogin = boolean(FileManager.ReadConfig("AutoLogin"))
		self.restartHere = boolean(FileManager.ReadConfig("AutoRestart"))
		self.bluePotions = boolean(FileManager.ReadConfig("UseBluePots"))
		self.redPotions = boolean(FileManager.ReadConfig("UseRedPots"))
		self.speedHack = boolean(FileManager.ReadConfig("SpeedHack"))
		self.speedMultiplier = float(FileManager.ReadConfig("SpeedHackMultiplier"))
		self.minMana = int(FileManager.ReadConfig("MinMana"))
		self.minHealth = int(FileManager.ReadConfig("MinHealth"))
		self.pickUp = boolean(FileManager.ReadConfig("PickupUse"))
		self.pickUpRange = float(FileManager.ReadConfig("PickupRange"))
		self.pickUpSpeed = float(FileManager.ReadConfig("PickupSpeed"))
		self.excludeInFilter = boolean(FileManager.ReadConfig("FilterMode"))
		self.useRangePickup = boolean(FileManager.ReadConfig("UseRangePickup"))
		self.wallHack = boolean(FileManager.ReadConfig("WallHack"))
		self.onClickDmgSpeed  = boolean(FileManager.ReadConfig("OnClickDamageSpeed"))
		self.antiExp = boolean(FileManager.ReadConfig("antiExp"))
		self.doNotPickupIfPlayerHere = boolean(FileManager.ReadConfig("doNotPickupIfPlayerHere"))
		self.pickItemsFirst = boolean(FileManager.ReadConfig("pickItemsFirst"))
		self.pickItemsIgnorePath = boolean(FileManager.ReadConfig("pickItemsIgnorePath"))

		if(self.pickItemsIgnorePath):
			eXLib.ItemGrndInBlockedPath()
		else:
			eXLib.ItemGrndNotInBlockedPath()

		if(self.pickItemsFirst):
			eXLib.ItemGrndItemFirst()
		else:
			eXLib.ItemGrndNoItemFirst()

		eXLib.ItemGrndSelectRange(self.pickUpRange)

		for i in FileManager.LoadListFile(FileManager.CONFIG_PICKUP_FILTER):
			self.addPickFilterItem(int(i))
		self.sellItems = {int(i) for i in FileManager.LoadListFile(FileManager.CONFIG_SELL_INVENTORY)}

	def SaveSettings(self):
		#OpenLog.DebugPrint("Saving Settings")
		FileManager.WriteConfig("AutoLogin", str(self.autoLogin))
		FileManager.WriteConfig("AutoRestart", str(self.restartHere))
		FileManager.WriteConfig("UseBluePots", str(self.bluePotions))
		FileManager.WriteConfig("UseRedPots", str(self.redPotions))
		FileManager.WriteConfig("SpeedHack", str(self.speedHack))
		FileManager.WriteConfig("SpeedHackMultiplier", str(self.speedMultiplier))
		FileManager.WriteConfig("MinMana", str(self.minMana))
		FileManager.WriteConfig("MinHealth", str(self.minHealth))
		FileManager.WriteConfig("PickupUse", str(self.pickUp))
		FileManager.WriteConfig("PickupRange", str(self.pickUpRange))
		FileManager.WriteConfig("PickupSpeed", str(self.pickUpSpeed))
		FileManager.WriteConfig("FilterMode", str(self.excludeInFilter))
		FileManager.WriteConfig("UseRangePickup", str(self.useRangePickup))
		FileManager.WriteConfig("WallHack", str(self.wallHack))
		FileManager.WriteConfig("OnClickDamageSpeed", str(self.onClickDmgSpeed))
		FileManager.WriteConfig("antiExp", str(self.antiExp))
		FileManager.WriteConfig("timeAfterDead", str(self.waitTimeDeadEditLine.GetText()))
		FileManager.WriteConfig("doNotPickupIfPlayerHere", str(self.doNotPickupIfPlayerHere))
		FileManager.WriteConfig("pickItemsFirst", str(self.pickItemsFirst))
		FileManager.WriteConfig("pickItemsIgnorePath", str(self.pickItemsIgnorePath))

		
		#chat.AppendChat(3,str(self.pickUp))
		FileManager.SaveListFile(FileManager.CONFIG_PICKUP_FILTER,self.pickFilter)
		FileManager.SaveListFile(FileManager.CONFIG_SELL_INVENTORY,self.sellItems)
		FileManager.Save()

#UI STUFF
	def OnShowKeyBindsButton(self):
		from Terminal.Modules import KeyBot
		KeyBot.instance.switch_state()

	def OnDoNotPickupIfPlayerNear(self, val):
		self.doNotPickupIfPlayerHere = val

	def OnCanFarmbotExchangeToShop(self, val):
		self.canFarmbotSellBool = val

	def OnChangePickItemFirst(self,val):
		self.pickItemsFirst = val
		if(self.pickItemsFirst):
			eXLib.ItemGrndItemFirst()
		else:
			eXLib.ItemGrndNoItemFirst()


	def OnCanFarmbotExchangeToEnergy(self, val):
		self.canFarmbotExchangeEnergyBool = val

	def UpdatePickFilterList(self):	
		searchValue = self.PickSearchItemEditLine.GetText()
		self.PickfileListBox.RemoveAllItems()
		for filterItem in sorted(self.pickFilter):
			item.SelectItem(filterItem)
			name = item.GetItemName()
			if searchValue in name:
				self.PickfileListBox.AppendItem(OpenLib.Item(str(filterItem)+" "+name))

	def UpdateSellFilterList(self):
		self.ShopFileListBox.RemoveAllItems()
		for filterItem in sorted(self.sellItems):
			item.SelectItem(filterItem)
			name = item.GetItemName()
			self.ShopFileListBox.AppendItem(OpenLib.Item(str(filterItem)+" "+name))

	def GetTimeAfterDead(self):
		return float(self.waitTimeDeadEditLine.GetText())

	def UIAddPickFilterItem(self,item):
		self.addPickFilterItem(item)
		self.UpdatePickFilterList()

	def UIAddSellFilterItem(self,item):
		self.sellItems.add(item)
		self.UpdateSellFilterList()

	def OnChangePickItemsIgnorePath(self,val):
		self.pickItemsIgnorePath = val
		if(self.pickItemsIgnorePath):
			eXLib.ItemGrndInBlockedPath()
		else:
			eXLib.ItemGrndNotInBlockedPath()

	def OpenPickItemDialog(self):
		pos = self.Board.GetGlobalPosition()
		ItemListDialog(self.UIAddPickFilterItem,pos[0]+self.Board.GetWidth(),pos[1])
		#ItemListDialog(self.AddFilterItem,pos[0],pos[1])

	def OpenSellItemDialog(self):
		pos = self.Board.GetGlobalPosition()
		ItemListDialog(self.UIAddSellFilterItem,pos[0]+self.Board.GetWidth(),pos[1])

	def UISellRemoveFilterItem(self):
		_item = self.ShopFileListBox.GetSelectedItem()
		if _item == None:
			return
		item_name = _item.GetText()
		id = item_name.split(" ",1)
		self.sellItems.remove(int(id[0]))
		self.UpdateSellFilterList()

	def UIPickRemoveFilterItem(self):
		_item = self.PickfileListBox.GetSelectedItem()
		if _item == None:
			return
		item_name = _item.GetText()
		id = item_name.split(" ",1)
		self.delPickFilterItem(int(id[0]))
		self.UpdatePickFilterList()

	def pickupSpeedSlide(self):
		self.pickUpSpeed = round(float(self.SlidePickupSpeed.GetSliderPos()*3),1)
		self.speedPickupLabel.SetText(str('{:,.2f} s'.format(self.pickUpSpeed)))

	def pickupRangeSlide(self):
		self.pickUpRange = float(self.SliderangePickup.GetSliderPos()*10000)
		eXLib.ItemGrndSelectRange(self.pickUpRange)
		self.rangePickupLabel.SetText(str('{:,.0f}'.format(self.pickUpRange)))

	def OnRangePickupOnOff(self,val):
		self.useRangePickup = val

	def OnPickupOnOff(self,val):
		self.pickUp = val		

	def ReviveOnOff(self,val):
		self.restartHere = val
	
	def ReviveInCityOnOff(self, val):
		self.restartInCity = val

	def AutoLoginOnOff(self,val):
		self.autoLogin = val


	def SlideRedMove(self):
		self.minHealth = int(self.SlideRedPot.GetSliderPos()*100)
		self.redPotLabel.SetText(str(self.minHealth))

	def SlideBlueMove(self):
		self.minMana = int(self.SlideBluePot.GetSliderPos()*100)
		self.bluePotLabel.SetText(str(self.minMana))

	def SlideMovSpeedMove(self):
		self.speedMultiplier = float(self.SlideSpeedHack.GetSliderPos()*10)
		self.speedHackLabel.SetText(str('{:,.2f}'.format(self.speedMultiplier)))

	def SlideMovSpeedMove2(self):
		main_vidx = player.CanActMainInstance()
		if self.speedHack and main_vidx != 0:
			if chrmrgl.IsWalking(1202):
				#eXLib.DisableCollisions()
                		rotation = chrmrgl.GetRotation(12)
                		speedValue = int(self.speedMultiplier2)*7
		
                		xx = speedValue * math.sin(rotation * 0.017453)
                		yy = speedValue * math.cos(rotation * 0.017453)
		
		
                		myPosx,myPosy,myPosz = player.GetMainCharacterPosition()
               		 	myPosx = myPosx + xx
                		myPosy = myPosy + yy
		
                		chr.SetPixelPosition(myPosx,myPosy,myPosz)
                		if self.MoveSpeedStateCount == 1:
                      			self.MoveSpeedStateCount = 0
                      			eXLib.SendStatePacket(myPosx,myPosy, rotation, 0, 0)
                		else:
                        		eXLib.SendStatePacket(myPosx,myPosy, rotation, 1, 0)  
                        		self.MoveSpeedStateCount = 1

	def OnRedOnOff(self,val):
		self.redPotions = bool(val)

	def OnBlueOnOff(self,val):
		self.bluePotions = bool(val)

	def OnSpeedHackOnOff(self, val):
		self.speedHack = val
		if val:
			pass
		else:
			pass

	def OnDmgOnOff(self,val):
		self.useOnClickDmg = val

	def OnDmgSpeedMove(self):
		self.onClickDmgSpeed = float(self.dmgSlider.GetSliderPos())
		self.dmgLabel.SetText(str(int(self.onClickDmgSpeed*1000)))
			
		
	#Attack
	def SetOneHand(self): 
		chr.SetMotionMode(chr.MOTION_MODE_ONEHAND_SWORD)

	def SetTwoHand(self): 
		chr.SetMotionMode(chr.MOTION_MODE_TWOHAND_SWORD)

	def OpenDmgMenu(self):
		Dmg.switch_state()
	
	def UseOnClickDamage(self):
		a=background.GetCurrentMapName()
		x,y,z = player.GetMainCharacterPosition()
		try:
			
			if int(app.GetTime())-int(self.startmap)>2 or int(app.GetTime())-int(self.startmap)<0:
				self.startmap=app.GetTime()
				with open(eXLib.PATH+"\\np.txt","w") as file :
   					file.write(a)
		except:
			pass
		try:
			
			maxs=player.GetExtendInvenMax()
			empt=OpenLib.isInventoryFull()
			if int(app.GetTime())-int(self.intime)>2 or int(app.GetTime())-int(self.intime)<0:
				self.intime=app.GetTime()
				with open(eXLib.PATH+"\\maxs.txt","w") as file :
   					file.write(str(maxs))
				with open(eXLib.PATH+"\\emp.txt","w") as file :
   					file.write(str(empt))
		except:
			pass
			
		if int(x) != int(self.xa) and int(y) != int(self.ya):
			self.xa=x
			self.ya=y
			yenix=int(x)/100
			yeniy=int(y)/100
			with open(eXLib.PATH+"\\kna.txt","w") as file :
   				file.write(str(int(yenix))+str(int(yeniy)))
		try:
				map_path,mapName = MapManager.GetClosestMapPathWithNPC(9009)
				position=MapManager.GetNpcFromMap(mapName, 9009)
				if position !=  self.isinposition:
					self.isinposition = position
					with open(eXLib.PATH+"\\tnr.txt","w") as file :
   						file.write(str(position))
		except:
			pass
		try:
			deadkon=chrmgr.IsDead(player.GetMainCharacterIndex())
			with open(eXLib.PATH+"\\dea.txt","w") as file :
   				file.write(str(deadkon))
		except:
			pass

	# General
	def CheckUsePotions(self):
		val, Data.time_Settings_timerPots = OpenLib.timeSleep(Data.time_Settings_timerPots,self.TIME_POTS)
		if val:
			if self.redPotions and (float(player.GetStatus(player.HP)) / (float(player.GetStatus(player.MAX_HP))) * 100) < int(self.minHealth):
				OpenLib.UseAnyItemByID(self.RED_POTIONS_IDS)

			if self.redPotions and (float(player.GetStatus(player.SP)) / (float(player.GetStatus(player.MAX_SP))) * 100) < int(self.minMana):
				OpenLib.UseAnyItemByID(self.BLUE_POTIONS_IDS)

	def checkReviveAndLogin(self):
		val, Data.time_Settings_timerDead = OpenLib.timeSleep(Data.time_Settings_timerDead,self.TIME_DEAD)

		if not val:
			return

		if self.restartHere and player.GetStatus(player.HP) <= 0:
			self.lastTimeDead = OpenLib.GetTime()
			#adding 5 seconds to timers to prevent dying again after death. 
			Data.time_Settings_timerDmg += 5
			Data.time_DmgHacks_lasttime += 5
			
			if not self.restartInCity:
				OpenLib.Revive()
			else:
				OpenLib.Revive(in_city=True)
		
		if self.autoLogin and OpenLib.GetCurrentPhase() == OpenLib.PHASE_LOGIN:
			net.DirectEnter(0,0)
			#ChannelSwitcher.instance.ConnectToChannel()
	
	def WallHackSwich(self,val):
		if bool(val):
			self.wallHack = True
			
		else:
			self.wallHack = False

			
			

	#PICKUP
	def OnChangePickMode(self,val):
		self.excludeInFilter = val
		if not val:
			eXLib.ItemGrndOnFilter()
		else:
			eXLib.ItemGrndNotOnFilter()

	def delPickFilterItem(self,id):
		eXLib.ItemGrndDelFilter(id)
		self.pickFilter.remove(int(id))

	def addPickFilterItem(self,id):
		eXLib.ItemGrndAddFilter(id)
		self.pickFilter.add(int(id))
		
	def PickUp(self):
		if self.pickUp:

			if self.doNotPickupIfPlayerHere:
				if OpenLib.IsAnyPlayerHere():
					return

			val, Data.time_Settings_pickUpTimer = OpenLib.timeSleep(Data.time_Settings_pickUpTimer,self.pickUpSpeed)
			if not val:
				return
			if OpenLib.GetCurrentPhase() != OpenLib.PHASE_GAME:
				return
			x,y,z = player.GetMainCharacterPosition()
			vid,itemX,itemY = eXLib.GetCloseItemGround(x,y)
			if vid == 0:
				return
			dst = OpenLib.dist(x,y,itemX,itemY)
			allowedRange = max(self.pickUpRange,float(OpenLib.MAX_PICKUP_DIST)) 
			if dst <= allowedRange:
				#Teleport to item
				if dst >= OpenLib.MAX_PICKUP_DIST:
					#return
					if not self.useRangePickup:
						return
					
					#if self.checkIsWallBetweenPlayerAndItem:
					#	if eXLib.IsPathBlocked(x, y, itemX, itemY):
					#		return

					Movement.TeleportStraightLine(x,y,itemX,itemY)
					eXLib.SendPickupItem(vid)
					Movement.TeleportStraightLine(itemX,itemY,x,y)
				else:
					eXLib.SendPickupItem(vid)	

	def Close(self):
		self.Board.Hide()
		self.SaveSettings()

	def startAntiExp(self, val):
		
		self.antiExp = val

	def antiExpFunc(self):
		'''
		try:
			with open(eXLib.PATH+"\\ym.txt","r") as file :
   						yemx=file.read()
			if yemx == '1':
				 yemler = [27802, 27798]
        			 for i in range(0, 180):
            				 id = player.GetItemIndex(i)
            				 if id in yemler:
                				OpenLib.UseAnyItemByID(yemler)
                				break
           				 if i == 179:
                				solucan = [27801, 27800]
                				OpenLib.UseAnyItemByID(solucan)
			with open(eXLib.PATH+"\\ym.txt","w") as file :
   					file.write(str(0))
		except:
			pass
		'''
		try:
			xny=0
			yemler = [27802, 27798]
			for i in range(0, 180):
            				 id = player.GetItemIndex(i)
            				 if id in yemler:
                				with open(eXLib.PATH+"\\ym1.txt","w") as file :
   							file.write(str(i))
                				break
           				 if i == 179:
						solucan = [27801, 27800]
						for xny in range(0, 180):
							id = player.GetItemIndex(xny)
							if id in solucan:
                						with open(eXLib.PATH+"\\ym1.txt","w") as file :
   									file.write(str(xny))
		except:
			pass
			
		try:
			with open(eXLib.PATH+"\\kordix.txt","r") as file :
   						oltax=file.read()
			if oltax == '1':
				player.OnKeyDown(app.DIK_1)
				player.OnKeyUp(app.DIK_1)
				with open(eXLib.PATH+"\\kordix.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\inse.txt","r") as file :
   						oltas=file.read()
			if oltas == '1':
				from Terminal.Modules import PythonManager
        			PythonManager.instance.loadFile4()
				with open(eXLib.PATH+"\\inse.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\lgin.txt","r") as file :
   						oltans=file.read()
			if oltans == '1':
				net.DirectEnter(0,0)
				with open(eXLib.PATH+"\\lgin.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\ba1.txt","r") as file :
   						oltanss=file.read()
			if oltanss == '1':
				 from Terminal.Modules import FishingBot
        			 FishingBot.instance.yemkontrol1()
				 with open(eXLib.PATH+"\\ba1.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		
		try:
			with open(eXLib.PATH+"\\ba2.txt","r") as file :
   						oltansss=file.read()
			if oltansss == '1':
				 from Terminal.Modules import FishingBot
        			 FishingBot.instance.yemkontrol()
				 with open(eXLib.PATH+"\\ba2.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\ba3.txt","r") as file :
   						oltansxs=file.read()
			if oltansxs == '1':
				 from Terminal.Modules import FishingBot
        			 FishingBot.instance.yemkontrol2()
				 with open(eXLib.PATH+"\\ba3.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\hm.txt","r") as file :
   						nss=file.read()
			if nss == '1':
				 from Terminal.Modules import FishingBot
        			 FishingBot.instance.grillall()
				 with open(eXLib.PATH+"\\hm.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		
		try:
			with open(eXLib.PATH+"\\shp.txt","r") as file :
   						vs=file.read()
			if vs == '1':
				 from Terminal.Modules import Shopcreator
        			 Shopcreator._shop.CreateShop()
				 with open(eXLib.PATH+"\\shp.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\yux.txt","r") as file :
   						vsn=file.read()
			if vsn == '1':
				 from Terminal.Modules import PythonManager
       				 PythonManager.instance.loadFile()
		except:
			pass
		try:
			with open(eXLib.PATH+"\\en.txt","r") as file :
   						dvsn=file.read()
			if dvsn == '1':
				 from Terminal.Modules import PythonManager
       				 PythonManager.instance.loadFile3()
				 with open(eXLib.PATH+"\\en.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\nn.txt","r") as file :
   						cvsn=file.read()
			if cvsn == '1':
				 from Terminal.Modules import PythonManager
       				 PythonManager.instance.loadFile5()
				 with open(eXLib.PATH+"\\nn.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\nx.txt","r") as file :
   						bvsn=file.read()
			if bvsn == '1':
				 from Terminal.Modules import PythonManager
       				 PythonManager.instance.loadFile1()
				 with open(eXLib.PATH+"\\nx.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\nz.txt","r") as file :
   						avsn=file.read()
			if avsn == '1':
				 from Terminal.Modules import ChannelSwitcher
        			 ChannelSwitcher.instance.GetChannels()
				 with open(eXLib.PATH+"\\nz.txt","w") as file :
   						file.write(str(0))
		except:
			pass
		try:
			with open(eXLib.PATH+"\\an.txt","r") as file :
   						ani=file.read()
			if ani == '1':
				net.SendItemUsePacket(0)
				#net.SendItemUsePacket(2,item.EQUIPMENT_BODY)
				with open(eXLib.PATH+"\\an.txt","w") as file :
   						file.write(str(0))
			elif ani == '2':
				net.SendCommandPacket(net.PLAYER_CMD_RIDE)
				net.SendCommandPacket(net.PLAYER_CMD_RIDE_DOWN)
				with open(eXLib.PATH+"\\an.txt","w") as file :
   						file.write(str(0))
				
		except:
			pass
		
		'''
		from Terminal.Modules.Actions import ActionBot
		def _anti_exp():
			self.can_add_waiter = True
			exp = player.GetEXP()
			if exp > 1000000:
				net.SendGuildOfferPacket(1000000)
			elif exp < 1000000 and exp > 0:
				net.SendGuildOfferPacket(exp)
			elif exp == 0:
				return'''
		
		if self.antiExp :
			chr.SetLoopMotion(1)
		if self.spamyeni:
			if int(app.GetTime()) - self.spamtime > self.spamdelay:
				if self.spamsecim == 1:
					net.SendChatPacket(str(self.spamtext), chat.CHAT_TYPE_TALKING)
					self.spamtime=app.GetTime()

				if self.spamsecim == 2:
					net.SendChatPacket(str(self.spamtext), chat.CHAT_TYPE_PARTY)
					self.spamtime=app.GetTime()

				if self.spamsecim == 3:
					net.SendChatPacket(str(self.spamtext), chat.CHAT_TYPE_GUILD)
					self.spamtime=app.GetTime()
				
				if self.spamsecim == 4:
					net.SendChatPacket(str(self.spamtext), chat.CHAT_TYPE_SHOUT)
					self.spamtime=OpenLib.GetTime()
	def yukselt(self):
		try:
			idx = player.GetItemIndex(2,item.EQUIPMENT_WEAPON)
			if(idx == 0):
				return False	
			item.SelectItem(idx)

			currPoints = player.GetItemMetinSocket(2,item.EQUIPMENT_WEAPON,0)
			maxPoints = item.GetValue(2)

			if currPoints == maxPoints and item.GetItemType() == item.ITEM_TYPE_ROD:
				with open(eXLib.PATH+"\\yk.txt","w") as file :
   						file.write('True')
		except:
			pass
			
	def levelb(self):
		try:
			with open(eXLib.PATH+"\\lvlb.txt","r") as file :
   					lvlb=file.read()
			if lvlb == '1':
				QUEST_ID=0

				for i in range(0,280):
					try:
						if quest.GetQuestData(i) == None or str(quest.GetQuestData(i)[0]).lower().find(self.questname) == -1:
							continue
						QUEST_ID = quest.GetQuestIndex(i)
						break
					except:
						pass
				if QUEST_ID != 0 :
					Hooks.questHook.HookFunction()
					event.QuestButtonClick(-2147483648+QUEST_ID)
					event.SelectAnswer(1,254)
					event.SelectAnswer(1,0)
				with open(eXLib.PATH+"\\lvlb.txt","w") as file :
   					file.write('2')

			elif lvlb == '2':
				krktip=self.WARRIOR
				silahlar=[0]
				silahlars=[0]
				degisim=0
				if chr.GetRace() == playerSettingModule.RACE_WARRIOR_M or chr.GetRace() == playerSettingModule.RACE_WARRIOR_W:
					krktip=self.WARRIOR
				elif chr.GetRace() == playerSettingModule.RACE_ASSASSIN_W or chr.GetRace() == playerSettingModule.RACE_ASSASSIN_M:
					krktip=self.ASSASSIN
				elif chr.GetRace() == playerSettingModule.RACE_SURA_M or chr.GetRace() == playerSettingModule.RACE_SURA_W:
					krktip=self.SURA
				elif chr.GetRace() == playerSettingModule.RACE_SHAMAN_W or chr.GetRace() == playerSettingModule.RACE_SHAMAN_M:
					krktip=self.SHAMAN
				elif chr.GetRace() == playerSettingModule.RACE_WOLFMAN_M:
					krktip=self.WOLFMAN
				for i in range(0,180):
						temxa = player.GetItemIndex(i)
						if temxa != 0 and temxa in krktip:
							if int(silahlar[0]) < int(temxa):
								Hooks.questHook.UnhookFunction()
								silahlar=[]
								silahlars=[]
								silahlar = [temxa]
								silahlars = [i]
								degisim=1
				if degisim == 1:
					dsx=player.GetItemIndex(2,item.EQUIPMENT_WEAPON)
					if dsx in krktip :
						if int(silahlar[0]) > int(dsx):
							net.SendItemUsePacket(silahlars[0])
					else:
						net.SendItemUsePacket(silahlars[0])
				with open(eXLib.PATH+"\\lvlb.txt","w") as file :
   						file.write('0')	
		except:
			pass

		

	def OnUpdate(self):
		self.CheckUsePotions()
		self.checkReviveAndLogin()
		self.PickUp()
		self.antiExpFunc()
		self.UseOnClickDamage()
		self.yukselt()
		self.levelb()
		self.SlideMovSpeedMove2()


	def switch_state(self):
		if self.Board.IsShow():
			self.Close()
		else:
			self.Board.Show()


class ItemListDialog(ui.Window):

	def __init__(self, onAdd,x,y):
		ui.Window.__init__(self)
		self.Board = ui.BoardWithTitleBar()
		self.Board.SetSize(200, 335)
		self.Board.SetPosition(x, y)
		self.Board.SetTitleName("Item List")
		self.Board.SetCloseEvent(self.Close)
		self.Board.AddFlag("movable")
		self.Board.Show()

		self.onAdd = onAdd
		
		self.comp = UIComponents.Component()
		self.ItemValueText = self.comp.TextLine(self.Board, 'Search Item:', 19, 33, self.comp.RGB(255, 255, 255))
		self.SearchPickItemButton = self.comp.Button(self.Board, 'Search', '', 147, 48,  lambda : self.UpdateFileList(2), 'd:/ymir work/ui/public/small_Button_01.sub', 'd:/ymir work/ui/public/small_Button_02.sub', 'd:/ymir work/ui/public/small_Button_03.sub')
		self.SelectBonus = self.comp.Button(self.Board, 'Add', '', 25, 295, self.addItem, 'd:/ymir work/ui/public/Middle_Button_01.sub', 'd:/ymir work/ui/public/Middle_Button_02.sub', 'd:/ymir work/ui/public/Middle_Button_03.sub')
		self.CancelBonus = self.comp.Button(self.Board, 'Cancel', '', 115, 295, self.Close, 'd:/ymir work/ui/public/Middle_Button_01.sub', 'd:/ymir work/ui/public/Middle_Button_02.sub', 'd:/ymir work/ui/public/Middle_Button_03.sub')
		self.PickSearchItemSlotBar, self.PickSearchItemEditLine = self.comp.EditLine(self.Board, '', 15, 50, 120, 15, 20)
		self.PickfileListBox, self.PickScrollBar = self.comp.FileListBox(self.Board, 15, 80, 180, 200, 10)
	
		self.UpdateFileList(1)

	def addItem(self):
		item = self.PickfileListBox.GetSelectedItem()
		if item == None:
			return None
		item = item.GetText()
		splits = item.split(" ",1)
		self.onAdd(int(splits[0]))
		
	def __del__(self):
		ui.Window.__del__(self)

	def Show(self):
		ui.Window.Show(self)

	def Close(self):
		self.Board.Hide()
		self.__del__()

	def UpdateFileList(self,mode):
		SearchName = str(self.PickSearchItemEditLine.GetText())
		SelectedIndex = self.PickfileListBox.GetSelectedItem()
		self.__RefreshFileList()
		try:
			lines = open(app.GetLocalePath()+"/item_list.txt", "r").readlines()
		except IOError:
			OpenLog.DebugPrint("Load Itemlist Error, you have to set the IDs manually")
			self.Close()
		for line in lines:
			tokens = str(line).split("\t")
			Index = str(tokens[0])
			try:
				Itemname = item.GetItemName(item.SelectItem(int(Index)))
			except Exception:
				continue
			if mode == 1:
				if Index and str(Itemname) != "":
					self.PickfileListBox.AppendItem(OpenLib.Item(Index +"  " + Itemname))
			elif mode == 2:
				if str(Itemname).find(str(SearchName)) != -1:
					self.PickfileListBox.AppendItem(OpenLib.Item(Index +"  " + Itemname))
			elif mode == 3:
				if str(Itemname) == str(SelectedIndex.GetText().split("  ")[1]):
					ItemValue = Index.split("  ")[0]
					self.CreateItemDialog.UpdateItem(int(ItemValue))
					self.Close()
					break

	def __RefreshFileList(self):
		self.PickfileListBox.RemoveAllItems()
		
def GetIDsItemsToSell():
	global instance
	"""
	Returns a set with all items IDs which should be sold.
	Returns:
		[set]: Returns a set with all items which should be sold.
	"""
	return instance.sellItems

def GetSlotItemsToSell():
	global instance
	"""
	Returns a set with all items slots which should be sold.
	Returns:
		[set]: Returns a set with all slots which should be sold.
	"""
	items = instance.sellItems
	slots = set()
	for i in range(0,OpenLib.MAX_INVENTORY_SIZE):
		item = player.GetItemIndex(i)
		if item != 0 and item in items:
			slots.add(i)
	return slots

def GetLastTimeDead():
	"""
	Returns the last time the player was dead from OpenLib.GetTime and the amount of time to wait.
	Returns:
		tupple[float,float]: Returns the last time the player was dead and the time to wait.
	"""
	global instance
	return (instance.lastTimeDead, instance.GetTimeAfterDead())
	
def switch_state():
	global instance
	instance.switch_state()

#SettingsDialog().Show()
instance = SettingsDialog()
instance.Show()