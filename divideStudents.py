import os
import platform
import json
import pyperclip
import random

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
        downloadedJsonFiles = [os.path.join(downloadsDirectory, f) for f in os.listdir(downloadsDirectory) 
                               if os.path.isfile(os.path.join(downloadsDirectory, f)) and f.endswith('.json')]

    allJsonFiles = jsonFiles + downloadedJsonFiles

    if not allJsonFiles:
        print("No JSON files found, starting with empty data.")
        return {}

    if len(allJsonFiles) == 1:
        dataFile = allJsonFiles[0]
        print(f"Found only one JSON file: {dataFile}")
        shouldLoad = input(f"Do you want to load data from {dataFile}? (Y/n): ").strip().lower() in ("", "yes", "y")
    else:
        print("Multiple JSON files found:")
        for idx, file in enumerate(allJsonFiles, start=1):
            location = "Current Directory" if file in jsonFiles else "Downloads Directory"
            print(f"{idx}. {file} ({location})")
        
        while True:
            try:
                choice = int(input("Choose a file to load (enter the number): ").strip())
                if 1 <= choice <= len(allJsonFiles):
                    dataFile = allJsonFiles[choice - 1]
                    shouldLoad = input(f"Do you want to load data from {dataFile}? (Y/n): ").strip().lower() in ("", "yes", "y")
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

    shouldDelete = input(f"Do you want to delete {dataFile} after loading? (Y/n): ").strip().lower() in ("", "yes", "y")
    
    if shouldDelete:
        try:
            os.remove(dataFile)
            print(f"Deleted {dataFile}.")
        except OSError as e:
            print(f"Error deleting file: {e}")

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
        

def saveString(inputStr, filePath):
    pyperclip.copy(inputStr)
    
    if not os.path.exists(filePath):
        print(f'{filePath} does not exist, it will be created.')
    
    with open(filePath, 'w') as file:
        file.write(inputStr)
    
    print(f'String saved to {filePath} and copied to clipboard.')



def sendStudents(studentData, internalData):
    # Initialize the result dictionary to store assignments
    result = {}
    
    # Initialize result dictionary with empty lists for each TA
    for ta in internalData:
        result[ta] = []
    
    # Skip if no TAs are available
    if not result:
        print("No TAs available. Cannot assign students.")
        return {}
    
    # For each student in the input data
    for student in studentData:
        # Get student info
        student_name = student.get("id", "Unknown")
        student_link = student.get("link", "No link")
        
        # First, find which TA has graded this student the least
        min_grades = float('inf')
        eligible_tas = []
        
        for ta in internalData:
            # Get the count of times this TA has graded this student, default to 0
            grade_count = internalData[ta].get(student_name, 0)
            
            # If this is a new minimum, clear the list and add this TA
            if grade_count < min_grades:
                min_grades = grade_count
                eligible_tas = [ta]
            # If this ties the minimum, add this TA to the eligible list
            elif grade_count == min_grades:
                eligible_tas.append(ta)
        
        # Now, from the eligible TAs, prioritize those with fewer total assignments
        if len(eligible_tas) > 1:
            # Count current assignments for each eligible TA
            ta_loads = {ta: len(result[ta]) for ta in eligible_tas}
            min_load = min(ta_loads.values())
            
            # Filter to only keep TAs with the minimum current load
            least_loaded_tas = [ta for ta in eligible_tas if ta_loads[ta] == min_load]
            
            # Select from this refined list
            selected_ta = random.choice(least_loaded_tas)
        else:
            # If only one TA is eligible, select that one
            selected_ta = eligible_tas[0]
        
        # Add the student to the selected TA's list
        result[selected_ta].append({
            "name": student.get("name", "Unknown"),
            "link": student_link
        })
        
        # Update the internal data to reflect this new assignment
        if student_name in internalData[selected_ta]:
            internalData[selected_ta][student_name] += 1
        else:
            internalData[selected_ta][student_name] = 1
    
    # Check the final distribution
    assignments = [len(result[ta]) for ta in result]
    max_diff = max(assignments) - min(assignments)
    
    print(f"Distribution: {', '.join([f'{ta}: {len(result[ta])}' for ta in result])}")
    
    if max_diff <= 1:
        print("Students distributed evenly among TAs.")
    else:
        print(f"Warning: Assignment difference: {max_diff}. This can happen when student history constraints conflict with even distribution.")
    
    return result


    
def getString(taData):
    result = ''
    for ta in taData:
        result += f'Students Assigned to {ta}\n'
        
        for idx, student in enumerate(taData[ta], start=1):
            result += f'{idx}. {student["name"]} - {student["link"]}\n'
        
        result += '\n'
    
    return result





def main():
    studentData = loadStudentData()
    [internalData, fileLoc] = loadInternalData()
    
    testData(studentData, internalData)
    save(internalData, fileLoc)
    
    sentData = sendStudents(studentData, internalData)
    
    saveString(getString(sentData), "temp.txt")
    
    shouldLoad = input(f"Do you want to save data to {fileLoc}? (Y/n): ").strip().lower()
    shouldLoad = shouldLoad in ("", "yes", "y")
    if(shouldLoad == True):
        save(internalData, fileLoc)
        
    os.system("start nano ./temp.txt")
    
    

main()