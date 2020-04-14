class DataStore: 
    def __init__(self, y, time, z, x):
        self.time = time.replace("timestamp:", "")
        self.x = x.replace("x:", "")
        self.y = y.replace("y:", "")
        self.z = z.replace("z:", "")
    def convertToCSVStyle(self):
        return self.time + ", " + self.x + ", " +self.y + ", " + self.z
if __name__ == "__main__":

    name = input("Enter file name: ")
    file = open(name,'r')
    content = file.read()

    filtered = content.replace("{", "").replace("\"", "").replace("}", "").replace("[", "").replace("]", "").replace("items:", "").replace("coordinate:", "")
    splitData = filtered.split(",")
    storeList = []
    
    count = 0
    while count < (len(splitData) - 3):
        dataTemp = splitData[count : count + 4]
        count +=4
        storeVal = DataStore(dataTemp[0], dataTemp[1], dataTemp[2], dataTemp[3])
        storeList.append(storeVal)
        # print(storeVal.convertToCSVStyle())

    file.close()
    
csv = open(name.replace(".txt", "")+".csv", 'w')
csv.write("Timestamp, X, Y, Z")
csv.write("\n")
for data in storeList:
    csv.write(data.convertToCSVStyle())
    csv.write("\n")
csv.close()
       
