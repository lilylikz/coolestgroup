import xlrd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import norm
from datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm


path = "TestGait.xlsx" # input("Please enter file path: ")
book = xlrd.open_workbook(path)
sheet = book.sheet_by_index(0)

gaitScoreCol = -1
gaitAvgCol = -1
gaitStdevCol = -1
gaitCodeCol = -1;

gaitScore = -1
gaitAvg = -1
gaitStdev = -1
gaitLowerBound = -1000
gaitCode = "";

for i in range(0, sheet.ncols):
    if (sheet.cell_value(0,i) == "Gait Score"):
        gaitScoreCol = i
    elif (sheet.cell_value(0,i) == "Normalized Gait Average for Age Group"):
        gaitAvgCol = i
    elif (sheet.cell_value(0,i) == "Gait Stdev"):
        gaitStdevCol = i
    elif (sheet.cell_value(0,i) == "Patient Name/Code"):
        gaitCodeCol = i

for row in range(1, sheet.nrows):
    
    for i in range(0, sheet.ncols):
        if (i == gaitScoreCol):
            gaitScore = sheet.cell_value(row,i)
        elif (i == gaitAvgCol):
            gaitAvg = sheet.cell_value(row,i)
        elif (i == gaitStdevCol):
            gaitStdev = sheet.cell_value(row,i)
        elif (i == gaitCodeCol):
            gaitCode = sheet.cell_value(row,i)

    # define constants
    mu = gaitAvg
    sigma = gaitStdev
    x1 = gaitLowerBound
    x2 = gaitScore
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
    ax.set_title('Gait Report for ' + gaitCode, fontsize = 'xx-large', fontname = "Times New Roman")

    personCode = str(gaitCode) + str(date.today().strftime("%b-%d-%Y"))
    figureName = 'gait_curve_ '+ personCode+ '.png'
    plt.savefig(figureName, dpi=72, bbox_inches='tight')
    # plt.show()

    print("image made")

    pdfName = 'gait_report_'+ personCode+ '.pdf'
    c = canvas.Canvas(pdfName)
    c.drawImage(figureName, 25, 620, 300, 200) #x, y, height, width

    # define a large font
    c.setFont("Helvetica", 12)
    # say hello (note after rotate the y coord needs to be negative!)
    textString = "Interpretation of Results: " 
    c.drawString(350, 800, textString)
    textString = "Gait measures your walking speed in steps" 
    c.drawString(350, 780, textString)
    textString = "per minute. Our results indicate that your" 
    c.drawString(350, 760, textString)
    textString = "walking speed is " + str(gaitScore) + " steps a minute."
    c.drawString(350, 740, textString)
    
    c.showPage()
    c.save()

    print("Report completed")
