import os
import gzip
import shutil

# 父目录路径（其中包含 2000, 2001, ..., 2021 等子文件夹）
base_directory = r"E:\Data\ODIAC\New folder"

# 获取所有子文件夹名称（确保它们都是真正的文件夹）
subfolders = [
    folder for folder in os.listdir(base_directory)
    if os.path.isdir(os.path.join(base_directory, folder))
]

# 遍历每个子文件夹
for subfolder in subfolders:
    subfolder_path = os.path.join(base_directory, subfolder)

    # 找到子文件夹内所有以 .gz 结尾的文件
    gz_files = [
        f for f in os.listdir(subfolder_path)
        if f.endswith('.gz')
    ]

    # 解压每个 .gz 文件
    for gz_file in gz_files:
        gz_file_path = os.path.join(subfolder_path, gz_file)

        # 解压后文件的输出路径，去掉 .gz 后缀
        output_file_name = gz_file[:-3]  # 去掉 .gz
        output_file_path = os.path.join(subfolder_path, output_file_name)

        # 利用 gzip 和 shutil 执行解压操作
        with gzip.open(gz_file_path, 'rb') as f_in:
            with open(output_file_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print(f"已解压: {gz_file_path} -> {output_file_path}")
