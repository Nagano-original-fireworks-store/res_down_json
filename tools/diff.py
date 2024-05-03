import json
from jsondiff import diff

def compare_json_files(file1_path, file2_path):
    # 读取JSON文件
    with open(file1_path, 'r', encoding='utf-8') as file:
        data1 = json.load(file)
    with open(file2_path, 'r', encoding='utf-8') as file:
        data2 = json.load(file)
    
    # 提取ClientDataVersion字段值
    version1 = data1.get('regionInfo', {}).get('ClientDataVersion')
    version2 = data2.get('regionInfo', {}).get('ClientDataVersion')

    # 比较两个版本
    if version1 is not None and version2 is not None:
        if version1 > version2:
            # 创建is_run.txt文件
            with open('is_run.txt', 'w') as file:
                file.write('UPDATE')
        else:
            print("NO UPDATE")
    else:
        print("Error: ClientDataVersion not found in one or both files.")

def compare_json_files2(file1_path, file2_path):
    # 读取JSON文件
    with open(file1_path, 'r', encoding='utf-8') as file:
        data1 = json.load(file)
    with open(file2_path, 'r', encoding='utf-8') as file:
        data2 = json.load(file)
    
    # 提取ClientDataVersion字段值
    version1 = data1.get('regionInfo', {}).get('ResVersionConfig').get('Version')
    version2 = data2.get('regionInfo', {}).get('ResVersionConfig').get('Version')

    # 比较两个版本
    if version1 is not None and version2 is not None:
        if version1 > version2:
            # 创建is_run.txt文件
            with open('is_run.txt', 'w') as file:
                file.write('UPDATE')
        else:
            print("NO UPDATE")
    else:
        print("Error: ResVersionConfig not found in one or both files.")

# 两个JSON文件的路径
file1_path = './4.6.0/CNRELAndroid4.6.0.json'
file2_path = './json/4.6.0/CNRELAndroid4.6.0.json'

# 调用比较函数
compare_json_files(file1_path, file2_path)
compare_json_files2(file1_path, file2_path)