# 绘图
from connMysql import connMysql
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import WordCloud
from pyecharts.charts import Tab
from pyecharts.faker import Faker

# 获得mysql的conn
conn = connMysql()
cursor = conn.cursor()


# 根据cnt绘制饼图
def pie_cnt():
    cursor.execute("select * from cnt_section")
    data = cursor.fetchall()
    c = (Pie(init_opts=opts.InitOpts(height="800px", width="1400px"))
         .add(series_name='使用总数区间', data_pair=data, radius=[100, 200])
         .set_global_opts(title_opts=opts.TitleOpts(title="Pie-cnt"))
         .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}"))
         )
    return c


# 根据week_cnt绘图
def bar_week():
    cursor.execute("select * from week_cnt")
    data = list(cursor.fetchall())
    y_data = []
    for d in data:
        y_data.append(d[1])
    c = (Bar(init_opts=opts.InitOpts(height="800px", width="1400px"))
         .add_xaxis(['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期七'])
         .add_yaxis("数量", y_data, category_gap=0, color='#3cb371')
         .set_global_opts(title_opts=opts.TitleOpts(title="Bar-week"))
         )
    return c


# 根据date_cnt绘制折线图
def line_date():
    cursor.execute("select * from date0_cnt")
    data0 = cursor.fetchall()
    x0_data = []
    y0_data = []
    for d in data0:
        x0_data.append(d[0])
        y0_data.append(d[1])
    cursor.execute("select * from date1_cnt")
    data1 = cursor.fetchall()
    x1_data = []
    y1_data = []
    for d in data1:
        x1_data.append(d[0])
        y1_data.append(d[1])
    c0 = (
        Line(init_opts=opts.InitOpts(height="400px", width="1400px"))
            .add_xaxis(x0_data)
            .add_yaxis('', y0_data, is_smooth=True, color="#ffdd00")
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-date"),yaxis_opts=opts.AxisOpts(max_=10000))
    )
    c1 = (
        Line(init_opts=opts.InitOpts(height="400px", width="1400px"))
            .add_xaxis(x1_data)
            .add_yaxis('', y1_data,is_smooth=True, color="#f15a22")
    )
    grid = Grid(init_opts=opts.InitOpts(height="800px", width="1400px"))
    grid.add(c0, grid_opts=opts.GridOpts(pos_bottom='60%'))
    grid.add(c1, grid_opts=opts.GridOpts(pos_top='60%'))
    return grid


def addOne():
    tab = Tab()
    tab.add(pie_cnt(), 'show1')
    tab.add(bar_week(), 'show2')
    tab.add(line_date(), 'show3')
    tab.render('./show/addOne.html')


if __name__ == '__main__':
    addOne()
