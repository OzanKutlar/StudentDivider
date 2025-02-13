import os
import platform
import json
import pyperclip

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
        print("Continuing with empty data.")
        return [{}, "data.data"]

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
            taName = input("Enter Teaching Assistant name (Leave blank or 'exit' to stop): ").strip()
            if taName == 'exit' or taName == '':
                break
            teachingAssistants[taName] = {}
        internalData.update(teachingAssistants)
        print("Teaching assistants initialized:", internalData)

def save(obj, filePath):
    with open(filePath, 'w') as jsonFile:
        json.dump(obj, jsonFile, indent=4)
        

def saveString(inputStr, fileName):
    pyperclip.copy(inputStr)
    
    filePath = 'temp.txt'
    if not os.path.exists(filePath):
        print(f'{filePath} does not exist, it will be created.')
    
    with open(filePath, 'w') as file:
        file.write(inputStr)
    
    print(f'String saved to {filePath} and copied to clipboard.')



def sendStudents(studentData, internalData):
    taAssignmentCount = {taName: 0 for taName in internalData}

    students = sorted(studentData, key=lambda x: x['id'])

    emptyInternalData = {taName: [] for taName in internalData}

    totalStudents = len(students)
    totalTas = len(internalData)
    upperLimit = totalStudents // totalTas

    for student in students:
        availableTas = [ta for ta in internalData if taAssignmentCount[ta] < upperLimit]
        
        
        if not availableTas:
            taWithLeastGrading = min(internalData, key=lambda taName: internalData[taName].get(student['id'], 0) + taAssignmentCount[taName])
        else:
            # breakpoint()
            taWithLeastGrading = min(availableTas, key=lambda taName: internalData[taName].get(student['id'], 0))

        emptyInternalData[taWithLeastGrading].append(student)
        
        internalData[taWithLeastGrading][student['id']] = internalData[taWithLeastGrading].get(student['id'], 0) + 1

        taAssignmentCount[taWithLeastGrading] += 1

    return emptyInternalData


    
def getString(taData):
    result = ''
    for ta in taData:
        result += f'Students Assigned to {ta}\n'
        
        for idx, student in enumerate(taData[ta], start=1):
            result += f'{idx}. {student["email"]} - {student["link"]}\n'
        
        result += '\n'
    
    return result





def main():
    studentData = loadStudentData()
    [internalData, fileLoc] = loadInternalData()
    
    testData(studentData, internalData)
    save(internalData, fileLoc)
    
    sentData = sendStudents(studentData, internalData)
    
    saveString(getString(sentData), "temp.txt")
    save(internalData, fileLoc)
    # save(sentData, "temp.txt")
    
    

main()