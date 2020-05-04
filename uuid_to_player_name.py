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
import datetime

def requestPlayerNameFromUUID(uuid):
	response = requests.get('https://api.mojang.com/user/profiles/'+uuid.replace('-', '')+'/names')
	return json.loads(response.text)[-1]['name']

def getPlayerNamesFromUuids(uuids):
	player_names = {}

	for player in uuids:
		player_names[player] = requestPlayerNameFromUUID(player)

	return player_names

# Not fully implemented. Learning python datetime.
def getPlayerNamesFromUuidsWithCache(uuids):
	player_names = {}

	# Check for and load the json cache.
	if os.path.exists('player_cache.json'):
		with open('player_cache.json') as player_cache:
			player_names = json.loads(player_cache.read())["players"]

		# Check if the cache was recent. (within a ~ 1 day)

		# If it was, make sure all the uuids requested are in the cache.

		# Request any uuid's that are not in the cache.

	else: # If no cache exists, prep one.
		# Set up the framework with now as the cache date and an entry player dictionary.
		player_names = { "cache_date" : datetime.datetime.now().isoformat(), "players" : {} }

		for player in uuids:
			player_names["players"][player] = requestPlayerNameFromUUID(player)

		print('cache_date', player_cache["cache_date"])
		#if player_names["cache_date"]

		# with open('player_cache.json', 'w') as player_cache:
			# json.dump(player_names, player_cache)

#	for player in uuids:
#		player_names[player] = requestPlayerNameFromUUID(player)

	return player_names
