# 绘图
from connMysql import connMysql
from pyecharts.components import Image
from pyecharts.options import ComponentTitleOpts
from pyecharts.charts import PictorialBar
from pyecharts.globals import SymbolType
from pyecharts import options as opts
from pyecharts.charts import Pie
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import EffectScatter
from pyecharts.charts import Tab
from pyecharts.charts import Radar

# 获得mysql的conn
conn = connMysql()
cursor = conn.cursor()


# 插入一幅图片
def imgShow():
    c = (Image()
         .add(
        src='https://gimg2.baidu.com/image_search/src=http%3A%2F%2F5b0988e595225.cdn.sohucs.com%2Fimages%2F20171018%2F8136cf30421b4da785db4f4ccd89ec2e.jpeg&refer=http%3A%2F%2F5b0988e595225.cdn.sohucs.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1673162909&t=60bb894776084545ee29eef5f269c711',
        style_opts={"width": "1200px", "height": "600px", "style": "margin-left: 100px"})
         .set_global_opts(title_opts=ComponentTitleOpts(title="华盛顿共享单车数据可视化展示")))
    return c


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
         .add_xaxis(['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日'])
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
            .add_yaxis('2011', y0_data, is_smooth=True, color="#ffdd00")
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-date"), legend_opts=opts.LegendOpts(pos_top="5%"),
                             yaxis_opts=opts.AxisOpts(max_=10000))
    )
    c1 = (
        Line(init_opts=opts.InitOpts(height="400px", width="1400px"))
            .add_xaxis(x1_data)
            .add_yaxis('2012', y1_data, is_smooth=True, color="#f15a22")
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-date"), legend_opts=opts.LegendOpts(pos_top="55%"),
                             yaxis_opts=opts.AxisOpts(max_=10000))
    )
    grid = Grid(init_opts=opts.InitOpts(height="800px", width="1400px"))
    grid.add(c0, grid_opts=opts.GridOpts(pos_bottom='60%'))
    grid.add(c1, grid_opts=opts.GridOpts(pos_top='60%'))
    return grid


# 根据假日周末绘图
def bar_hw():
    cursor.execute("select * from holiday_avg")
    hol_data = cursor.fetchall()
    cursor.execute("select * from workingday_avg")
    wrk_data = cursor.fetchall()
    y_hol = []
    y_wrk = []
    for h in hol_data:
        y_hol.append(h[1])
    for w in wrk_data:
        y_wrk.append(w[1])
    c = (Bar(init_opts=opts.InitOpts(height="800px", width="1400px"))
         .add_xaxis(['2011年', '2012年'])
         .add_yaxis('假期日', y_hol, color='#ff4500')
         .add_yaxis('工作日', y_wrk, color='#3cb371')
         .set_global_opts(title_opts=opts.TitleOpts(title="Bar-h&w")))
    return c


# 根据月份绘图:
def mnth():
    cursor.execute('select * from mnth_cnt')
    data = cursor.fetchall()
    x = []
    y = []
    for d in data:
        x.append(str(d[0]) + '月')
        y.append(d[1])
    c = (
        EffectScatter(init_opts=opts.InitOpts(height="800px", width="1400px"))
            .add_xaxis(x)
            .add_yaxis("", y)
            .set_global_opts(
            title_opts=opts.TitleOpts(title="EffectScatter-月份使用量"),
            xaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True)),
            yaxis_opts=opts.AxisOpts(splitline_opts=opts.SplitLineOpts(is_show=True))
        )
    )
    return c


# 根据季节绘图
def season():
    cursor.execute(
        'select case when season=1 then "冬季" when season=2 then "春季" when season=3 then "夏季" when season=4 then "秋季" end season,season_sum from season_cnt')
    data = cursor.fetchall()
    x = [data[0][0], data[3][0], data[2][0], data[1][0]]
    y = [data[0][1], data[3][1], data[2][1], data[1][1]]
    c = (
        PictorialBar(init_opts=opts.InitOpts(height="800px", width="1400px"))
            .add_xaxis(x)
            .add_yaxis(
            "",
            y,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol=SymbolType.ROUND_RECT,
        )
            .reversal_axis()
            .set_global_opts(
            title_opts=opts.TitleOpts(title="PictorialBar-各季节单车使用情况"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            ),
        )
    )
    return c


# 根据天气绘图
def weather():
    cursor.execute(
        'select case when weathersit=1 then "晴天" when weathersit=2 then "雾天" when weathersit=3 then "小雪" when weathersit=4 then "大雨" end weathersit,weathersit_cnt from weathersit_cnt')
    data = cursor.fetchall()
    y = []
    for d in data:
        y.append(d[1])
    y.append(0)  # 没有大雨数据
    cursor.execute('select * from weathersit_casual')
    data = cursor.fetchall()
    yc = []
    for d in data:
        yc.append(d[1])
    yc.append(0)
    c = (Radar(init_opts=opts.InitOpts(height="800px", width="1400px"))
         .add_schema(schema=[
        opts.RadarIndicatorItem(name="晴天", max_=2500000),
        opts.RadarIndicatorItem(name="雾天", max_=2500000),
        opts.RadarIndicatorItem(name="小雪", max_=2500000),
    ])
         .add(series_name='租车总数', data=[y], linestyle_opts=opts.LineStyleOpts(color="#CD0000"))
         .add(series_name='休闲用户数量', data=[yc], linestyle_opts=opts.LineStyleOpts(color='#5CACEE'))
         .set_global_opts(title_opts=opts.TitleOpts(title="天气雷达图"), legend_opts=opts.LegendOpts()
                          )
         )
    return c


## 根据温度和湿度绘图
def th():
    cursor.execute('select * from temp')
    t = cursor.fetchall()
    x0_data = []
    y0_data = []
    for d in t:
        x0_data.append(d[0])
        y0_data.append(d[1])
    cursor.execute('select * from hum')
    h = cursor.fetchall()
    x1_data = []
    y1_data = []
    for d in h:
        x1_data.append(d[0])
        y1_data.append(d[1])
    c0 = (
        Line(init_opts=opts.InitOpts(height="600px", width="700px"))
            .add_xaxis(x0_data)
            .add_yaxis('温度', y0_data, color='#ffdd00')
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-temp&hum"),
                             legend_opts=opts.LegendOpts(pos_left="20%"))
    )
    c1 = (
        Line(init_opts=opts.InitOpts(height="600px", width="700px"))
            .add_xaxis(x1_data)
            .add_yaxis('湿度', y1_data, color='#f15a22')
            .set_global_opts(title_opts=opts.TitleOpts(title="Line-temp&hum"),
                             legend_opts=opts.LegendOpts(pos_right="20%"))
    )
    grid = Grid(init_opts=opts.InitOpts(height="800px", width="1400px"))
    grid.add(c0, grid_opts=opts.GridOpts(is_show=True, pos_right='55%', pos_top='20%'))
    grid.add(c1, grid_opts=opts.GridOpts(is_show=True, pos_left='55%', pos_top='20%'))
    return grid


def addOne():
    tab = Tab()
    tab.add(imgShow(), '首页')
    tab.add(pie_cnt(), '数量')
    tab.add(bar_week(), '星期')
    tab.add(line_date(), '日期')
    tab.add(bar_hw(), '假日')
    tab.add(mnth(), '月份')
    tab.add(season(), '季节')
    tab.add(weather(), '天气')
    tab.add(th(), '温湿')
    tab.render('./show/addOne.html')


if __name__ == '__main__':
    addOne()
