import os

def make_subfolders(top_dir):
    directs = []
    for root, dirs, files in os.walk(top_dir):   #collects the name of all of the .txt file for later use
	for file in files:
	    if file.endswith(".txt"):
		directs.append(file[:-4])
    for name in directs:                
	if not os.path.exists(top_dir + "/%s" %name): #makes a new directory from the .txt name if one doesn't exist
	    os.mkdir(top_dir + "/%s" %name)
        text = open("%s.txt" %name).read()          #reads in the .txt file and splits it by paragraph
	if len(text) > 0:
	    docs = text.split("%EOS%")
	else:                                #if it has no text we skip to avoid erroring out
	    continue
	for i in range(0, len(docs)):             #write the file in the new subfolder
	    file = open("%(name)s/%(name)s%(number)d.txt" %{"name": name, "number": i}, "w")
	    file.write(docs[i])
	    file.close()
