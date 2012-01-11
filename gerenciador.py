import os,sys,urllib,yaml,shutil,subprocess

##=====COMMANDS FUNCTIONS=====##

##=====listrepo=====##
#This function access the content of the file
#"content.arp" in the repo and print the structure
#of the componet that there are in the repo.
def listrepo():
	file_url = repo_url + "content.arp"
	
	print "Trying to access \'" + file_url + "\'..."
	
	file = urllib.urlopen(file_url)
	content = file.read()
	file.close()

	yaml_obj = {}
	yaml_obj = yaml.load(content)
	
	for x in structure:
		print x.upper() + ":"
		if yaml_obj[x] != None:
			for y in sorted(yaml_obj[x].iterkeys()):
				print "  " + y + ": " + yaml_obj[x][y]
			print ""
		else:
			print ""

##=====list=====##
#This function list the structure of local components
def	list():
	localpath = os.getcwd()
	for x in structure:
		mypath = localpath + "/" + x
		print x.upper() + ":"
		if os.path.isdir(mypath):
			tmpdirlist = os.listdir(mypath)
			for y in tmpdirlist:
				if os.path.isdir(mypath + "/" + y):
					print " ", y, "-", getDescriptionText(mypath + "/" + y)
		print ""

##=====get=====##
#This function try to get the component from the repo
#if t find, the function dowanload the component package
#and unpack it.
#if not, returns error.
def get(type, name):
	if type != None:
		list = []
		list.append(type)
		component = findRepoComponent(name, list)
	else:
		component = findRepoComponent(name, structure)
	if component != None:
		target = os.getcwd() + "/" + component.split("/")[-2] + "/"
		fileName = component.split("/")[-1]
		try:
			download(component, target, fileName)
		except:
			print "!!! Error: Component " + name + " not found"
			sys.exit(1)
	else:
		print "!!! Error: Component " + name + " not found"
		sys.exit(1)
	print "Component " + name + " was downloaded successfully."
	unpack(target + fileName)

##=====put=====##
#This function was not implemented.
def put(type, name):
	print "Sorry!! Function not yet implemented."
	sys.exit(0)

##=====pack=====##
#This function pack the component or platfomrs.
#It compress all files in a arppack file.
def pack(type, name):
	source_files = ""
	if type == None and name == None:
		localpath = os.getcwd()
		for x in structure:
			mypath = localpath + "/" + x + "/"
			if os.path.exists(mypath):
				source_files = source_files + x + "/ "
		source_files = source_files + "Makefile"
		package_file = "all.arppack"
		
	elif type == None and name != None:
		component = findLocalComponent(name, structure)
		if component != None:
			source_files = component.split("/")[-3] + "/" + component.split("/")[-2] + "/"
			package_file = component.split("/")[-3] + "/" + name + ".arppack"
		else:
			print "!!! Error: Component " + name + " not found"
			sys.exit(1)
	else:
		list = []
		list.append(type)
		component = findLocalComponent(name, list)
		if component != None:
			source_files = component.split("/")[-3] + "/" + component.split("/")[-2] + "/"
			package_file = component.split("/")[-3] + "/" + name + ".arppack"
		else:
			print "!!! Error: Component " + name + " not found"
			sys.exit(1)


	print "Packing " + package_file + "..."
	cmd = "tar -czf " + package_file + " " + source_files
	p = subprocess.Popen(cmd, shell=True)
	print "Done."

##=====unpack=====##
#This function unpack the component package
def unpack(package):
    if not os.path.exists(package):
		print "!!! Error: Package " + package + " doesn't exists."
		sys.exit(1)
    else:
		print "Unpacking " + package + " ..."
		cmd = "tar -xzmf " + package
		p = subprocess.Popen(cmd, shell=True)
		print "Done." 

##=====create=====##
#This function create the component specified
#if exist a local copy of the template component
#the functions copy it with the new name,
#if not, the function try to get in the repo.
def create(type, name):
	list = []
	list.append(type)
	component = findLocalComponent("template", list)
	print component
	
	if component != None:
		target = os.getcwd() + "/" + type + "/"
		try:
			shutil.copytree(component, target + name)
		except:
			print "!!! Error: Component template of " + type + " not found"
			sys.exit(1)
	else:
		get(type, "template")

##=====start=====##
#This function download the start.package
#and unpack it. This File has the structure of dir
#and the main Makefile.
def start():
	target = os.getcwd() + "/"
	fileName = "start.arppack"
	try:
		download(repo_url + fileName, target, fileName)
	except:
		print "!!! Error: File start.arppack not found."
		sys.exit(1)
	unpack(target + fileName)
	print "The main structure was created successfully."

##=====repo=====##
#This function creates the "content.arp" file.
#The function gets all components in the local structure
#and put it in a YAML file.
def repo():
	localpath = os.getcwd()
	file = open(localpath + "/content.arp", "w")
	for x in structure:
		mypath = localpath + "/" + x
		file.write(x + ":\n")
		tmpdirlist = os.listdir(mypath)
		for y in tmpdirlist:
			if os.path.isdir(mypath + "/" + y):
				file.write("  " + y + ": " + getDescriptionText(mypath + "/" + y) + "\n") 
		file.write("\n")
	file.close()
	print "The file 'content.arp' was created successfully."

##=====help=====##
#This function shows the help contents.
def help():
	print """
  -c,  --create              create
  -g,  --get                 get
  -h,  --help                help
  -l,  --list                list
  -lr, --listrepo            listrepo
  -pa, --pack                pack
  -up, --put                 put
  -r,  --repo                repo
  -s,  --start               start
  -u,  --unpack              unpack
	"""

##=====AUX FUNCTIONS=====##

##=====getDescripitionText=====##
#This function gets the content of the file
#"desc.txt" and return it
#if the file doesn't exist, it returns none
def getDescriptionText(path):
	path = path + "/desc.txt"
	try:
		file = open(path, "r")
		desc = file.read()
		file.close()
		return desc
	except:
		return "No description provided."

##=====download=====##
#This function gets a file in the repo and copy it
#to the user local path
def download(source, target, name):
	webFile = urllib.urlopen(source)
	localFile = open(target + name, 'w')
	localFile.write(webFile.read())
	webFile.close()
	localFile.close()

##=====findLocalComponent=====##
#This function search for the component in the users local path
#if it founds, returns the path to the component
#if not, return none
def findLocalComponent(name, list):
	path = os.getcwd()
	tmpdirlist = os.listdir(path)
	for x in list:
		tmpdirlist = os.listdir(path + "/" + x)
		if name in tmpdirlist:
			if os.path.isdir(path + "/" + x + "/" + name):
				return path + "/" + x + "/" + name + "/"
	return None

##=====findRepoComponent=====##
#This function search for the component in the repo
#if it founds, returns the path to the component
#if not, return none
def findRepoComponent(name, list):
	file_url = repo_url + "content.arp"

	file = urllib.urlopen(file_url)
	content = file.read()
	file.close()

	yaml_obj = {}
	yaml_obj = yaml.load(content)
	
	compName = name.split(".")[0]
	
	for x in list:
		if yaml_obj[x] != None:
			if compName in yaml_obj[x].iterkeys():
				return repo_url + x + "/" + name + ".arppack"
	return None

##=====DEFINES=====##

##=====repo location=====#
repo_url = "http://www.students.ic.unicamp.br/~ra063091/repo/"

##=====list of supported commands=====#
commands={
"lr":"listrepo", "l":"list", "g":"get", "pu":"put", 
"pa":"pack", "u":"unpack", "c":"create",
"s":"start", "r":"repo", "h":"help"
}

##=====structure of plataform=====#
structure = ["platforms", "processors", "ip", "is", "sw", "wrappers"]



execline = []
#get cmdline args
cmdline=sys.argv[1:]

if cmdline==[]:
	print "!!! Error: Invalid action."
	sys.exit(1)
elif len(cmdline) > 3:
	print "!!! Error: Too many arguments"
	sys.exit(1)

	
cmd = cmdline[0]
#identify the command and add it to an execution line
if cmd[0:1]=="-" and cmd[1:2]=="-":
	values = commands.values()
	if cmd[2:] in values:
		execline.append(cmd[2:])
	else:
		print "!!! Error: " + cmd + " is an invalid action."
		sys.exit(1)

elif cmd[0:1]=="-" and cmd[1:2]!="-":
	if commands.has_key(cmd[1:]):
		execline.append(commands[cmd[1:]])
	else:
		print "!!! Error: "+cmd+" is an invalid short action."
		sys.exit(1)
else:
	print "!!! Error: " + cmd + " is an invalid action."
	sys.exit(1)


execline.extend(cmdline[1:]);
action = execline[0]

if len(execline) != 1:
	if len(execline) == 2:
		type = None
		name = execline[1]
	else:
		type = execline[1]
		name = execline[2]
else:
		type = None
		name = None
		

#switch with the functions calls
if action == "listrepo":
	listrepo()

elif action == "list":
	list()

elif action == "get":
	get(type, name)

elif action == "put":
	put(type, name)

elif action == "pack":
	pack(type, name)

elif action == "unpack":
	unpack(name)

elif action == "create":
	create(type, name)

elif action == "repo":
	repo()
	
elif action == "start":
	start()

elif action == "help":
	help()

else:
	print "!!! Error: No command found"
	sys.exit(1)


