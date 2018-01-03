#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/20 10:07
# @Author  : huiliu@acorndx.com
# @Descript: 
# @File    : dataPlot.py
# @Software: PyCharm
# from acorndxData.dataSql import *
from pyecharts import Bar
from pyecharts import Line
from pyecharts import Pie
from pyecharts import Overlap
from pyecharts import Page
from pyecharts import Geo
from pyecharts import Timeline


class PlotBar:
    # 柱状图/条形图
    def __init__(self):
        self.data = ''
        self.bar = Bar()
        self.sort = '0'
        self.script_list = self.bar.get_js_dependencies()

    def bar_plot(self, dat, sort):
        self.data = dat
        self.sort = sort
        self.bar = Bar(width=900, height=500)
        for label in list(self.data.columns):
            if label != 'index':
                print(list(self.data['index']))
                print(list(self.data[label]))
                if self.sort == '1':
                    self.data = self.data.sort_values(by=label, ascending=True)
                elif self.sort == '2':
                    self.data = self.data.sort_values(by=label, ascending=False)
                self.bar.add(label, list(self.data['index']),
                             list(self.data[label]),
                             is_datazoom_show=True,
                             datazoom_range=[10, 25],
                             datazoom_type='both',
                             xaxis_interval=0,
                             xaxis_rotate=30,
                             yaxis_rotate=0)
        return self.bar.render_embed()


class PlotPie:
    def __init__(self):
        self.data = ''
        self.sort = '0'
        self.pie = Pie()
        self.script_list = self.pie.get_js_dependencies()

    def plot_pie(self, dat, sort):
        self.data = dat
        self.sort = sort
        self.pie = Pie()
        for label in list(self.data.columns):
            if label != 'index':
                self.pie.add(label, self.data['index'],
                             self.data[label],
                             radius=[40, 75],
                             legend_pos='right',
                             legend_orient='vertical',
                             is_label_show=True)
        return self.pie.render_embed()


class PlotLine:
    def __init__(self):
        self.data = ''
        self.sort = ''
        self.line = Line()
        self.script_list = self.line.get_js_dependencies()

    def plot_line(self, dat, sort):
        self.data = dat
        self.sort = sort
        self.line = Line()
        try:
            for label in list(self.data.columns):
                if label != 'index':
                    print(list(self.data['index']))
                    print(list(self.data[label]))
                    self.line.add(label, list(self.data['index']),
                                  list(self.data[label]),
                                  is_smooth=True,
                                  mark_line=['average']
                                  )
                    print(label)
            return self.line.render_embed()
        except Exception as e:
            print('{} in plot line'.format(e))


class PlotBarWithLine:
    def __init__(self):
        self.data = {{'label': []}, }
        self.titles = ''
        self.indexes = []
        self.bar = Bar()
        self.line = Line()
        self.overlap = Overlap()
        self.script_list = self.overlap.get_js_dependencies()

    def plot_bar_line(self, dat, tit, ind):
        self.data = dat
        self.titles = tit
        self.indexes = ind
        self.bar = Bar(self.titles)
        for label in self.data.keys():
            label_bar = '{}_B'.format(label)
            label_line = '{}_L'.format(label)
            self.bar.add(label_bar, self.indexes,
                         self.data[label],
                         is_label_show=True)
            self.line.add(label_line, self.indexes,
                          self.data[label],
                          is_label_show=True,
                          mark_point=['max', 'min'])
        self.overlap.add(self.bar)
        self.overlap.add(self.line)
        return self.overlap.render_embed()


class PlotGeo:
    def __init__(self):
        self.data = {{'label': []}, }
        self.titles = ['全国销售情势图', 'data from sale']
        self.indexes = []
        self.geo = Geo()
        self.script_list = self.geo.get_js_dependencies()

    def plot_geo(self, dat, tit, ind):
        self.data = dat
        self.titles = tit
        self.indexes = ind
        self.geo = Geo(self.titles[0], self.titles[1],
                       title_pos='center', title_color='#fff',
                       width=1200, height=600, background_color='#404a59')
        for label in self.data.keys():
            self.geo.add(label, self.indexes, self.data[label],
                         visual_range=[0, 200], visual_text_color='#fff',
                         symbol_size=15, is_visualmap=True)
        return self.geo.render_embed()


class MultiPlot:
    def __init__(self):
        self.data = ''
        self.timeLine = Timeline()
        self.page = Page()
        self.script_list = Bar().get_js_dependencies()

    def multi_plot(self, dat):
        self.data = dat
        try:
            for m_title, tpv1 in self.data.items():
                self.timeLine = Timeline(is_auto_play=False, timeline_bottom=0)
                attr = tpv1['index']
                for m_time in list(tpv1.columns):
                    if m_time != 'index':
                        tp_bar = Bar(m_time)
                        tpv1 = tpv1.sort_values(by=m_time ,ascending=False)
                        tp_bar.add(m_title, list(tpv1['index']),
                                   list(tpv1[m_time]),
                                   xaxis_interval=0,
                                   xaxis_rotate=30,
                                   yaxis_rotate=30,)
                        self.timeLine.add(tp_bar, m_time)
                self.page.add(self.timeLine)
            return self.page.render_embed()
        except Exception as e:
            print('multi_plot error with {}'.format(str(e)))
            return None
