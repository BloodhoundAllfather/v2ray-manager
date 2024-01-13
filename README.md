# About The Project
`v2ray-manager` is a command line tool for managing v2ray users via Python3. You can add, delete and list users, see v2ray config file and also restart the `v2ray` service. It also generates `VMESS` URIs to be used in any application. It's written in a single Python3 script file.

The script has five global variables that four of them can be read from a file. If you don't want to have a configuration file, you can just change the values inside the script. The global variables are:
```python
CONFIG_FILE = "/usr/local/etc/v2ray/config.json"	# v2ray config file
LIST_FILE = "list"		# file to store users and their info
SERVER_IP = "12.34.56.78"	# the server's ip address
APPLICATION_CONFIG = "config"	# configuration file of the script
SERVER_NAME = "My VPN Server"	# The connection name inside the VMESS URI
```
If the `APPLICATION_CONFIG` file couldn't be found, the default values will be used. If you want to read these values from a file, the sample config file should be like this:
```
config = /usr/local/etc/v2ray/config.json
list = list
ip = 12.34.56.78
name = My Awesome Server
```
`config` will set `CONFIG_FILE`, `list` will set `LIST_FILE`, `ip` will set `SERVER_IP` and `name` will set `SERVER_NAME`.
The application's configuration file is called `config` and should be next to the script. Obviously that also can be changed from the script.

P.S. I pushed the `.vscode` folder intentionally, in case someone wants to debug the script.

# Usage
```
Usage:
	Add new user:		python3 v2rayman.py add USERNAME
	Delete existing user:	python3 v2rayman.py delete USERNAME
	List users:		python3 v2rayman.py list
	Print v2ray config:	python3 v2rayman.py config
	Restart v2ray service:	python3 v2rayman.py restart
	Show user details:	python3 v2rayman.py info USERNAME
```

### Add User
To add a user to the v2ray config file, use `add` parameter. The `v2ray` service needs to be restarted after adding a user (needs `root` access). It also generates VMESS URI for the user.
`python3 v2rayman.py add "Michael Grey"`
```
User Four has been added: b5b3373e-3e96-468d-90fa-01561e8828fb
vmess://eyJhZGQiOiIxMi4zNC41Ni43OCIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiJiNWIzMzczZS0zZTk2LTQ2OGQtOTBmYS0wMTU2MWU4ODI4ZmIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjIyMCIsInBzIjoiTXkgQXdlc29tZSBTZXJ2ZXIgKFVzZXIgRm91cikiLCJzY3kiOiJjaGFjaGEyMC1wb2x5MTMwNSIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
```

### Delete User
To delete a user from the v2ray config file, use `delete` parameter. The `v2ray` service needs to be restarted after deleting a user (needs `root` access).
`python3 v2rayman.py delete "Michael Grey"`

### List Users
To see list of current users and more info about them, use `list` parameter. It shows the usernames, IDs, number of days passed since their creation and the date of creation.
`python3 v2rayman.py list`
```
1	User One	e29ad5ef-67da-4f8c-813f-676b94a960e4	12 days	01/01/2024 16:11:41
2	User Two	be99079c-cd63-40d5-b7eb-f37003ac02b3	6 days	07/01/2024 13:51:56
```

### Print v2ray Config File
To print the `v2ray` configuration file, just use `config` parameter.
`python3 v2rayman.py config`

### Restart v2ray Service
To restart the `v2ray` service, just use `restart` parameter (needs `root` access).
`python3 v2rayman.py config`

### Show User Information
To show information about a given user, just use `info` parameter.
`python3 v2rayman.py info "Michael Grey"`
```
ID: b5b3373e-3e96-468d-90fa-01561e8828fb
Username: Michael Grey
Created At: 13/01/2024 22:15:01
URI: vmess://eyJhZGQiOiIxMi4zNC41Ni43OCIsImFpZCI6IjAiLCJhbHBuIjoiIiwiZnAiOiIiLCJob3N0IjoiIiwiaWQiOiJiNWIzMzczZS0zZTk2LTQ2OGQtOTBmYS0wMTU2MWU4ODI4ZmIiLCJuZXQiOiJ0Y3AiLCJwYXRoIjoiIiwicG9ydCI6IjIyMCIsInBzIjoiTXkgQXdlc29tZSBTZXJ2ZXIgKFVzZXIgRm91cikiLCJzY3kiOiJjaGFjaGEyMC1wb2x5MTMwNSIsInNuaSI6IiIsInRscyI6IiIsInR5cGUiOiJub25lIiwidiI6IjIifQ==
```

# License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/BloodhoundAllfather/v2ray-manager/blob/master/LICENSE) file for details
You can use the code anyway you want but if you are going to add some features to it, please push to the project so that others can use it.


