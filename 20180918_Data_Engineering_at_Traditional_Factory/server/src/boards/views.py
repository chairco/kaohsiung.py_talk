# boards/views.py
from django.shortcuts import render
from django.views.generic.base import TemplateView

from django_echarts.views.frontend import EChartsFrontView

from boards.load_dashdata import FACTORYDASH


def index(request):
    return render(request, 'index.html', {})


class DashIndex(TemplateView):
    template_name = 'boards/frontend_dashcharts.html'


class DashViewYield(EChartsFrontView):
    def get_echarts_instance(self, **kwargs):
        return FACTORYDASH.create('dash_yield', hours=1)