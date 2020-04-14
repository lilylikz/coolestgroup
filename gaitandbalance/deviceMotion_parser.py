class DataStore:
    def __init__(self, attY, attW, attZ, attX, time, rotX, rotY, rotZ, uaX, uaY, uaZ, gravX, gravY, gravZ, magY, magZ, magX, magAcc):
        self.attW = attW.replace("w:", "")
        self.attX = attX.replace("x:", "")
        self.attY = attY.replace("y:", "")
        self.attZ = attZ.replace("z:", "")
        self.time = time.replace("timestamp:", "")
        self.rotX = rotX.replace("x:", "")
        self.rotY = rotY.replace("y:", "")
        self.rotZ = rotZ.replace("z:", "")
        self.uaX = uaX.replace("x:", "")
        self.uaY = uaY.replace("y:", "")
        self.uaZ = uaZ.replace("z:", "")
        self.gravX = gravX.replace("x:", "")
        self.gravY = gravY.replace("y:", "")
        self.gravZ = gravZ.replace("z:", "")
        self.magX = magX.replace("x:", "")
        self.magY = magY.replace("y:", "")
        self.magZ = magZ.replace("z:", "")
        self.magAcc = magAcc.replace("accuracy:", "")

    def convertToCSVStyle(self):
        return (self.time + ", " + self.attW + ", " + self.attX + ", " + self.attY + ", " + self.attZ + ", " +
                self.rotX + ", " + self.rotY + ", " + self.rotZ  + ", " + self.uaX + ", " + self.uaY + ", " + self.uaZ + ", " +
                self.gravX + ", " + self.gravY + ", " + self.gravZ + ", " + self.magX + ", " + self.magY + ", " + self.magZ + ", " + self.magAcc + ", ")


if __name__ == "__main__":

    name = input("Enter file name: ")
    file = open(name,'r')
    content = file.read()

    filtered = content.replace("{", "").replace("\"", "").replace("}", "").replace("[", "").replace("]", "").replace("items:", "").replace("attitude:", "")
    filtered = filtered.replace("rotationRate:", "").replace("userAcceleration:", "").replace("gravity:", "").replace("magneticField:", "")
    splitData = filtered.split(",")
    storeList = []

    count = 0
    while count < (len(splitData) - 17):
        dataTemp = splitData[count : count + 18]
        count +=18
        storeVal = DataStore(dataTemp[0], dataTemp[1], dataTemp[2], dataTemp[3], dataTemp[4], dataTemp[5],
                             dataTemp[6], dataTemp[7], dataTemp[8], dataTemp[9], dataTemp[10], dataTemp[11],
                             dataTemp[12], dataTemp[13], dataTemp[14], dataTemp[15], dataTemp[16], dataTemp[17])
        storeList.append(storeVal)
        print(storeVal.convertToCSVStyle())

    file.close()

    csv = open(name.replace(".txt", "")+".csv", 'w')
    csv.write("Timestamp, Attitude W, Attitude X, Attitude Y, Attitude Z, Rotation Rate X, Rotation Rate Y, Rotation Rate Z, User Acceleration X, " +
              "User Acceleration Y, User Acceleration Z, Gravity X, Gravity Y, Gravity Z, Magnetic Field X, Magnetic Field Y, Magnetic Field Z, Magnetic Field Accuracy")
    csv.write("\n")
    for data in storeList:
        csv.write(data.convertToCSVStyle())
        csv.write("\n")

    csv.close()

