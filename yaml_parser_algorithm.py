structure = ["platforms", "processors", "ip", "is", "sw", "wrappers"]
def LoadYAML(content):
    dic = {}
    superiorLevel = ''
    #f = open(content,"r")
    content = content.split("\n")
    # builds the dictionary
    for line in content:
        if line != "":
            # heavy wizardry \/
            [key, value] = line.split(':')
            if (key[0] == ' '):
                # removes the whitespaces before the key name
                key = key.lstrip()
                # removes the line break
                #value = value.rstrip("\n")
                # subtree
                dic[superiorLevel][key] = value
            else:
                # tree
                dic[key] = {}
                superiorLevel = key
    #f.close()

    # cleans the dictionary
    for l in structure:
        if dic[l] == {}:
            dic[l] = None

    return dic
a = open("content.arp","r")
content = a.read()
a.close()
print LoadYAML(content)
