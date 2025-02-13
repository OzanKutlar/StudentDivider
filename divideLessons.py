import os
import platform
import json

def loadInternalData():
    jsonFiles = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.data')]

    allJsonFiles = jsonFiles

    if not allJsonFiles:
        print("No DATA files found, starting with empty data.")
        return [{}, "data.data"]
    else:
        if len(allJsonFiles) == 1:
            dataFile = allJsonFiles[0]
            print(f"Found only one DATA file: {dataFile}")
            shouldLoad = input(f"Do you want to load data from {dataFile}? (Y/n): ").strip().lower()
            shouldLoad = shouldLoad in ("", "yes", "y")

        else:
            print("Multiple DATA files found:")
            
            for idx, file in enumerate(allJsonFiles, start=1):
                if file in jsonFiles:
                    print(f"{idx}. {file} (Current Directory)")
            
            while True:
                try:
                    choice = int(input("Choose a file to load (enter the number): ").strip())
                    if 1 <= choice <= len(allJsonFiles):
                        dataFile = allJsonFiles[choice - 1]
                        shouldLoad = input(f"Do you want to load data from {dataFile}? (Y/n): ").strip().lower()
                        shouldLoad = shouldLoad in ("", "yes", "y")
                        break
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

    if not shouldLoad:
        print("Exiting.")
        exit()

    with open(dataFile, "r") as f:
        data = json.load(f)
    
    return [data, dataFile]


def loadStudentData():
    jsonFiles = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith('.json')]

    downloadsDirectory = os.path.join(os.path.expanduser("~"), "Downloads")
    downloadedJsonFiles = []
    if os.path.exists(downloadsDirectory):
        downloadedJsonFiles = [os.path.join(downloadsDirectory, f) for f in os.listdir(downloadsDirectory) if os.path.isfile(os.path.join(downloadsDirectory, f)) and f.endswith('.json')]

    allJsonFiles = jsonFiles + downloadedJsonFiles

    if not allJsonFiles:
        print("No JSON files found, starting with empty data.")
    else:
        if len(allJsonFiles) == 1:
            dataFile = allJsonFiles[0]
            print(f"Found only one JSON file: {dataFile}")
            shouldLoad = input(f"Do you want to load data from {dataFile}? (Y/n): ").strip().lower()
            shouldLoad = shouldLoad in ("", "yes", "y")

        else:
            print("Multiple JSON files found:")
            
            for idx, file in enumerate(allJsonFiles, start=1):
                if file in jsonFiles:
                    print(f"{idx}. {file} (Current Directory)")
                else:
                    print(f"{idx}. {file} (Downloads Directory)")
            
            while True:
                try:
                    choice = int(input("Choose a file to load (enter the number): ").strip())
                    if 1 <= choice <= len(allJsonFiles):
                        dataFile = allJsonFiles[choice - 1]
                        shouldLoad = input(f"Do you want to load data from {dataFile}? (Y/n): ").strip().lower()
                        shouldLoad = shouldLoad in ("", "yes", "y")
                        break
                    else:
                        print("Invalid selection.")
                except ValueError:
                    print("Invalid input. Please enter a number.")

    if not shouldLoad:
        print("Exiting.")
        exit()

    with open(dataFile, "r") as f:
        data = json.load(f)
    
    return data

def testData(studentData, internalData):
    if not studentData:
        print("Student data is empty. Exiting program.")
        exit()

    if not internalData:
        teachingAssistants = {}
        while True:
            taName = input("Enter Teaching Assistant name (or 'exit' to stop): ").strip()
            if taName == 'exit' or taName == '':
                break
            teachingAssistants[taName] = []
        internalData.update(teachingAssistants)
        print("Teaching assistants initialized:", internalData)

def save(obj, filePath):
    with open(filePath, 'w') as jsonFile:
        json.dump(obj, jsonFile, indent=4)


def sendStudents(studentData, internalData):
    studentIds = [student['id'] for student in studentData]
    
    numTAs = len(internalData)
    
    numStudentsPerTA = len(studentIds) // numTAs
    
    taAssignments = {taName: [] for taName in internalData}

    studentGradingCounts = {studentId: {taName: 0 for taName in internalData} for studentId in studentIds}

    for studentId in studentIds:
        taGradingCounts = {taName: internalData[taName].get(studentId, 0) for taName in internalData}
        
        leastGradedTA = min(taGradingCounts, key=taGradingCounts.get)
        
        taAssignments[leastGradedTA].append(studentId)
        
        internalData[leastGradedTA][studentId] = taGradingCounts[leastGradedTA] + 1
    
    allAssignedStudents = sum(taAssignments.values(), [])
    numAssignedPerTA = len(allAssignedStudents) // numTAs
    remainingStudents = allAssignedStudents[numTAs * numAssignedPerTA:]

    for taName in internalData:
        if len(taAssignments[taName]) < numAssignedPerTA:
            while len(taAssignments[taName]) < numAssignedPerTA:
                taAssignments[taName].append(remainingStudents.pop())

    return taAssignments



def main():
    studentData = loadStudentData()
    [internalData, fileLoc] = loadInternalData()
    testData(studentData, internalData)
    save(internalData, fileLoc)
    print(sendStudents(studentData, internalData))
    

main()