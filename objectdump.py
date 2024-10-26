import player
import item
from Terminal.Modules import Shopcreator

with open(eXLib.PATH+"numbers.txt","w") as file:
				file.write("")
items_ui = []
for i in range(0, 90):
			_id = player.GetItemIndex(i)

			item.SelectItem(_id)

			if _id in items_ui or _id == 0:
				continue
			item_name = item.GetItemName()
			with open(eXLib.PATH+"numbers.txt","a") as file:
				file.write(str(i)+":"+item_name+":"+str(_id)+"\n")
			items_ui.append(_id)

Shopcreator._shop.nameshop = 'Yabbie '