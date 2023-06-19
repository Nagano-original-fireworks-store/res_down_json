import requests
import hashlib
import json
import os
import random
import string
from datetime import datetime

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        md5_hash = hashlib.md5()
        while chunk := file.read(8192):
            md5_hash.update(chunk)
    return md5_hash.hexdigest()

def download_file(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

def get_file_url(base_url, version, res_version, device, file_type):
    return base_url.format(version, res_version, device, file_type)

# 从外部读取 info.json 文件内容
with open('info.json', 'r') as file:
    info_data = json.load(file)

for version, version_data in info_data.items():
    md5_data = []  # 用于保存下载文件的信息
    device_md5_data = {}  # 用于保存不同设备的信息

    base_url = "https://autopatchcn.yuanshen.com/client_game_res/{}_live/output_{}/client/{}/{}"
    devices = version_data["device"]
    res_version = version_data["res"]["Version_Suffix"]
    file_types = version_data["res"]["file"]

    for device in devices:
        device_md5_data[device] = []  # 为每个设备创建一个空列表

        for file_type in file_types:
            file_url = get_file_url(base_url, version, res_version, device, file_type)
            file_destination = f"save/{version}/{file_type}.txt"  # 文件的保存路径和名称可以根据需求自行修改

            # 创建文件夹路径
            save_directory = os.path.dirname(file_destination)
            os.makedirs(save_directory, exist_ok=True)

            download_file(file_url, file_destination)

            # 生成地区时间和随机信息后缀
            region = device  # 替换为实际的地区信息
            time_suffix = datetime.now().strftime('%Y%m%d_%H%M%S')
            random_suffix = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

            # 生成新的文件名
            file_extension = os.path.splitext(file_destination)[1]  # 获取文件扩展名
            new_file_name = f"{region}_{time_suffix}_{random_suffix}_{os.path.basename(file_destination)}{file_extension}"
            new_file_path = os.path.join(save_directory, new_file_name)

            # 重命名文件
            os.rename(file_destination, new_file_path)

            # 计算文件的 MD5 值
            md5 = calculate_md5(new_file_path)
            md5_lowercase = md5.lower()

            print("文件下载完成并计算MD5值：")
            print("文件URL:", file_url)
            print("新文件名:", new_file_name)
            print("MD5:", md5_lowercase)

            # 获取未重命名的文件名和文件大小
            original_file_name = os.path.basename(file_destination)
            file_size = os.path.getsize(new_file_path)

            # 保存文件信息到 md5_data 列表和 device_md5_data 字典中
            file_info = {
                "remoteName": original_file_name,
                "md5": md5_lowercase,
                "fileSize": file_size,
            }
            md5_data.append(file_info)
            device_md5_data[device].append(file_info)

    # 保存不同设备的信息到不同的 md5_{device}_{version}.json
    for device, device_data in device_md5_data.items():
        device_file_name = f"md5/md5_{device}_{version}.json"
        with open(device_file_name, 'w') as file:
            json.dump(device_data, file)

print("所有文件下载完成并计算MD5值，并保存到相应的 JSON 文件中。")
