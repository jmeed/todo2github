from distutils.core import setup
import sys
import os
import fnmatch
import re
from github import *
from configs import *

gh = GitHub(username=user, password=password)

path = '.'

configfiles = [os.path.join(dirpath, f)
	for dirpath, dirnames, files in os.walk(path)
	for extension in extensions
	for f in fnmatch.filter(files, extension)]

import fileinput
for fileName in configfiles:
	count = 0
	search = fileinput.input(fileName, inplace = 1)
	for line in search: #TODO [GH12]: to
		line = line.rstrip()  # remove '\n' at end of line
		if re.match("(.*)(\#)TODO:(.*)", line):
			todoInfo= re.sub("(.*)(\#)TODO:\s","", line)
			fileNameShort = re.sub("\.\/","", fileName)
			subject = fileNameShort+":"+str(count)+" " + todoInfo
			# make url that can link to specific place in file
			url = "https://github.com/"+projectAccount + "/" + project + "/blob/master/" + fileNameShort + "#L" + str(count)
			r = gh.repos(projectAccount)(project).issues.post(title=subject, body=url)
			line = re.sub("(\#)TODO:","#TODO [GH"+str(r.number)+"]:", line)
		print(line) #write line back to file
		count = count + 1

