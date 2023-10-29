import hashlib
import json
import os
import requests
from datetime import datetime

def download_file(url, save_directory, version_data, file_name):
    response = requests.get(url)
    if response.status_code == 200:
        save_path = os.path.join(save_directory, file_name)
        if os.path.exists(save_path):
            file_name, extension = os.path.splitext(file_name)
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            file_name = f"{file_name}_{timestamp}_client_{extension}"
            save_path = os.path.join(save_directory, file_name)
        with open(save_path, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded: {url}")
        print(f"File size: {os.path.getsize(save_path)} bytes")  # Added a print statement to output the file size
        md5_hash = calculate_md5(save_path)
        print(f"MD5: {md5_hash}")
        print()

        return save_path
    else:
        return None

def calculate_md5(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
        md5_hash = hashlib.md5(data).hexdigest()
        return md5_hash

# 调用示例
save_directory = "./save_data_versions/"

# 从 JSON 文件中获取下载数据
with open('info_data_versions.json', 'r') as file:
    info_data = json.load(file)

for version_data, suffix_data in info_data.items():
    version_suffix_client = suffix_data.get("Version_Suffix_client")
    version_suffix_silence = suffix_data.get("Version_Suffix_silence")

    if version_suffix_client or version_suffix_silence:
        url_client = "https://autopatchcn.yuanshen.com/client_design_data/{}_live/output_{}"
        
        if version_suffix_client:
            file_name_client = version_suffix_client.split("/")[-1]

            # 下载 Version_Suffix_client 文件并保存
            file_path_client = download_file(url_client.format(version_data, version_suffix_client), save_directory, version_data, file_name_client)
            if file_path_client:
                # 计算 Version_Suffix_client 文件的 MD5 哈希值
                md5_hash_client = calculate_md5(file_path_client)

                # 保存 Version_Suffix_client 的 MD5 哈希值到文件
                with open(f"md5_data_versions/md5_{version_data}_{file_name_client}", 'w') as md5_file_client:
                    md5_file_client.write(md5_hash_client)

        if version_suffix_silence:
            file_name_silence = version_suffix_silence.split("/")[-1]

            # 下载 Version_Suffix_silence 文件并保存
            file_path_silence = download_file(url_client.format(version_data, version_suffix_silence),  save_directory, version_data, file_name_silence)
            if file_path_silence:
                # 计算 Version_Suffix_silence 文件的 MD5 哈希值
                md5_hash_silence = calculate_md5(file_path_silence)

                # 保存 Version_Suffix_silence 的 MD5 哈希值到文件
                with open(f"md5_data_versions/md5_{version_data}_silence_{file_name_silence}", 'w') as md5_file_silence:
                    md5_file_silence.write(f"{md5_hash_client}|{md5_hash_silence}")
