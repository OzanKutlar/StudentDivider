# **StudentDivider**  

## **Project Overview**  
**StudentDivider** is an automation tool designed to efficiently distribute students among Teaching Assistants (TAs) for grading and mentoring. It consists of three main components:  

1. **`browserInject.js`** – A script that scrapes student data from [learn.khas.edu.tr](https://learn.khas.edu.tr/).  
2. **`converter.py`** – Converts `browserInject.js` into a **bookmarklet**, allowing users to run the scraper directly from their browser bookmarks.  
3. **`main.py`** – Processes the scraped student data and assigns students to TAs while keeping track of past assignments.  

---

## **Features**  
✅ **Student data extraction** from `learn.khas.edu.tr` using JavaScript.  
✅ **Bookmarklet support** for easy scraping (via `converter.py`).  
✅ **Automatic TA workload balancing** with historical tracking.  
✅ **Clipboard copy support** for quick access to assigned student lists.  
✅ **Persistent data storage** to ensure fair distribution over multiple runs.  

---

## **How It Works**  

### **Step 1: Convert `browserInject.js` to a Bookmarklet (Optional)**  
Instead of manually running the JavaScript in the browser console every time, you can convert it into a bookmarklet:  

1. Run the Python script:  
   ```bash
   python converter.py
   ```  
2. The script will generate a **bookmarklet link**.  
3. Copy and save it as a bookmark in your browser.  
4. Click the bookmark whenever you're on `learn.khas.edu.tr` to extract student data.  

### **Step 2: Extract Student Data**  
- If you don't use the bookmarklet, manually run `browserInject.js` in the browser's developer console.  
- The script will save student data as a `.json` file.  

### **Step 3: Assign Students to TAs**  
1. Run `main.py`:  
   ```bash
   python main.py
   ```  
2. Follow the prompts to select student data and TA records.  
3. Students will be **fairly assigned** to available TAs.  
4. The results are **saved** and **copied to the clipboard** for easy sharing.  

---

## **Installation & Setup**  

### **Prerequisites**  
Make sure you have the following installed:  
- **Python 3.7+**  
- Required Python libraries (install with the following command):  
  ```bash
  pip install pyperclip
  ```

### **Running the Project**  

#### **Option 1: Using the Bookmarklet (Recommended)**  
1. Run `converter.py` to create the bookmarklet.  
2. Save it as a bookmark in your browser.  
3. Click the bookmark while on `learn.khas.edu.tr` to extract student data.  

#### **Option 2: Running Manually**  
1. Copy and paste `browserInject.js` into the browser console.  
2. Run it to generate the `.json` file.  

#### **Run the Python Script**  
1. Open a terminal and navigate to the project directory.  
2. Run:  
   ```bash
   python main.py
   ```  
3. Follow the prompts to assign students and save the results.  

---

## **File Descriptions**  

### **1. `main.py`**  
- Loads student and TA data.  
- Evenly distributes students among TAs.  
- Saves and updates assignment history.  
- Copies assignments to the clipboard.  

### **2. `browserInject.js`**  
- Scrapes student details (email, ID, submission links) from `learn.khas.edu.tr`.  
- Saves data as a `.json` file.  

### **3. `converter.py`**  
- Converts `browserInject.js` into a **bookmarklet**.  
- Allows users to run the scraper with a single click from their browser.  

---

## **Usage Example**  

1. Run `converter.py` and save the bookmarklet.  
2. Click the bookmark on `learn.khas.edu.tr` to generate a `.json` file.  
3. Run `main.py` to distribute students among TAs.  
4. The assignments are saved and copied to the clipboard for easy sharing.  

---

## **Future Enhancements**  
🔹 **Web-based interface** for easier management.  
🔹 **Customizable assignment rules** (e.g., priority-based allocation).  
🔹 **TA workload analytics** for better distribution.  

---

## **License**  
**MIT License**  

Copyright (c) 2025 OzanKutlar