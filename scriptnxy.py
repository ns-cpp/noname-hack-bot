from Terminal.Modules import NPCInteraction
from Terminal.Modules import Movement
from Terminal.Modules import FishingBot
import player

to_buy = []
to_sell = []
has_worms=False
has_fire=False
def testpest():
	with open(eXLib.PATH+"\\true.txt","w") as file :
   		file.write("True")


originalPosition = player.GetMainCharacterPosition()
with open(eXLib.PATH+"\\position.txt","w") as file :
   		file.write(str(originalPosition))
for i in range(0,180):
			idx = player.GetItemIndex(i)

			if 27801 == idx:
						has_worms = True
			if 27600 == idx:
						has_fire = True
if not has_worms:
		for i in range(0,int(FishingBot.instance.xrc)):
			to_buy.append(7)
if not has_fire :
			to_buy.append(1)
NPCInteraction.RequestBusinessNPCAway(to_buy,to_sell,NPCInteraction.GetFishermanShop(),callback=testpest)
#Movement.GoToPositionAvoidingObjects(FishingBot.instance.startPosition[0],FishingBot.instance.startPosition[1],callback=None,maxDist=250)

