import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 设置matplotlib字体以正确显示中文
plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# Pandas选项设置，以便更好地查看数据
pd.set_option('display.max_columns', None)  # 显示所有列
pd.set_option('display.max_rows', None)  # 显示所有行
pd.set_option('display.width', None)  # 设置为自动调整宽度

# 定义文件路径和对应的城市名称
files = {
    'bj.csv': '北京',
    'sh.csv': '上海',
    'gz.csv': '广州',
    'sz.csv': '深圳',
    'zz.csv': '郑州'
}

# 定义各个城市的人均GDP
gdp_per_capita = {
    '北京': 200204.50,
    '上海': 189827.57,
    '广州': 161235.09,
    '深圳': 194526.17,
    '郑州': 104687.88
}

# 创建一个空的DataFrame用于存储所有数据
all_data = pd.DataFrame()

# 遍历每个csv文件并读取内容到DataFrame中
for file, city in files.items():
    df = pd.read_csv(f'D:\\rentSpider\\rentSpider\\{file}')
    df['city'] = city  # 添加城市列

    # 清理和转换数据
    df['price'] = df['price'].astype(float)  # 转换为浮点数
    df['area'] = df['area'].astype(float)  # 确保面积是浮点数类型
    df['price_per_area'] = df['price'] / df['area']  # 计算单位面积租金

    # 将当前城市的dataframe追加到总的dataframe中
    all_data = pd.concat([all_data, df], ignore_index=True)

# 计算每个城市的单位面积租金均价
avg_price_per_area = all_data.groupby('city')['price_per_area'].mean().reset_index()

# 计算单位面积租金均价与人均GDP的比例
avg_price_per_area['ratio'] = avg_price_per_area['price_per_area'] / avg_price_per_area['city'].map(gdp_per_capita)

# 输出统计数据
print("各城市单位面积租金均价与人均GDP的比例:")
print(avg_price_per_area[['city', 'ratio']])

# 绘制各城市人均GDP对比的条形图
plt.figure(figsize=(10, 6))

# 创建一个DataFrame来保存人均GDP数据以便绘图
gdp_df = pd.DataFrame(list(gdp_per_capita.items()), columns=['city', 'gdp_per_capita'])

# 使用seaborn绘制条形图
sns.barplot(x='city', y='gdp_per_capita', data=gdp_df)
plt.title('各城市人均GDP对比')
plt.ylabel('人均GDP (元)')
plt.xlabel('城市')
plt.savefig('各城市人均GDP对比.png')  # 保存图表
plt.show()

# 绘制条形图展示比例
plt.figure(figsize=(10, 6))
sns.barplot(x='city', y='ratio', data=avg_price_per_area)
plt.title('各城市单位面积租金均价与人均GDP的比例')
plt.ylabel('比例')
plt.xlabel('城市')
plt.savefig('各城市单位面积租金均价与人均GDP的比例.png')  # 保存图表
plt.show()