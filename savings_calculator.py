import requests
import json
import sys
import os
from requests.auth import HTTPBasicAuth

'''
USAGE INSTRUCTIONS
Two options:
1. distancegoogle.py <reservation file> <dump file> <percentage>
Input 1: name of the json file containing the relevant reservation
addresses. Has to be in the same format as how they've been so far.
Input 2: name of the json file containing the relevant dump
addresses. Also has to be in the same format. 
Input 3: percentage of respondents who would have driven to the 
dump themselves. Write 78, not 0.78 or 78%.

2. distancegoogle.py <reservation file> <dump file>
Here, we don't give a dump file name, and instead just write
the dump coordinates into the code. Leaving this as an option
because I wasn't sure whether json dump files make sense from
your side.

Note for future development: depending on how many cities you're
working with, it could make sense to write the dump location(s)
for each city into the code. Then, we could just specify city name
in the command-line. For example, we could write
distancegoogle.py reservations.json Orinda 78
and program it to use Orinda's dump location when reading Orinda.

Also, for extended use, you're going to need to either make 
your own Google Distance Matrix API key (I think I'm on some
sort of free trial) or convert this to the RouteXL API
'''


# check the command-line arguments
if len(sys.argv) == 3:
	reservation_list = sys.argv[1]
	dump_list = ["37.860844,-122.208877"] # Orinda right now
	scale = int(sys.argv[2]) / 100
elif len(sys.argv) == 4:
	reservation_list = sys.argv[1]
	dump_list = sys.argv[2]
	scale = int(sys.argv[3]) / 100
else:
	print("Check usage instructions in comments")
	sys.exit(1)



# endpoint URL
url = "https://maps.googleapis.com/maps/api/distancematrix/json"

# keep track of the sum of all distances
total_distance = 0

# recording errors
error_type = 0
error_message = 0

# API key
key = os.environ.get(FIRE_ASIDE_KEY)



# turn a JSON file entry into the form the Google API wants.
# note that this will have to be rewritten if we start
# working with differently formatted JSON files. the
# assumed format is: reservation_id, longitude, 
# latitude, address, load size. would also have to 
# modify if we move back to the RouteXL API.

def reformat(entry):
	latitude = str(entry["group_series_1"])
	longitude = str(entry["group_series_0"])
	origins = latitude + "," + longitude
	return origins


# find the distance from a given address to its nearest dump, given a list of dumps

def find_distance(entry, dump_list):

	# format we get in the JSON file is not the format
	# the API wants
	entry = reformat(entry)

	# for each entry, we find the distance to each possible
	# dump, and choose the nearest one.
	shortest_distance = 10 ** 7
	for dump in dump_list:

		# if we're working with a json file dump list,
		# we have to reformat. if we coded the list in,
		# it's already formatted correctly.
		if len(sys.argv) == 4:
			dump = reformat(dump)

		# send a request to the Google Distance Matrix
		# API to find distance in meters from entry
		# to dump
		params = {
			"destinations":dump,
			"origins":entry,
			"units":"imperial",
			"key":key
		}
		response = requests.get(url, params=params)
		if response.status_code == 200:
			data = response.json()
			distance = data["rows"][0]["elements"][0]["distance"]["value"]
			current_distance = distance
		
		# check for error
		else:
			global error_type
			error_type = response.status_code
			global error_message
			error_message = response.text
			current_distance = -1

		if current_distance == -1:
			return -1
		if current_distance < shortest_distance:
			shortest_distance = current_distance

	return shortest_distance



# iterate through file entries. for each one, 
# find the distance to the nearest dump, then
# add that value to the sum of all distances.
with open(reservation_list, mode="r") as file:
	data = json.load(file)
	for entry in data:
		if find_distance(entry, dump_list) == -1:
			print(error_type, error_message)
			break
		else:
			distance = find_distance(entry, dump_list)
			print(distance) # (un-comment this line to watch
			# the calculations happening
			total_distance += distance

# scale distance by proportion of customers who would have driven, then convert from meters to miles
final_distance = total_distance * scale * 0.000621371

# use this number to find gallons of gas saved (justification in document)
gas_gallons = 0.0384 * final_distance

# then find pounds CO2 saved
carbon_pounds = 22.44 * gas_gallons

# print final answer
print(final_distance, "miles saved")
print(gas_gallons, "gallons of gas saved")
print(carbon_pounds, "pounds of CO2 saved")


