import json

def compare_json_files(file1_path, file2_path, key_path, output_file='is_run.txt'):
    def get_nested_value(data, key_path):
        keys = key_path.split('.')
        for key in keys:
            data = data.get(key)
            if data is None:
                return None
        return data

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

    # Compare the versions
    if version1 is not None and version2 is not None:
        if version1 > version2:
            with open(output_file, 'w') as file:
                file.write('UPDATE')
        else:
            print("NO UPDATE")
    else:
        print(f"Error: '{key_path}' not found in one or both files.")

# Define the JSON file paths
file1_path = './4.7.0/CNRELAndroid4.7.0.json'
file2_path = './json/4.7.0/CNRELAndroid4.7.0.json'

# Call the function for both cases
compare_json_files(file1_path, file2_path, 'regionInfo.ClientDataVersion')
compare_json_files(file1_path, file2_path, 'regionInfo.ResVersionConfig.Version')
