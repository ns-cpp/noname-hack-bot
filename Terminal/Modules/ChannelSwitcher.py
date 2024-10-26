import OpenLib, UIComponents, Hooks, Settings, OpenLog
import serverInfo, background, ui, chat, net, app, introLogin # introLogin gives ServerStateChecker module


def __PhaseChangeChannelCallback(phase,phaseWnd):
    global instance
    if instance.currState == STATE_NONE:
        return
    else:
        if phase == OpenLib.PHASE_GAME:
            instance.SetStateNone()
        elif phase == OpenLib.PHASE_SELECT:
            OpenLib.SetTimerFunction(0.5,phaseWnd.SelectStart)


def getCallBackWithArg(func, arg):
    return lambda: func(arg)

STATE_NONE = 0
STATE_CHANGING_CHANNEL = 1

class ChannelSwitcher:

    def __init__(self):
        self.channels = {}
        self.currChannel = 0
        self.currState = STATE_NONE
        self.selectedChannel = 0
	self.sayi=1

    def BuildWindow(self, board):
        self.component = UIComponents.Component()
        self.Board = board

        #self.barItems, self.fileListBox, self.ScrollBar = component.ListBoxEx2(self.Board, 50, 40, 100, 150)
        #self.fileListBox.SetViewItemCount(10)

        self.refreshButton = self.component.Button(self.Board, 'Refresh', '', 90, 150, self.OnRefreshButton,
                                          'd:/ymir work/ui/public/large_Button_01.sub',
                                          'd:/ymir work/ui/public/large_Button_02.sub',
                                          'd:/ymir work/ui/public/large_Button_03.sub')

    def OnRefreshButton(self):
        self.GetChannels()
        #self.fileListBox.RemoveAllItems()
        x = 65
        y = 50
        for id in sorted(self.channels): #.items():
            self.channels[id]['btn'] = self.component.Button(self.Board, 'CH ' + str(id), '', x, y,
                                                            getCallBackWithArg(self.OnConnectButton, int(id)),
                                                            'd:/ymir work/ui/public/small_Button_01.sub',
                                                            'd:/ymir work/ui/public/small_Button_02.sub',
                                                            'd:/ymir work/ui/public/small_Button_03.sub')
            
            x += 50
            if x >= 200:
                x = 65
                y += 30

    def OnConnectButton(self,id):
        _channel = id#self.fileListBox.GetSelectedItem().text
        if not _channel:
         
            return

        if self.IsSpecialMap():
           
           return

        self.ChangeChannelById(_channel)

    def GetRegionID(self):
        # FOR EU IS 0
        return 0

    def GetServerID(self):
        server_name = OpenLib.GetCurrentServer()
        region_id = self.GetRegionID()
        if server_name:
            for server in serverInfo.REGION_DICT[region_id].keys():
                if serverInfo.REGION_DICT[region_id][server]['name'] == server_name:
                    return int(server)

    def GetChannels(self):
        del self.channels
        self.channels = {}
        region_id = self.GetRegionID()
        server_id = self.GetServerID()

        try:
            channelDict = serverInfo.REGION_DICT[region_id][server_id]['channel']
        except:
            
            return

        for channelID, channelDataDict in channelDict.items():

            self.channels[int(channelID)] = {
                'id': int(channelID),
                'name': channelDataDict['name'],
                'ip': channelDataDict['ip'],
                'port': channelDataDict['tcp_port'],
                'acc_ip' : serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]['ip'],
                'acc_port' : serverInfo.REGION_AUTH_SERVER_DICT[region_id][server_id]['port']
            }
        self.ChangeChannelById(self.sayi)

    def IsSpecialMap(self):
        maps = {
            "season1/metin2_map_oxevent",
            "season2/metin2_map_guild_inside01",
            "season2/metin2_map_empirewar01",
            "season2/metin2_map_empirewar02",
            "season2/metin2_map_empirewar03",
            "metin2_map_dragon_timeattack_01",
            "metin2_map_dragon_timeattack_02",
            "metin2_map_dragon_timeattack_03",
            "metin2_map_skipia_dungeon_boss",
            "metin2_map_skipia_dungeon_boss2",
            "metin2_map_devilsCatacomb",
            "metin2_map_deviltower1",
            "metin2_map_t1",
            "metin2_map_t2",
            "metin2_map_t3",
            "metin2_map_t4",
            "metin2_map_t5",
            "metin2_map_wedding_01",
            "metin2_map_duel"
        }
        if str(background.GetCurrentMapName()) in maps:
            return True
        return False

    def ConnectToChannel(self):
        net.Disconnect()
        net.ConnectTCP(self.selectedChannel["ip"],self.selectedChannel["port"])

    def ConnectToGame(self):
        net.SendEnterGamePacket()

    def ChangeChannelById(self, id):
        if int(id) not in self.channels:
            
            return

        self.selectedChannel = self.channels[int(id)]
        self.currState = STATE_CHANGING_CHANNEL
        self.ConnectToChannel()


    def SetStateNone(self):
        self.selectedChannel = 0
        self.currState = STATE_NONE


    def __del__(self):
        Hooks.deletePhaseCallback("channelCallback")

    def switch_state(self):
        if self.Board.IsShow():
            self.Board.Hide()
        else:
            self.OnRefreshButton()
            self.Board.Show()


def switch_state():
    instance.switch_state()

def SwitchChannel(val):
    instance.ChangeChannelById(val)

def GetNextChannel():
	current_channel = OpenLib.GetCurrentChannel()

	if not current_channel:
		return 0
	if current_channel + 1 > len(instance.channels):
		current_channel = 1
	else:
		current_channel += 1
	
	return current_channel

instance = ChannelSwitcher()
Hooks.registerPhaseCallback("channelCallback", __PhaseChangeChannelCallback)
OpenLog.DumpObject(instance)