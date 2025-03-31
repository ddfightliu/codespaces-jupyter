# from pyecharts.charts import Kline
from pyecharts.charts import Kline, Bar, Grid
from pyecharts import options as opts
import akshare as ak

# from pyecharts.globals import CurrentConfig,NotebookType
# CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB


def trans_aksdat_to_echartdat(df_data):
    """ """
    kline_data = df_data[["开盘", "收盘", "最低", "最高"]].values.tolist()
    date = df_data["日期"].values.tolist()
    volumn_data = df_data[["成交量"]].values.tolist()
    value_data = df_data[["成交额"]].values.tolist()
    return date, kline_data, volumn_data, value_data


def draw_kline(
    data, xaxis, yaxis_name="Price", title="Stock K-Line Chart", markline=None
):
    """ """
    kline = Kline()
    kline.add_xaxis(xaxis).add_yaxis(
        "Stock :" + yaxis_name,
        y_axis=data,
        markline_opts=opts.MarkLineOpts(
            data=(
                [
                    opts.MarkLineItem(type_="max", name="Max"),
                    opts.MarkLineItem(type_="min", name="Min"),
                ]
                if markline
                else None
            ),
        ),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(type_="category", is_scale=True),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            is_scale=True,
        ),
        datazoom_opts=[opts.DataZoomOpts(type_="inside"), opts.DataZoomOpts()],
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )
    return kline


def draw_bar(volumn_data, date):
    bar = Bar()
    bar.add_xaxis(date).add_yaxis("成交量", volumn_data).set_global_opts(
        xaxis_opts=opts.AxisOpts(type_="category", is_scale=True),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            is_scale=True,
        ),
        datazoom_opts=[opts.DataZoomOpts(type_="inside"), opts.DataZoomOpts()],
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )
    return bar


class kchartDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getData(self, symbol, period="daily", adjust="qfq", **kwargs):
        self[symbol] = ak.stock_zh_a_hist(symbol, period, adjust, **kwargs)
        return self[symbol]

    def plot_aks(self, symbol, period="daily", adjust="qfq", **kwargs):
        if symbol not in self.keys():
            self.getData(symbol, period, adjust, **kwargs)
        date, kline_data, volumn_data, value_data = trans_aksdat_to_echartdat(
            self[symbol]
        )

        grid = Grid(init_opts=opts.InitOpts(width="1200px", height="600px"))

        kline = draw_kline(
            kline_data, date, symbol, title="stock " + symbol + " Kline Chart"
        )

        volumn_bar = draw_bar(volumn_data, date)

        grid.add(kline, grid_opts=opts.GridOpts(pos_bottom="70%"))
        grid.add(
            volumn_bar,
            grid_opts=opts.GridOpts(
                pos_top="30%",
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category", axislabel_opts=opts.LabelOpts(rotate=0)
            ),
        )

        volumn_bar.set_series_opts(
            label_opts=opts.LabelOpts(is_show=False),
            xaxis_index=[0, 1],
        )

        grid.render()
        return grid
