import os, sys
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm

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
path = ""
dirs = None
while True:
    try:
        path = input("Please enter the folder path of the stroop data: ")
        dirs = os.listdir(path)
        break
    except FileNotFoundError:
        print("Invalid path entered")
        

age = 0
age = float(input("Please enter patient age: "))
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

# https://www.researchgate.net/publication/258823137_Normative_Data_for_the_Stroop_Color_Word_Test_for_a_North_American_Population
#Other published normative data found no
#influence of age in the older population (>65 years), and only a
#small influence of age in a more broad sample of subjects aged
#12-83 14,15. Other published normative data found age,
#intellectual level and/or education to be related to Stroop
#scores 16-18.

# Let X = the normalized value above
# According to this study done in Canada, calculation of z-score for age should be done by taking
# Let Y = X - (-.403)*(age - 37.5)
# Z-score = (Y - 45.4)/10.4
normalized = 45.0 * (correct / totalTime)
print("Anticipated correct in 45 seconds: " + str(normalized))
ageFactor = normalized - (-.403)*(age - 37.5)
zScore = (ageFactor - 45.4)/10.4
print("Z-Score " + str(zScore))

# Data extracted from redcap files done above
# Report generation done below

mu = 0
sigma = 1
x1 = -10
x2 = zScore
percentile = int((norm.cdf((x2 - mu)/sigma) + 0.005) * 100)

x = np.arange(x1, x2, 0.001) # range of x in spec
x_all = np.arange((-4 * sigma) + mu, (4 * sigma) + mu, 0.001) # what does this line do
# mean = 0, stddev = 1, since Z-transform was calculated
y = norm.pdf(x, mu, sigma)
y2 = norm.pdf(x_all, mu, sigma)

fig, ax = plt.subplots(figsize=(9,6))

plt.style.use('fast')

ax.plot(x_all,y2)

ax.fill_between(x,y,0, alpha=0.3, color='purple')
ax.fill_between(x_all,y2,0, alpha=0.1)
ax.set_xlim([(-4 * sigma) + mu ,(4 * sigma) + mu])

ax.set_xlabel("You performed better than " + str(percentile) + "% of people in your age group", fontsize = 'xx-large', fontname = "Times New Roman")
ax.set_yticklabels([])
ax.set_title('Stroop Report', fontsize = 'xx-large', fontname = "Times New Roman")

personCode = str(path) + '_'+ str(date.today().strftime("%b-%d-%Y"))
figureName = 'stroop_curve_ '+ personCode + '_.png'

while True:
    try:
        plt.savefig(figureName, dpi=72, bbox_inches='tight')
        break
    except PermissionError:
        print("Please close the existing image with name: " + figureName)
# plt.show()

print("image made")

pdfName = 'stroop_report_'+ personCode+ '_.pdf'
c = canvas.Canvas(pdfName)
c.drawImage(figureName, 25, 620, 300, 200) #x, y, height, width

# define a large font
c.setFont("Helvetica", 12)
# say hello (note after rotate the y coord needs to be negative!)
textString = "Interpretation of Results: " 
c.drawString(350, 800, textString)
textString = "Stroop measures your selective attention, "
c.drawString(350, 780, textString)
textString = "processing speed, and cognitive flexibility." 
c.drawString(350, 760, textString)
ageFactor = int(1000*ageFactor)
textString = "Your stroop score is " + str(ageFactor/1000) + "."
c.drawString(350, 740, textString)
textString = "The average score is 45.4."
c.drawString(350, 720, textString)
try:
    c.showPage()
    c.save()
    print("Report completed")
except PermissionError:
    print("Please close the existing pdf with name: " + pdfName + " . Then try again")
