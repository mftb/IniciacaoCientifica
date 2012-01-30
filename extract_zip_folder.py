import zipfile

def extract():
	z = zipfile.ZipFile("processors1.zip","a")
	z.extractall()
	z.close()
	
extract()
