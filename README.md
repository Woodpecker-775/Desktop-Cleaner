# Desktop-Cleaner
 Here's a breakdown of code, line by line, with a detailed explanation:

---

### Importing Required Modules
```python
import os
```
- Provides functionality to interact with the operating system, including file and directory management.

```python
import shutil
```
- Handles file operations such as copying and moving files.

```python
import logging
```
- Used to log messages during the script's execution. This helps in debugging and tracking the script's progress.

---

### Configure Logging
```python
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
```
- Sets up the logging system.
- `level=logging.INFO`: Ensures only messages at the INFO level or higher (INFO, WARNING, ERROR) are logged.
- `format="%(asctime)s - %(levelname)s - %(message)s"`: Defines the log format, which includes:
  - Timestamp (`%(asctime)s`).
  - Log level (INFO, ERROR, etc.).
  - The message.

---

### Define Target Directory and File Categories
```python
TARGET_DIR = r"C:\Users\shafe\Downloads"
```
- Specifies the directory where files will be organized.
- `r""`: The raw string ensures backslashes in the path are handled properly without needing to escape them.

```python
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Others": []  # Catch-all category
}
```
- A dictionary mapping file categories (keys) to their associated file extensions (values).
- For example, files ending with `.jpg` will be placed in the "Images" folder.

---

### Define `organize_files` Function
```python
def organize_files(directory):
```
- A function to organize files in the given `directory` (the target folder).

```python
    for category in FILE_CATEGORIES:
        category_path = os.path.join(directory, category)
        os.makedirs(category_path, exist_ok=True)
```
- Loops through each category in `FILE_CATEGORIES`.
- Creates folders for each category inside the target directory.
- `os.path.join`: Joins the directory and category names into a valid path.
- `os.makedirs`: Creates the folder. The `exist_ok=True` ensures no error if the folder already exists.

---

### Loop Through Files in the Directory
```python
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)
```
- `os.listdir(directory)`: Gets a list of all items (files and folders) in the target directory.
- `os.path.join`: Combines the directory path and file name into a full file path.

```python
        if os.path.isdir(file_path):
            continue
```
- Skips over any folders in the directory.

---

### Handle File Categorization
```python
        _, file_extension = os.path.splitext(file_name)
```
- Splits the file name into its name (`_`) and extension (`file_extension`).
- For example, `"example.jpg"` becomes `("example", ".jpg")`.

```python
        moved = False
```
- A flag to track if the file has been successfully moved.

```python
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension.lower() in extensions:
                target_path = os.path.join(directory, category, file_name)
                target_path = handle_duplicates(target_path)
                shutil.move(file_path, target_path)
                logging.info(f"Moved: {file_name} → {category}")
                moved = True
                break
```
- Loops through each category and its associated extensions:
  - If the file's extension matches, the file is moved to the respective category's folder.
  - `shutil.move`: Moves the file to the target folder.
  - `logging.info`: Logs a message indicating the file has been moved.
  - `moved = True`: Marks the file as processed.

---

### Handle "Others" Category
```python
        if not moved:
            others_path = os.path.join(directory, "Others")
            os.makedirs(others_path, exist_ok=True)
            target_path = os.path.join(others_path, file_name)
            target_path = handle_duplicates(target_path)
            shutil.move(file_path, target_path)
            logging.info(f"Moved: {file_name} → Others")
```
- If no category matches the file's extension:
  - Moves it to the "Others" folder.

---

### Define `handle_duplicates` Function
```python
def handle_duplicates(target_path):
    base, extension = os.path.splitext(target_path)
    counter = 1
    while os.path.exists(target_path):
        target_path = f"{base} ({counter}){extension}"
        counter += 1
    return target_path
```
- Ensures no files are overwritten if duplicates exist.
- Example:
  - If `file.jpg` exists, it renames the duplicate as `file (1).jpg`.

---

### Main Block
```python
if __name__ == "__main__":
    try:
        organize_files(TARGET_DIR)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
```
- Executes the `organize_files` function when the script runs.
- The `try-except` block catches any unexpected errors and logs them.

---

### Example Output (Log Messages)
- `"2025-01-16 13:00:00 - INFO - Moved: example.jpg → Images"`
- `"2025-01-16 13:01:00 - INFO - Moved: unknown_file.xyz → Others"`

This script is efficient for file management in large, unorganized folders. 
