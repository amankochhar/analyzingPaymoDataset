# Coded by Aman Kochhar
# amanskochhar@gmail.com
# For insight fellowship coding challenge 
# Please read the adjoining readme to see how this works, 
# Also the code is heavily commented to explain what purpose each function serves

import sys
import time
import sys
import os.path
import csv

# starts at the bottom 
############################################################################
# 2. PROCESSING/TIDYING DATA
# this function parses each line to the required format
# IN - lines from .txt file; OUT - addNodesEdges() or writeData()
############################################################################
def formatLines (line, build, OP1, OP2, OP3):
	# changing line to a list datatype for further processing
	line = line.split("\n")

	for i in range (len(line)):
		try: 
			timeLine, firstPerson, secondPerson, amount, message = line[i].split(",", 4)
			# stripping time for further calculations
			timeLine = timeLine.replace("T"," ")
			timeLine = timeLine.replace("Z"," ")
			timeLine = timeLine.strip()
			#print("Before stripping time: ", timeLine)
			timeLine = time.strptime(timeLine, "%Y-%m-%d %H:%M:%S")
			timeLine = int(time.mktime(timeLine))
			#print("After stripping time: ", timeLine)
		except:
			timeLine, firstPerson, secondPerson, amount, message = "chull"

		if build == True:
			addNodesEdges(firstPerson, secondPerson, timeLine, amount, message)
		else:
			writeData(firstPerson, secondPerson, OP1, OP2, OP3)

############################################################################
# 3. ADDING NODES/EDGES
# this adds the reqd nodes and edges in the edges dict
# IN - formatLines()
############################################################################
edges = dict()
def addNodesEdges (firstPerson, secondPerson, timeLine, amount, message):
	if firstPerson in edges:
		if secondPerson not in (edges[firstPerson]):
			edges[firstPerson].append(secondPerson)
			edges[firstPerson].append(timeLine)
			edges[firstPerson].append(amount)
			edges[firstPerson].append(message)
	else:
		edges[firstPerson] = [secondPerson, timeLine, amount, message]

	if secondPerson in edges:
		if firstPerson not in (edges[secondPerson]):
			edges[secondPerson].append(firstPerson)
			edges[secondPerson].append(timeLine)
			edges[secondPerson].append(amount)
			edges[secondPerson].append(message)
	else:
		edges[secondPerson] = [firstPerson, timeLine, amount, message]
	
	#uncomment below to see output
	# print("firstPerson", firstPerson,": ", edges[firstPerson])
	# print("secondPerson", secondPerson,": ", edges[secondPerson])
	
############################################################################
# 4. Feature 2
# this checks the edges to see if the feature 2 is OK
# Called by writeData()
############################################################################
def feature2(firstPerson, secondPerson):
	for person in edges[firstPerson]:
		if secondPerson in edges[person]:
			return True
		else:
			return False
		
############################################################################
# 5. Feature 3
# this checks the edges to see if the feature 3 is OK
# Called by writeData()
############################################################################

def feature3(firstPerson, secondPerson):
	for person in edges[firstPerson]:
		if secondPerson not in edges[person]:
			for people in edges[person]:
				if secondPerson not in edges[people]:
					return False
				else:
					return True
		else:
			return True


############################################################################
# 6. WRITING DATA
# this writes the results into output(1, 2, 3).txt
# IN - formatLines(); OUT - output(1,2,3).txt
############################################################################
def writeData(firstPerson, secondPerson, OP1, OP2, OP3):

	output1 = open(OP1, 'a')
	output2 = open(OP2, 'a')
	output3 = open(OP3, 'a')

	# feature 1 
	if firstPerson in edges:
		if firstPerson == "chull":
			output1.write("unverified\n")
			output2.write("unverified\n")
			output3.write("unverified\n")
		else:
			if secondPerson in edges[firstPerson]:
				output1.write("trusted\n")
				output2.write("trusted\n")
				output3.write("trusted\n")
			else:
				output1.write("unverified\n")

				if feature2(firstPerson, secondPerson) == True:
					output2.write("trusted\n")
				else:
					output2.write("unverified\n")

				if feature3(firstPerson, secondPerson) == True:
					output3.write("trusted\n")
				else:
					output3.write("unverified\n")
	else:
		output1.write("unverified\n")
		output2.write("unverified\n")
		output3.write("unverified\n")

	output1.close()
	output2.close()
	output3.close()

	# print("additional features")
	# additionalFeatures(firstPerson, secondPerson)

############################################################################
# 7. REMOVING A FRIEND FROM YOUE TRUSTED LIST
# this removes the requested friend from your list of trusted friends
# IN: PERSON ID WHO INITITATES THE REQUEST; THE PERSON ID TO REMOVE OUT: True/False
############################################################################
def removeFriend(firstPerson, secondPerson):
	if secondPerson not in edges[firstPerson]:
		return False
	else:
		if len(edges[firstPerson]) == 1:
			edges[firstPerson].pop()
		else:
			for i in range (0, len(edges[firstPerson])):
				if secondPerson in edges[firstPerson]:
					index = edges[firstPerson].index(secondPerson)
					del edges[secondPerson][index - 1]
		return True

############################################################################
# 8. DISPLAYS THE TOTAL NUMBER OF FRIENDS AND THERE ID/NAME FOR THE GIVEN USER
# IN: PERSON ID WHO INITITATES THE REQUEST; OUT: list, count
############################################################################
def FriendCounter(personID):
	if personID in edges:
		return int(len(edges[personID])/4), edges[personID]
	else:
		return None, None

############################################################################
# 9. ADDITIONAL FEATURES
############################################################################
def additionalFeatures(firstPerson, secondPerson):

	#to remove a particular person from my trusted list
	removed = removeFriend(firstPerson, secondPerson)
	if removed == True:
		print("Your requested Id was removed")
	else:
		print("We were unable to remove the requested person")

	# total number of friends and there list
	count, friendList = FriendCounter(firstPerson)
	if count == None:
		print("Sorry we could not find your records")
	else:
		print("The total number of friends: ", count, ". Friends are: ", friendList)

############################################################################
# 1. READING DATA/ PREPPING OUTPUT(1,2,3).TXT
# the program starts here
# this preps the output.txt and reads the files and sends it for further processing
# IN - .csv files; OUT - formatLines()
############################################################################
# to clean the previous output file and make sure the program runs on both the shell
# and on the normal execution of the code 
def main():
	if len(sys.argv) != 6:
		print("Please provide the path for the two input files and three output files")
		sys.exit(1)

	IP1 = sys.argv[1]
	IP2 = sys.argv[2]
	OP1 = sys.argv[3]
	OP2 = sys.argv[4]
	OP3 = sys.argv[5]

	try:
		output1 = open(OP1, 'w')
		output2 = open(OP2, 'w')
		output3 = open(OP3, 'w')
		output1.close()
		output2.close()
		output3.close()
	except:
		os.chdir("../")
		output1 = open(OP1, 'w')
		output2 = open(OP2, 'w')
		output3 = open(OP3, 'w')
		output1.close()
		output2.close()
		output3.close()
		
	# open the input file and send lines to formatLines()
	build = True
	print("build")
	with open(IP1, 'r') as fileToRead:
		reader = csv.reader(fileToRead, skipinitialspace=True)
		for row in reader:
			line = fileToRead.read()

	formatLines(line, build, OP1, OP2, OP3)

	build = False
	print("learn")
	with open(IP2, 'r') as fileToRead:
		reader = csv.reader(fileToRead, skipinitialspace=True)
		for row in reader:
			line = fileToRead.read()

	formatLines(line, build, OP1, OP2, OP3)

if __name__ == '__main__':
	main()
