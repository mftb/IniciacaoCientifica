# LOL WTF BBQ

import zipfile, os, sys

# this shit adds a fucking folder to a zip file
class ZipUtilities:
    # this stuff now takes a list as arg
    def toZip(self, files_to_zip, filename):
        zip_file = zipfile.ZipFile(filename, "w")
        for file_to_zip in files_to_zip:
            if os.path.isfile(file_to_zip):
                zip_file.write(file_to_zip)
            else:
                self.addFolderToZip(zip_file, file_to_zip)
        zip_file.close()

    def addFolderToZip(self, zip_file, folder): 
        for file_ in os.listdir(folder):
            full_path = os.path.join(folder, file_)
            if os.path.isfile(full_path):
                #print "File added: " + str(full_path)
                zip_file.write(full_path)
            elif os.path.isdir(full_path):
                #print "Entering folder: " + str(full_path)
                self.addFolderToZip(zip_file, full_path)

def main():
    utilities = ZipUtilities()
    filename = "processors1.zip"
    directory = ["processors1","Makefile"]
    utilities.toZip(directory, filename)
#cmdline = sys.argv[1:]
#print cmdline
#main(cmdline[0],cmdline[1])
main()
