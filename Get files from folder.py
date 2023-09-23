import os, glob

os.chdir("C:\\Users\\DELL\\Pictures\\Captures")
for files in glob.glob("*"):
    # add format name after * to get specific type of files like .jpg or .png
    print(files)