import os
import shutil
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Define the directory to organize
TARGET_DIR = r"C:\Users\shafe\Downloads"  # Change this as needed

# Define categories and their file extensions
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "setup": [".exe"],
    "Others": []  # Catch-all category
}

def organize_files(directory):
    # Create folders if they don't exist
    for category in FILE_CATEGORIES:
        category_path = os.path.join(directory, category)
        os.makedirs(category_path, exist_ok=True)

    # Iterate through files in the directory
    for file_name in os.listdir(directory):
        file_path = os.path.join(directory, file_name)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Get file extension
        _, file_extension = os.path.splitext(file_name)

        # Find the category for the file
        moved = False
        for category, extensions in FILE_CATEGORIES.items():
            if file_extension.lower() in extensions:
                target_path = os.path.join(directory, category, file_name)
                target_path = handle_duplicates(target_path)
                shutil.move(file_path, target_path)
                logging.info(f"Moved: {file_name} → {category}")
                moved = True
                break

        # Move to 'Others' if no category matches
        if not moved:
            others_path = os.path.join(directory, "Others")
            os.makedirs(others_path, exist_ok=True)
            target_path = os.path.join(others_path, file_name)
            target_path = handle_duplicates(target_path)
            shutil.move(file_path, target_path)
            logging.info(f"Moved: {file_name} → Others")

def handle_duplicates(target_path):
    """Handle duplicate files by renaming them."""
    base, extension = os.path.splitext(target_path)
    counter = 1
    while os.path.exists(target_path):
        target_path = f"{base} ({counter}){extension}"
        counter += 1
    return target_path

if __name__ == "__main__":
    try:
        organize_files(TARGET_DIR)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
