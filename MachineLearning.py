import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

# 设置Excel文件路径
file_path = r"E:\\New folder (3)\\GADM_Province_2000_TableToExcel.xlsx"

# 检查文件是否存在
if not os.path.exists(file_path):
    raise FileNotFoundError(f"The file at {file_path} does not exist. Please check the path.")

# 读取Excel文件
data = pd.read_excel(file_path)

# 检查所需列是否存在
required_columns = ['MEAN_DepCom', 'MEAN_MaxDep', 'SUM_Carbon', 'CONTINENT']
if not all(col in data.columns for col in required_columns):
    raise ValueError(f"The file must contain the following columns: {required_columns}")

# 处理数据：去除负值和零值
for col in ['MEAN_DepCom', 'MEAN_MaxDep', 'SUM_Carbon']:
    if (data[col] <= 0).any():
        print(f"Warning: Non-positive values found in column {col}. These will be removed.")
        data = data[data[col] > 0]

# 根据CONTINENT分组并绘制二维概率分布图
continents = data['CONTINENT'].unique()
for continent in continents:
    subset = data[data['CONTINENT'] == continent]

    plt.figure(figsize=(10, 6))
    sns.kdeplot(x=subset['MEAN_DepCom'], y=subset['SUM_Carbon'], cmap="Blues", fill=True)
    plt.title(f'Probability Distribution: MEAN_DepCom vs SUM_Carbon ({continent})')
    plt.xlabel('MEAN_DepCom')
    plt.ylabel('SUM_Carbon')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.kdeplot(x=subset['MEAN_MaxDep'], y=subset['SUM_Carbon'], cmap="Greens", fill=True)
    plt.title(f'Probability Distribution: MEAN_MaxDep vs SUM_Carbon ({continent})')
    plt.xlabel('MEAN_MaxDep')
    plt.ylabel('SUM_Carbon')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.kdeplot(x=subset['MEAN_DepCom'], y=subset['MEAN_MaxDep'], cmap="Reds", fill=True)
    plt.title(f'Probability Distribution: MEAN_DepCom vs MEAN_MaxDep ({continent})')
    plt.xlabel('MEAN_DepCom')
    plt.ylabel('MEAN_MaxDep')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.show()
