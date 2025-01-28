import json
import os
import sys

def compare_json_files(file1_path, file2_path, key_path, output_file='./is_run.txt'):
    def get_nested_value(data, key_path):
        keys = key_path.split('.')
        for key in keys:
            data = data.get(key)
            if data is None:
                return None
        return data

    # Check if files exist
    if not os.path.exists(file1_path):
        print(f"Error: File 1 '{file1_path}' does not exist.")
        return

    # If file2 does not exist, write 'UPDATE' to output file
    if not os.path.exists(file2_path):
        print(f"File 2 '{file2_path}' does not exist. Creating '{output_file}' with 'UPDATE'.")
        with open(output_file, 'w') as file:
            file.write('UPDATE')
        return

    # Read JSON files
    try:
        with open(file1_path, 'r', encoding='utf-8') as file:
            data1 = json.load(file)
        with open(file2_path, 'r', encoding='utf-8') as file:
            data2 = json.load(file)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return

    # Extract the version values
    version1 = get_nested_value(data1, key_path)
    version2 = get_nested_value(data2, key_path)

    # If version2 is None, write 'UPDATE' to output file
    if version2 is None:
        print(f"Key '{key_path}' not found in file2. Writing 'UPDATE' to '{output_file}'.")
        with open(output_file, 'w') as file:
            file.write('UPDATE')
        return

    # Compare the versions
    if version1 is not None and version2 is not None:
        if version1 > version2:
            with open(output_file, 'w') as file:
                file.write('UPDATE')
        else:
            print("NO UPDATE")
    else:
        print(f"Error: '{key_path}' not found in one or both files.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python diff.py <version>")
        sys.exit(1)

    current_dir = os.getcwd()
    version = sys.argv[1]

    # Define the JSON file paths
    file1_path = f'{current_dir}/{version}/CNRELAndroid{version}.json'
    file2_path = f'{current_dir}/json/{version}/CNRELAndroid{version}.json'

    # Call the function for both cases
    compare_json_files(file1_path, file2_path, 'regionInfo.ClientDataVersion')
    compare_json_files(file1_path, file2_path, 'regionInfo.ResVersionConfig.Version')