import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Pie,Bar,Timeline

# 用pandas.read_csv() 读取指定的excel文件，选择编码格式gb18030(gb18030范围比)
df = pd.read_csv('weather.csv',encoding='gb18030')
# print(df['日期'])

# datatime   Series DataFrame  日期格式的数据类型
df['日期'] = df['日期'].apply(lambda x: pd.to_datetime(x))
print(df['日期'])

# 新建一列月份数据(将日期中的月份month 一项单独拿出来)
df['month'] = df['日期'].dt.month
# print(df['month'])

# DataFrame GroupBy聚合对象 分组和统计的 size()能够计算分组的大小
df_agg = df.groupby(['month','天气']).size().reset_index()
# print(df_agg)

# 设置下这3列的列名
df_agg.columns = ['month','tianqi','count']
# print(df_agg)

# 天气数据的形成
# print(df_agg[df_agg['month'==1]['tianqi','count']].sort_values(by='count',ascending=False).values.tolist())
"""
[['阴',10],['晴',6],['多云',13]]
"""

# 画图
# 实例化一个时间序列的对象
timeline = Timeline()
# 播放参数：设置时间间隔 1S 单位是：ms(毫秒)
timeline.add_schema(play_interval=1000) # 单位是：ms(毫秒)

# 循环遍历df_agg['month]里的唯一值
for month in df_agg['month'].unique():
    data =(
        df_agg[df_agg['month'] == month][['tianqi', 'count']]
        .sort_values(by='count', ascending=True)
        .values.tolist()
    )
     # 绘制柱状图
    bar = Bar()
    bar.add_xaxis([x[0] for x in data]) # x轴是天气名称
    bar.add_yaxis('',[x[1] for x in data]) # y轴是出现次数

    # 让柱状图横着放
    bar.reversal_axis()
    # 将计数标签放置在图形右边
    bar.set_series_opts(label_opts=opts.LabelOpts(position='right'))
    # 设置下图标的名称
    bar.set_global_opts(title_opts=opts.TitleOpts(title='清远2022年每月天气变化'))
    # 将设置好的bar对象放置到时间轮播图当中，并且标签选择月份 格式为: 数字月
    timeline.add(bar,f'{month}月')

# 将设置好的图表保存为 weather.html文件
timeline.render('weather.html')
