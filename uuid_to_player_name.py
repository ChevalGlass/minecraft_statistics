#!/usr/bin/python3.7

# Get Minecraft account names based on uuid and save it to json array on disk.
# Currently this script makes a couple assumptions.
#	- The last name in the response is the most recent. (Doesn't check the date field.)
#	- You have the uuid(s) you want to look up in the standard form (with dashes).

# Mojang API for getting the player names.
#GET https://api.mojang.com/user/profiles/<uuid>/names
# note: they don't want dashes in the uuid.

import os
import json
import requests

def requestPlayerNameFromUUID(uuid):
	response = requests.get('https://api.mojang.com/user/profiles/'+uuid.replace('-', '')+'/names')
	return json.loads(response.text)[-1]['name']

def getPlayerNamesFromUuids(uuids):
	player_names = {}

	for player in uuids:
		player_names[player] = requestPlayerNameFromUUID(player)

	return player_names
