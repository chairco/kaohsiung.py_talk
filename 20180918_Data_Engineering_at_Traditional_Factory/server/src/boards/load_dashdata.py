# boards/load_dashdata.py
import datetime
import itertools
import pytz

from borax.fetch import fetch
from pyecharts import HeatMap, Bar, Line, Grid, Scatter, EffectScatter, Style

from boards.models import Record
from boards.factory import ChartFactory

from django.db.models import Count, Q
from django.utils import timezone

from collections import OrderedDict


FACTORYDASH = ChartFactory()


def gen_dates(start, end):
    """
    yield datetime with interval
    """
    while start < end:
        start += datetime.timedelta(minutes=1)
        yield start.strftime('%Y-%m-%d %H:%M')


def groupy(datas, start, end):
    """
    :param datas: target dataset is dict
    :param start: gap time with start
    :param start: gap time with end
    """
    tzutc_8 = pytz.timezone('Asia/Taipei') # UTC to +8

    # group by mins, data should be order by rs232 time
    grouped = itertools.groupby(datas, lambda f: f.rs232_time.astimezone(
        tzutc_8).strftime("%Y-%m-%d %H:%M"))
    
    data_records = {day: len(list(g)) for day, g in grouped}
    
    # get all time interval
    data_gaps = {d: 0 for d in gen_dates(start, end)}
    data_all = {**data_gaps, **data_records}
    return data_all


def getall_data(hours):
    """
    get all data 
    :param: hours:
    return
    """
    tp = pytz.timezone('Asia/Taipei')
    timenow = timezone.now() - timezone.timedelta(minutes=1)
    start = timenow - timezone.timedelta(hours=hours)
    datas = Record.objects.gte(dt=start)
    
    start = start.astimezone(tp)
    end = timenow.astimezone(tp)
    data_all = groupy(datas, start, end)
    return data_all


@FACTORYDASH.collect('dash_yield')
def create_dash_yield(hours):
    """
    create bar+line to show yield rate in the time interval
    :param: kwargs: requests parameter
    :return: grid: pyechart object
    """
    datas = getall_data(hours=hours)


    # sort data by key
    data_filter = OrderedDict(
        sorted(datas.items(), key=lambda t: t[0]))

    attr = list(data_filter.keys())
    cam = list(data_filter.values())


    bar = Bar("柱狀圖", height=720)
    bar.add(
        "cam", attr, cam,
        is_stack=True,
    )

    line = Line("折線圖", title_top="50%")
    line.add(
        "cam", attr, cam,
        mark_point=["max", "min"],
        mark_line=["average"],
        is_datazoom_show=True,
    )

    grid = Grid(width='100%')
    grid.add(bar, grid_bottom="60%")
    grid.add(line, grid_top="60%")
    grid.render()

    return grid