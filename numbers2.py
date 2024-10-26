import net
import player
import eXLib
import chr

slota=0
for vid in eXLib.InstancesList:
		chr.SelectInstance(vid)
		race = chr.GetRace()
		if race == 12000:
			net.SendGiveItemPacket(vid,player.SLOT_TYPE_INVENTORY,slota,player.GetItemCount(slota))