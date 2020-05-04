#!/usr/bin/python3.8

# This script loads all the minecraft server stats files and
# generates html tables with all player's stats for each item in every category.

import json
import os
import sys
import optparse

# My libraries.
import replace_between
import uuid_to_player_name

time_stats = (
	'sneak_time',
	'play_one_minute',
	'time_since_death',
	'time_since_rest'
)

distance_stats = (
	'aviate_one_cm',
	'boat_one_cm',
	'climb_one_cm',
	'crouch_one_cm',
	'fall_one_cm',
	'fly_one_cm',
	'horse_one_cm',
	'minecart_one_cm',
	'sprint_one_cm',
	'swim_one_cm',
	'walk_on_water_one_cm',
	'walk_one_cm',
	'walk_under_water_one_cm'
)

pretty_text_map = {
	'aviate_one_cm' : 'distance by elytra',
	'jump' : 'jumps',
	'sleep_in_bed' : 'times slept in a bed',
	'deaths' : 'number of deaths',
	'inspect_dispenser' : 'dispensers searched',
	'inspect_dropper' : 'droppers searched',
	'inspect_hopper' : 'hoppers searched',
	'play_one_minute' : 'time played',
	'sprint_one_cm' : 'distance sprinted',
	'swim_one_cm' : 'distance swum',
	'walk_one_cm' : 'distance walked',
	'walk_under_water_one_cm' : 'distance  walked under water',
	'enchant_item' : 'items enchanted',
	'open_barrel' : 'barrels opened',
	'open_chest' : 'chests opened',
	'open_enderchest' : 'ender chests opened',
	'open_shulker_box' : 'shulker boxes opened',
	'play_noteblock' : 'note blocks played',
	'tune_noteblock' : 'note blocks tuned'
}

# Load all player stats, given the directory, into a highly nested dictionary.
def load_stats(stats_dir):
	#  _                 _      _ ___  ___  _  _ 
	# | |   ___  __ _ __| |  _ | / __|/ _ \| \| |
	# | |__/ _ \/ _` / _` | | || \__ \ (_) | .` |
	# |____\___/\__,_\__,_|  \__/|___/\___/|_|\_|

	player_stats = {}
	#player_category = {}
	#player_item = {}

	categories = {
		'broken' : [],
		'crafted' : [],
		'dropped' : [],
		'mined' : [],
		'picked_up' : [],
		'used' : [],
		'killed' : [],
		'killed_by' : [],
		'custom' : []
	}

	# For each file
	for filename in os.listdir(stats_dir):
		# Create a dictionary of stats for each player.
		with open(os.path.join(stats_dir,filename)) as file:
			parsed = json.load(file)

			player_category = {}
			#print(filename[:-5])
			for category in parsed['stats']:
				player_item = {}
				for stat in parsed['stats'][category]:
					if stat[10:] not in categories[category[10:]]:
						categories[category[10:]].append(stat[10:])
					player_item[stat[10:]] = parsed['stats'][category][stat]
				player_category[category[10:]] = player_item

			# Save all the 'minecraft:custom' stats to the dictionary.
			player_stats[filename[:-5]] = player_category
	return [player_stats, categories]

# Go through the dictionary of player stats and generate html tables.
def generate_tables(player_stats, categories):
	#   ___                       _         _____     _    _        
	#  / __|___ _ _  ___ _ _ __ _| |_ ___  |_   _|_ _| |__| |___ ___
	# | (_ / -_) ' \/ -_) '_/ _` |  _/ -_)   | |/ _` | '_ \ / -_|_-<
	#  \___\___|_||_\___|_| \__,_|\__\___|   |_|\__,_|_.__/_\___/__/

	# Create list of players.
	players = []
	for user in player_stats:
		players.append(user)

	players.sort() # Sort all the player names.

	# Sort all the items in each category.
	for category in categories:
		categories[category].sort()

	# Get player names (instead of just showing uuids)
	player_map = uuid_to_player_name.getPlayerNamesFromUuids(players)

	output = ''
	# Print a Table for each category.
	# Displaying each players stats for each.
	for category in categories:
		output +='<div class="category" id="pane_'+category+'"><br>\n\t<h2>'+category.replace('_', ' ').title()+'</h2>\n'
		output +='\t<table class="" id="'+category+'">\n\t\t<thead>'
		# Print table header for each category.
		output +='<tr><th>Stat</th>'

		for player in player_map:
			output +='<th>'+player_map[player]+'</th>'
		output +='</tr></thead>\n'

		# Print out the stats for each table.
		for item in categories[category]:
			if item in pretty_text_map:
				output +='\t\t\t<tr><td>'+pretty_text_map[item].replace('_', ' ').title()+'</td>'
			else:
				output +='\t\t\t<tr><td>'+item.replace('_', ' ').title()+'</td>'
			for player in player_map:
				stat = player_stats.get(player, {}).get(category, {}).get(item, 0)
				if category == 'custom':
					if item in time_stats:
						stat = format_time(stat)
					elif item in distance_stats:
						stat = format_distance(stat)
					else:
						stat = format(stat, ',')
					output +='<td>'+str(stat)+'</td>'
				else:
					output +='<td>'+format(player_stats.get(player, {}).get(category, {}).get(item, 0), ',')+'</td>'
			output +='</tr>\n'
		output +='\t\t</tbody>\n\t</table>\n</div>\n'
	return output

# Using my library, "dump" the generated html into the template file.
def update_html(file, html):
	#  _   _          _      _         _  _ _____ __  __ _    
	# | | | |_ __  __| |__ _| |_ ___  | || |_   _|  \/  | |   
	# | |_| | '_ \/ _` / _` |  _/ -_) | __ | | | | |\/| | |__ 
	#  \___/| .__/\__,_\__,_|\__\___| |_||_| |_| |_|  |_|____|
	#       |_|                                               
	replace_between.replace_between('<!-- Starts Stats -->', '<!-- End Stats -->', file, html)


def format_time(stat):
	# Go through some checks to find the time range.
	if stat >= 0 and stat < 20:				# number is within the tick range.
		return format(stat, '.2f')+'ticks'	# format to ticks.
	elif stat >= 20 and stat < 1200:		# number is within the second range.
		return format(stat / 20, '.2f')+'s'	# format to seconds.
	elif stat >= 1200 and stat < 72000:		# number is within the minute range.
		return format(stat / 20 / 60, '.2f')+'m' # format to minutes.
	elif stat >= 72000 and stat < 1728000:	# number is within the hour range.
		return format(stat / 20 / 60 / 60, '.2f')+'h' # format to hours.
	elif stat >= 1728000:	# number is within the day range.
		return format(stat / 20 / 60 / 60 / 24, '.2f')+'d'
	else:	# Less than zero! Return the stat.
		return stat

def format_distance(stat):
	# Go through some checks to find the distance range.
	if stat >= 0 and stat < 100:	# number is within the tick range.
		return format(stat, '.2f')+'cm' # format to Centimeters.
	elif stat >= 100 and stat < 1000:	# number is within the second range.
		return format(stat / 100, '.2f')+'m'# format to Meters.
	elif stat >= 1000:	# number is within the minute range.
		return format(stat / 100000, '.2f')+'km' # format to Kilometers.
	else:	# Less than zero! Return the stat.
		return stat

def main():

	# handle command line options and args
	version = "%prog 1.0"
	usage = "usage: %prog -s STATS_DIR -o OUTPUTFILE"
	description = "Generates html tables from minecraft player statistic files."
	parser = optparse.OptionParser(version=version, usage=usage, description=description)
	parser.add_option("-s", "--stats_dir", dest="stats_dir", default="./", help="Specify the directory of the stats/<uuid>.json files. Default: Current directory.")
	parser.add_option("-o", "--outputfile", dest="outputfile", default="stdout", help="Where the output should be put. Default: stdout")
	(options, args) = parser.parse_args()

	# Load stats from files.
	player_stats, categories = load_stats(os.path.join(options.stats_dir))

	# Generate the html code for each table.
	tables = generate_tables(player_stats, categories)

	if options.outputfile == 'stdout':
		print(tables)
	else:
		# Send generated html code to html.
		update_html(os.path.join(options.outputfile), tables)


main() # Start Script
