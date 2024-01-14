#!/usr/bin/python3
# A command line tool for managing v2ray users via Python3
# You can add/delete/list users from the V2ray config file
# This applies to inbounds -> settings -> clients
# 
# 
# https://github.com/BloodhoundAllfather/v2ray-manager

import json, sys, uuid, base64, subprocess
from datetime import datetime
#------------------------------------------------------------------------------------------------------------------------
# if the APPLICATION_CONFIG file doesn't exists, the default values will be used
CONFIG_FILE = "/usr/local/etc/v2ray/config.json"	# v2ray config file
LIST_FILE = "list"									# file to store users and their info
SERVER_IP = "12.34.56.78"							# the server's ip address
APPLICATION_CONFIG = "config"						# configuration file of the script
SERVER_NAME = "My VPN Server"						# The connection name inside the VMESS URI
#------------------------------------------------------------------------------------------------------------------------
# Read v2ray config file
def readConfig():
	f = open(CONFIG_FILE, "r")
	jsonObject = json.load(f)
	f.close()
	return jsonObject
#------------------------------------------------------------------------------------------------------------------------
# Read list file
def readList():
	try:
		f = open(LIST_FILE, "r")
		jsonObject = json.load(f)
		f.close()
		return jsonObject
	except FileNotFoundError:
		print("List file doesn't exists. Creating empty one...")
		f = open(LIST_FILE, "w")
		f.write("{\"users\": []}")
		f.close()
		return []
	except:
		print("An error occured at reading the list file")
		exit(0)
#------------------------------------------------------------------------------------------------------------------------
# Write JSON object to v2ray config file
def writeConfig(config):
	configStr = json.dumps(config, indent = 2)
	f = open(CONFIG_FILE, "w")
	f.write(configStr)
	f.close()
#------------------------------------------------------------------------------------------------------------------------
# Appends new id to 'clients' in the config JSON object
# If uuid isn't given, it will be generated and returned
def addUser(config, uuidv4 = ""):
	if uuidv4 == "":
		uuidv4 = str(uuid.uuid4())
	
	config["inbounds"][0]["settings"]["clients"].append({"id": uuidv4})
	return uuidv4
#------------------------------------------------------------------------------------------------------------------------
# Deletes given id from 'clients' in the config JSON object
def deleteUser(config, uuidv4):
	foundUserIndex = -1
	numberOfUsers = len(config["inbounds"][0]["settings"]["clients"])
	newUsers = []

	for i in range(numberOfUsers):
		if uuidv4 == config["inbounds"][0]["settings"]["clients"][i]["id"]:
			foundUserIndex = i
		else:
			newUsers.append(config["inbounds"][0]["settings"]["clients"][i])
	
	if foundUserIndex == -1:
		return False
	else:
		config["inbounds"][0]["settings"]["clients"] = newUsers
		return True
#------------------------------------------------------------------------------------------------------------------------
# Prints available script parameters
def printUsage():
	print("Usage:")
	print("\tAdd new user: \t\tpython3 v2rayman.py add USERNAME")
	print("\tDelete existing user: \tpython3 v2rayman.py delete USERNAME")
	print("\tList users: \t\tpython3 v2rayman.py list")
	print("\tPrint v2ray config: \tpython3 v2rayman.py config")
	print("\tRestart v2ray service: \tpython3 v2rayman.py restart")
	print("\tShow user details: \tpython3 v2rayman.py info USERNAME")
	print("")
#------------------------------------------------------------------------------------------------------------------------
# Check UUID
def checkUUID(uuidv4):
	try:
		version = uuid.UUID(uuidv4).version
		return True
	except:
		return False
#------------------------------------------------------------------------------------------------------------------------
def generateVmessUri(uuidv4, username, config):
	name = SERVER_NAME + " ({})".format(username)
	port = str(config["inbounds"][0]["port"])
	protocol = config["inbounds"][0]["protocol"]
    
	config = '{\"add\":\"' + SERVER_IP +  '\",\"aid\":\"0\",\"alpn\":\"\",\"fp\":\"\",\"host\":\"\",\"id\":\"' + uuidv4 + '\",\"net\":\"tcp\",\"path\":\"\",\"port\":\"' + port + '\",\"ps\":\"' + name + '\",\"scy\":\"chacha20-poly1305\",\"sni\":\"\",\"tls\":\"\",\"type\":\"none\",\"v\":\"2\"}'

	configBytes = config.encode("ascii")
	encoded = base64.b64encode(configBytes)
	encodedString = encoded.decode("ascii")

	return protocol + "://" + encodedString
#------------------------------------------------------------------------------------------------------------------------
def writeNewUserToList(listJson, username, uuidv4, uri):
	now = datetime.now()
	dateStr = now.strftime("%d/%m/%Y %H:%M:%S")

	listJson["users"].append({"id": uuidv4, "username": username, "uri": uri, "createdAt": dateStr})
	
	configStr = json.dumps(listJson, indent = 2)
	f = open(LIST_FILE, "w")
	f.write(configStr)
	f.close()
#------------------------------------------------------------------------------------------------------------------------
def deleteUserFromList(list, uuidv4):
	foundUserIndex = -1
	numberOfUsers = len(list["users"])
	newUsers = []

	for i in range(numberOfUsers):
		if uuidv4 == list["users"][i]["id"]:
			foundUserIndex = i
		else:
			newUsers.append(list["users"][i])
	
	if foundUserIndex == -1:
		return False
	else:
		list["users"] = newUsers
		return True
#------------------------------------------------------------------------------------------------------------------------	
# Write JSON object to v2ray config file
def writeList(list):
	listStr = json.dumps(list, indent = 2)
	f = open(LIST_FILE, "w")
	f.write(listStr)
	f.close()
#------------------------------------------------------------------------------------------------------------------------
# searches for the given username inside the list file and returns its id
def findUsernameGetUUID(list, username):
	for i in range(len(list["users"])):
			if username.lower() == list["users"][i]["username"].lower():
				return list["users"][i]["id"]
	return ""
#------------------------------------------------------------------------------------------------------------------------				
# searches for the given username inside the list file and returns its id
def findUsernameGetDetails(list, username):
	for i in range(len(list["users"])):
			if username.lower() == list["users"][i]["username"].lower():
				return "ID: " +         list["users"][i]["id"] + "\n" + \
					   "Username: " +   list["users"][i]["username"] + "\n" + \
					   "Created At: " + list["users"][i]["createdAt"] + "\n" + \
					   "URI: " +        list["users"][i]["uri"] + "\n"
	return ""
#------------------------------------------------------------------------------------------------------------------------				
def numberOfDaysSinceCreated(createdAt):
	if createdAt == "":
		return ""
	datetimeObj = datetime.strptime(createdAt, '%d/%m/%Y %H:%M:%S')
	now = datetime.now()
	return str(abs(now - datetimeObj).days)
#------------------------------------------------------------------------------------------------------------------------				
# Read application configuration file next the to main script
# if the file doesn't exists, then the default values will be used
def readApplicationConfig():
	try:
		f = open(APPLICATION_CONFIG, "r")
		lines = f.readlines()
		f.close()

		variables = {}

		for i in range(len(lines)):
			variable, value = lines[i].split('=')
			variable = variable.strip().lower()
			value = value.strip()
			variables[variable] = value
		
		global CONFIG_FILE
		global LIST_FILE
		global SERVER_IP
		global SERVER_NAME
		CONFIG_FILE = variables["config"]
		LIST_FILE = variables["list"]
		SERVER_IP = variables["ip"]
		SERVER_NAME = variables["name"]
	except:
		pass

#------------------------------------------------------------------------------------------------------------------------				
#      __  __          _____ _   _ 
#     |  \/  |   /\   |_   _| \ | |
#     | \  / |  /  \    | | |  \| |
#     | |\/| | / /\ \   | | | . ` |
#     | |  | |/ ____ \ _| |_| |\  |
#     |_|  |_/_/    \_\_____|_| \_|
                                                            
#------------------------------------------------------------------------------------------------------------------------				

# If no parameter is passed, exit
if len(sys.argv) == 1:
	printUsage()
	exit(0)

# Read the application config
readApplicationConfig()

# Read config file
config = readConfig()

# Read list file
list = readList()

# Add user
if sys.argv[1].lower() == "add":
	if len(sys.argv) == 3:
		# Generate UUID and add user
		uuidv4 = addUser(config)
		username = sys.argv[2]
		
		# write to the config file
		writeConfig(config)
		print(username + " has been added: " + uuidv4)
		
		# print VMESS URI
		vmessUri = generateVmessUri(uuidv4, username, config)
		print(vmessUri)
		
		# write to the list
		writeNewUserToList(list, username, uuidv4, vmessUri)
	else:
		printUsage()
		exit(0)
# Delete user
elif sys.argv[1].lower() == "delete":
	if len(sys.argv) == 3:
		username = sys.argv[2]
		uuidv4 = findUsernameGetUUID(list, username)
		if uuidv4 == "":
			print("The given username doesn't exist in the list file. Exiting...")
			exit(0)

		# delete user from the config file
		success = deleteUser(config, uuidv4)
		if success:
			print(username + " has been deleted: \t" + uuidv4)
			writeConfig(config)

			# now that user is deleted from the config file, delete it from the list file as well
			success = deleteUserFromList(list, uuidv4)
			if success:
				writeList(list)
		else:
			print("Given UUID doesn't exists in the config file")
			exit(0)
	else:
		printUsage()
		exit(0)
# List users
elif sys.argv[1].lower() == "list":
	numberOfUsers = len(config["inbounds"][0]["settings"]["clients"])
	
	for i in range(numberOfUsers):
		printed = False
		
		for j in range(len(list["users"])):
			if config["inbounds"][0]["settings"]["clients"][i]["id"] == list["users"][j]["id"]:
				days = numberOfDaysSinceCreated(list["users"][j]["createdAt"])
				print(str(i + 1) + "\t" + list["users"][j]["username"] + "\t\t" + config["inbounds"][0]["settings"]["clients"][i]["id"] + "\t" + days + " days\t\t" + list["users"][j]["createdAt"])
				printed = True
		
		if printed == False:
			days = numberOfDaysSinceCreated(list["users"][j]["createdAt"])
			print(str(i + 1) + "\t" + config["inbounds"][0]["settings"]["clients"][i]["id"] + "\t" + days + " days\t\t" + list["users"][j]["createdAt"])
	
	exit(0)
# Show all details about the given user
elif sys.argv[1].lower() == "info":
	if len(sys.argv) == 3:
		username = sys.argv[2]
		details = findUsernameGetDetails(list, username)

		if details == "":
			print("Username couldn't be found in the list file. Exiting...")
		else:
			print(details)
		exit(0)
# Dump whole v2ray config file
elif sys.argv[1].lower() == "config":
	print(json.dumps(config, indent = 2))
	exit(0)
# Restart the v2ray service
elif sys.argv[1].lower() == "restart":
	output = subprocess.check_output(["systemctl", "restart", "v2ray"])
	if len(output) > 0:
		print(output.decode('utf-8'))
	
	inputVar = input("Do you want to see the status of the v2ray service? (Y/n)")
	inputVar = inputVar.lower()
	if inputVar == 'y' or inputVar == "":
		print(subprocess.check_output(["systemctl", "status", "v2ray"]).decode('utf-8'))
	exit(0)




