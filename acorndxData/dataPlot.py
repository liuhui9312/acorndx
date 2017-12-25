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
from pyecharts import Grid
from pyecharts import Geo


class PlotBar:
    # 柱状图/条形图
    def __init__(self):
        self.data = {'label1': [], }
        self.indexes = []
        self.bar = Bar()
        self.script_list = self.bar.get_js_dependencies()

    def bar_plot(self, dat, ind):
        self.data = dat
        self.indexes = ind
        self.bar = Bar(width=900, height=500)
        for label in self.data.keys():
            self.bar.add(label, self.indexes,
                         self.data[label],
                         is_datazoom_show=True,
                         datazoom_range=[10, 25],
                         datazoom_type='both',
                         xaxis_interval=0,
                         xaxis_rotate=30,
                         yaxis_rotate=30,
                         mark_point=['max', 'min'],
                         mark_line=['average'])
        return self.bar.render_embed()


class PlotPie:
    def __init__(self):
        self.data = ['label', []]
        self.indexes = []
        self.title = ''
        self.pie = Pie()

    def plot_pie(self, dat, ind, tit):
        self.data = dat
        self.title = tit
        self.indexes = ind
        self.pie = Pie(self.title, title_pos='center')
        self.pie.add(self.data[0], self.indexes,
                     self.data[1],
                     radius=[40, 75],
                     legend_pos='right',
                     legend_orient='vertical',
                     is_label_show=True)
        return self.pie.render_embed()


class PlotLine:
    def __init__(self):
        self.data = {'label1': [], }
        self.titles = '折线图'
        self.labels = ['default_labels']
        self.indexes = []
        self.line = ''

    def plot_line(self, dat, tit, lab, ind):
        self.data = dat
        self.titles = tit
        self.labels = lab
        self.indexes = ind
        self.line = Line(self.titles)
        for label in self.data.keys():
            self.line.add(label, self.indexes,
                          self.data[label],
                          is_smooth=True,
                          mark_line=['average'],
                          mark_point=['max', 'min'])
        return self.line


class PlotBarWithLine:
    def __init__(self):
        self.data = {{'label': []}, }
        self.titles = ''
        self.indexes = []
        self.bar = Bar()
        self.line = Line()
        self.overlap = Overlap()

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
        return self.overlap


class PlotGeo:
    def __init__(self):
        self.data = {{'label': []}, }
        self.titles = ['全国销售情势图', 'data from sale']
        self.indexes = []
        self.geo = Geo()

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
        return self.geo

