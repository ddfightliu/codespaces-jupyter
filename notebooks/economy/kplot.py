# from pyecharts.charts import Kline
from pyecharts.charts import Kline
from pyecharts import options as opts
import akshare as ak


# from pyecharts.globals import CurrentConfig,NotebookType
# CurrentConfig.NOTEBOOK_TYPE = NotebookType.JUPYTER_LAB


def akshare_data_to_kline(df_data):
    """
    Converts AKShare stock data to a format suitable for Kline chart.
    :param data: DataFrame containing stock data with columns ['open', 'close', 'low', 'high'].
    :return: List of lists containing stock data in the format:
             [[open, close, low, high], [open, close, low, high], ...]
    """
    kline_data = df_data[["开盘", "收盘", "最低", "最高"]].values.tolist()
    xaxis_data = df_data["日期"].values.tolist()
    return kline_data, xaxis_data


def draw_kline_chart(data, xaxis,yaxis_name="Price", title="Stock K-Line Chart"):
    """
    Draws a K-line (candlestick) chart using pyecharts.
    :param data: List of lists containing stock data in the format:
                 [[open, close, low, high], [open, close, low, high], ...]
    :param title: Title of the chart.
    :return: A Kline chart object.
    """
    kline = Kline()
    kline.add_xaxis(xaxis).add_yaxis(
        "Stock :" + yaxis_name,
        y_axis=data,
        markline_opts=opts.MarkLineOpts(
            data=[
                opts.MarkLineItem(type_="max", name="Max"),
                opts.MarkLineItem(type_="min", name="Min"),
            ],
        ),
    ).set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(type_="category", is_scale=True),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            is_scale=True,
        ),
        datazoom_opts=[opts.DataZoomOpts(type_='inside'), opts.DataZoomOpts()],
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )
    return kline


class kchartDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def getData(self, symbol, **kwargs):
        self[symbol] = ak.stock_zh_a_hist(
            symbol, **kwargs
        )
        return self[symbol]
    
    def plot_aks(self, symbol, period="daily", adjust="qfq", **kwargs):
        if symbol not in self.keys():
            self.getData(
                symbol, period=period, adjust=adjust, **kwargs
            )
        kline=draw_kline_chart(
            *akshare_data_to_kline(self[symbol]),symbol,
            title="stock " + symbol + " Kline Chart"
        )
        kline.render()
        return kline
