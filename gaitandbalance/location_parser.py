class DataStore: 
    def __init__(self, vert, horz, long, lat, time, alt):
        self.verticalAccuracy = vert.replace("verticalAccuracy:", "")
        self.horizontalAccuracy = horz.replace("horizontalAccuracy:", "")
        self.longitude = long.replace("longitude:", "")
        self.latitude = lat.replace("latitude:", "")
        self.timestamp = time.replace("timestamp:", "")
        self.altitude = alt.replace("altitude:", "")
    def convertToCSVStyle(self):
        return self.verticalAccuracy + ", " + self.horizontalAccuracy + ", " +self.longitude + ", " + self.latitude + ", " + self.timestamp + ", " + self.altitude

if __name__ == "__main__":

    name = input("Enter file name: ")
    file = open(name,'r')
    content = file.read()

    filtered = content.replace("{", "").replace("\"", "").replace("}", "").replace("[", "").replace("]", "").replace("items:", "").replace("coordinate:", "")
    splitData = filtered.split(",")
    storeList = []
    
    count = 0
    while count < (len(splitData) - 5):
        dataTemp = splitData[count : count + 6]
        count +=6
        storeVal = DataStore(dataTemp[0], dataTemp[1], dataTemp[2], dataTemp[3], dataTemp[4], dataTemp[5])
        storeList.append(storeVal)
        print(storeVal.convertToCSVStyle())

    file.close()
    
    csv = open(name.replace(".txt", "")+".csv", 'w')
    csv.write("Vertical Accuracy, Horizontal Accuracy, Longitude, Latitude, Timestamp, Altitude")
    csv.write("\n")
    for data in storeList:
        csv.write(data.convertToCSVStyle())
        csv.write("\n")

    csv.close()
        
