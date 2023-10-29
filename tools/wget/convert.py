import json
import os

# Hardcoded paths
JSON_FILE_PATH = "./info.json"
INPUT_DIR = "./input"
OUTPUT_DIR = "./outputs"

def process_files():
    # Load the JSON data
    with open(JSON_FILE_PATH, 'r') as file:
        data = json.load(file)
    
    # Ensure the output directory exists
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Iterate over each txt file in the input directory
    for file_name in os.listdir(INPUT_DIR):
        if file_name.endswith('.txt'):
            file_path = os.path.join(INPUT_DIR, file_name)

            # Extract version and device from the filename
            parts = file_name.split('_')
            device = parts[1]
            version_key = parts[2].replace('.txt', '')
            
            # Replace StandaloneWindows64 with PC in the device name
            if device == "StandaloneWindows64":
                device = "PC"
                
            # Get the Version_Suffix for the version
            version_suffix = data.get(version_key, {}).get('res', {}).get('Version_Suffix', '')
                
            # Split the Version_Suffix to get new_version and new_version_suffix
            new_version, new_version_suffix = version_suffix.split('_')
                
            # Read the txt file content and update version and versionSuffix
            with open(file_path, 'r') as f:
                content = json.load(f)
                
            content['version'] = new_version
            content['versionSuffix'] = new_version_suffix
                
            # Write the updated content back to the txt file
            with open(file_path, 'w') as f:
                json.dump(content, f)
                
            # Rename the file to the format "DEVICE_version.txt"
            new_file_name = f"{device.upper()}_version.txt"
            
            # Create a version folder and move the file into it
            version_folder = os.path.join(OUTPUT_DIR, version_key)
            if not os.path.exists(version_folder):
                os.makedirs(version_folder)
            
            os.rename(file_path, os.path.join(version_folder, new_file_name))

if __name__ == "__main__":
    process_files()
