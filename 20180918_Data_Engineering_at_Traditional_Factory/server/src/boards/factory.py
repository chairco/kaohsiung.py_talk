#-*- coding: utf-8 -*-

class ChartFactory:
    def __init__(self):
        self._func = {}
        self._charts = {}

    def collect(self, name):
        def _inject(func):
            self._func[name] = func
            return func

        return _inject

    def create(self, name, **kwargs):
        num = kwargs.get('num')
        if name in self._func:
            if name == 'bar':
                chart = self._func[name](num)
            elif name in ['dash', 'dash_yield', 'dash_scatter']:
                chart = self._func[name](**kwargs)
            elif name == 'pie':
                chart = self._func[name]()
            else:
                chart = self._func[name]()
            return chart
        else:
            raise ValueError(f'No Chart build for {name}')