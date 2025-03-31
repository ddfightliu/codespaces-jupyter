from pyecharts.charts import Kline
from pyecharts import options as opts


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
    xaxis_data = df_data["日期"].tolist()
    return kline_data,xaxis_data

def draw_kline_chart(data,xaxis, title="Stock K-Line Chart"):
    """
    Draws a K-line (candlestick) chart using pyecharts.
    :param data: List of lists containing stock data in the format:
                 [[open, close, low, high], [open, close, low, high], ...]
    :param title: Title of the chart.
    :return: A Kline chart object.
    """
    kline = Kline().add_xaxis(xaxis).add_yaxis("Stock Price", y_axis=data).set_global_opts(
        title_opts=opts.TitleOpts(title=title),
        xaxis_opts=opts.AxisOpts(type_="datetime", is_scale=True),
        yaxis_opts=opts.AxisOpts(type_="value", is_scale=True),
        datazoom_opts=[opts.DataZoomOpts(type_="inside"), opts.DataZoomOpts(type_="inside")],
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
    )
    return kline
