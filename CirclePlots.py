import pandas as pd

# 设置输入 Excel 文件路径
input_path = r"C:\Users\cl7613\Desktop\New folder (3)\2000_NEW.xlsx"  # 修改为你的实际路径
output_path = r"C:\Users\cl7613\Desktop\DonutChart_Stats.xlsx"

# 读取数据
df = pd.read_excel(input_path)

# ------------- 外环数据（大洲层级）统计 -------------
outer_df = df['FIRST_CONTINENT'].value_counts().reset_index()
outer_df.columns = ['FIRST_CONTINENT', 'Count']
outer_df['Percent_of_Total'] = outer_df['Count'] / outer_df['Count'].sum()
outer_df['Percent_of_Total'] = outer_df['Percent_of_Total'].apply(lambda x: f"{x:.2%}")

# ------------- 内环数据（每个大洲中CLUSTER_ID的分布） -------------
# 先统计每个大洲下各CLUSTER_ID的数量
inner_df = df.groupby(['FIRST_CONTINENT', 'CLUSTER_ID']).size().reset_index(name='Count')

# 再合并对应的大洲总数以计算占比
continent_total = df['FIRST_CONTINENT'].value_counts().to_dict()
inner_df['Percent_in_Continent'] = inner_df.apply(
    lambda row: row['Count'] / continent_total[row['FIRST_CONTINENT']],
    axis=1
)
inner_df['Percent_in_Continent'] = inner_df['Percent_in_Continent'].apply(lambda x: f"{x:.2%}")

# ------------- 导出为 Excel 文件 -------------
with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    outer_df.to_excel(writer, sheet_name='Outer_Ring_Summary', index=False)
    inner_df.to_excel(writer, sheet_name='Inner_Ring_Summary', index=False)

print(f"✅ 已成功生成统计Excel文件：{output_path}")
