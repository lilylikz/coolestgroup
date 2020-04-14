import os, sys

class DataStore: 
    def __init__(self, start, end, color, text, selection):
        self.start = float(start.replace("startTime:", ""))
        self.end = float(end.replace("endTime:", ""))
        self.time = self.end - self.start
        self.color = color.replace("color:", "")
        self.text = text.replace("text:", "")
        self.colorSelected = selection.replace("colorSelected:", "")
        self.correct = (self.colorSelected == self.color)
    def convertToCSVStyle(self):
        return str(self.time) + ", " + str(self.correct)
        # return self.start + ", " + self.end + ", " +self.color + ", " + self.text + ", " + self.colorSelected
    def getCorrect(self):
        return self.correct
    def getTime(self):
        return self.time
# Open a file
path = "StroopData"
dirs = os.listdir(path)

# This would print all the files and directories
# asked to name the color of the word
storeList = []
totalTime = 0
correct = 0
for fname in dirs:
   file = open(path+"/"+fname,'r')
   content = file.read()
   dataTemp = content.split(";")
   storeVal = DataStore(dataTemp[0], dataTemp[1], dataTemp[2], dataTemp[3], dataTemp[4])
   storeList.append(storeVal)

for member in storeList:
    print(member.convertToCSVStyle())
    totalTime += member.getTime()
    if (member.getCorrect()):
        correct+=1

print("Accuracy: " + str(correct/len(storeList)))
print("Average Time: " + str(totalTime/len(storeList)))

