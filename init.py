#Responsible for inputing the right methods
#DON'T RUN SCRIPTS FROM ON HERE

import sys, os
import dBUyLqM  as _chat
import jVLGMMuEab  as _player
import gDOnKFCx  as _net
import JFWsaHXjj  as _chrmgr
import opiEviBil  as _nonplayer
import OfHgOY  as _wndMgr
import maBLd  as _quest
import IJlqzUG  as _ranking
import HFIFX  as _skill
import BHGLlCJB  as _exchange
import RAfmSGFRd  as _guildbank
import FJIi  as _mail
import lTDoYyASP  as _messenger
import zMXjbBp  as _miniMap
import KMDLcsa  as _safebox
import tkxG  as _shop
import PIxNJ  as _mount
import HHsOHCDgrDCpDRGQIQ  as _premiumPrivateShop
import wZSfELcB  as _textTail
import bSW  as _ime 
import  nGeHgwVXHMcJA  as _systemSetting
import FWPuLzD  as _rootlib
import GSalHiG  as _grpText
import PoxuGprE  as  _grpImage
import Ews  as _grp
import chrmrgl

import eXLib
import chr,app

sys.modules['player'] = _player
sys.modules['net'] = _net
sys.modules['chat'] = _chat
sys.modules['chrmgr'] = _chrmgr
sys.modules['nonplayer'] = _nonplayer
sys.modules['quest'] = _quest
sys.modules['ranking'] = _ranking
sys.modules['exchange'] = _exchange
sys.modules['guildbank'] = _guildbank
sys.modules['mail'] = _mail
sys.modules['messenger'] = _messenger
sys.modules['miniMap'] = _miniMap
sys.modules['mount'] = _mount
sys.modules['premiumPrivateShop'] = _premiumPrivateShop
sys.modules['safebox'] = _safebox
sys.modules['shop'] = _shop
sys.modules['textTail'] = _textTail
sys.modules['ime'] = _ime
sys.modules['systemSetting'] = _systemSetting
sys.modules['rootlib'] = _rootlib
sys.modules['wndMgr'] = _wndMgr
sys.modules['grpText'] = _grpText
sys.modules['grpImage'] = _grpImage
sys.modules['grp'] = _grp
sys.modules['skill'] = _skill


def SetSingleDIKKeyState(key,state):
    if state == 1:
        _player.OnKeyDown(key)
    else:
        _player.OnKeyUp(key)

def SetAttackKeyState(state):
    if state == 1:
        _player.OnKeyDown(app.DIK_SPACE)
    else:
        _player.OnKeyUp(app.DIK_SPACE)

setattr(chr, 'GetPixelPosition', eXLib.GetPixelPosition)
setattr(chr, 'MoveToDestPosition', eXLib.MoveToDestPosition)
setattr(_net, 'GetMainActorVID', _player.GetMainCharacterIndex)
setattr(_player, 'SetSingleDIKKeyState', SetSingleDIKKeyState)
setattr(_player, 'SetAttackKeyState', SetAttackKeyState)


#Set Path
folder = eXLib.PATH+"Terminal"
command = 'mklink /d Terminal "' + folder +'"'

sys.path.append(os.path.join(eXLib.PATH))
sys.path.append(os.path.join(eXLib.PATH,'Terminal'))
sys.path.append(os.path.join(eXLib.PATH,'Terminal', 'lib'))
sys.path.append(os.path.join(eXLib.PATH,'Terminal', 'Modules'))
