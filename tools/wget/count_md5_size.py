import hashlib
import os

def get_md5(file_path):
    """计算文件的MD5值"""
    md5_obj = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            buf = f.read(4096)
            if not buf:
                break
            md5_obj.update(buf)
    return md5_obj.hexdigest()

def get_file_size(file_path):
    """获取文件大小，单位是字节"""
    return os.path.getsize(file_path)

def main():
    # 需要计算MD5值和文件大小的目录路径
    dir_path = "./save/1.6"

    # 打开输出文件
    with open("md5.txt", "w") as f:
        # 遍历目录下的所有文件
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                # 计算文件的MD5值和文件大小
                md5_value = get_md5(file_path)
                file_size = get_file_size(file_path)
                # 将结果输出到文件中，每行包含文件名、MD5值和文件大小，用竖线|进行分割
                f.write("{}|{}|{}\n".format(md5_value, file_size, file))

    print("Done.")

if __name__ == '__main__':
    main()