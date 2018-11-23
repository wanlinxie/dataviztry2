
keyword = "facebook"
urlfile = "2017urls.txt"
newfile = "2017"+keyword+".txt"


if __name__ == "__main__":
	fr = open(urlfile,'r')
	fw = open(newfile,'w')
	count = 0
	for line in fr:
		# look for mention of fb
		if keyword in line:
			fw.write(line)
			count += 1

	print("found: "+str(count))
	fw.close()
	fr.close()
