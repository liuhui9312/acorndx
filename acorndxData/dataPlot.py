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


class Plot:
    # 柱状图/条形图
    def __init__(self):
        self.data = ''
        self.page = ''
        self.overlap = ''
        self.sort = '0'
        self.timeLine = ''
        self.script_list = ''
        self.project = ''

    def get_plot_type(self, pic_type):
        class_sets = {'Bar': Bar(),
                      'Line': Line(),
                      'Pie': Pie(),
                      'Map': Geo()
                      }
        self.project = class_sets[pic_type]
        return self.project

    def add_plot(self, label, data, add_type=0, pic_type='Bar'):
        if pic_type == 'Bar':
            if add_type == 1:
                self.project.add(label, list(data['index']),
                                 list(data[label]),
                                 is_datazoom_show=True,
                                 datazoom_range=[10, 25],
                                 datazoom_type='both',
                                 xaxis_interval=0,
                                 xaxis_rotate=30,
                                 yaxis_rotate=0)
            elif add_type == 2:
                self.project.add(label, list(data['index']),
                                 list(data[label]),
                                 xaxis_interval=0,
                                 xaxis_rotate=30,
                                 yaxis_rotate=0)
        elif pic_type == 'Pie':
            self.project.add(label, data['index'],
                             list(data[label]),
                             radius=[40, 75],
                             legend_pos='right',
                             legend_orient='vertical',
                             is_label_show=True)
        elif pic_type == 'Line':
            self.project.add(label,
                             list(data['index']),
                             list(data[label]),
                             is_smooth=True)
        elif pic_type == 'Map':
            self.project.add(label, list(data['index']),
                             list(data[label]),
                             visual_range=[0, 200],
                             visual_text_color='#fff',
                             symbol_size=15,
                             is_visualmap=True)

    def chart_plot(self, dat, sort, time_line, group, pic_type):
        self.data = dat
        self.sort = sort
        label_set = list([val for val in self.data.columns if val != 'index'])
        if '_'not in label_set[0]:
            self.project = self.get_plot_type(pic_type)
            for label in label_set:
                if len(label_set) == 1:
                    if self.sort == '1':
                        self.data = self.data.sort_values(by=label, ascending=True)
                    elif self.sort == '2':
                        self.data = self.data.sort_values(by=label, ascending=False)
                self.add_plot(label=label, data=self.data, add_type=1, pic_type=pic_type)
            self.script_list = self.project.get_js_dependencies()
            return self.project.render_embed()
        elif len(label_set[0].split('_')) == 2:
            self.timeLine = Timeline(timeline_bottom=1)
            if time_line != '--':
                if pic_type == 'Map':
                    self.page = Page()
                for label in label_set:
                    self.project = self.get_plot_type(pic_type)
                    if len(label_set) == 1:
                        if self.sort == '1':
                            self.data = self.data.sort_values(by=label, ascending=True)
                        elif self.sort == '2':
                            self.data = self.data.sort_values(by=label, ascending=False)
                    self.add_plot(label=label, data=self.data, add_type=2, pic_type=pic_type)
                    if pic_type == 'Map':
                        self.page.add(self.project)
                    else:
                        self.timeLine.add(self.project, label)
                if pic_type == 'Map':
                    self.script_list = self.page.get_js_dependencies()
                    return self.page.render_embed()
                else:
                    self.script_list = self.timeLine.get_js_dependencies()
                    return self.timeLine.render_embed()
            elif group != '--':
                self.project = self.get_plot_type(pic_type)
                for label in label_set:
                    if len(label_set) == 1:
                        if self.sort == '1':
                            self.data = self.data.sort_values(by=label, ascending=True)
                        elif self.sort == '2':
                            self.data = self.data.sort_values(by=label, ascending=False)
                    self.add_plot(label=label, data=self.data, add_type=1, pic_type=pic_type)
                self.script_list = self.project.get_js_dependencies()
                return self.project.render_embed()
        elif len(label_set[0].split('_')) == 3:
            time_sets = list(set([val.split('_')[0] for val in label_set]))
            self.timeLine = Timeline(timeline_bottom=1)
            if pic_type == 'Map':
                self.page = Page()
            for time_set in time_sets:
                self.project = self.get_plot_type(pic_type)
                for label in label_set:
                    if time_set not in label:
                        continue
                    self.add_plot(label=label, data=self.data, add_type=2, pic_type=pic_type)
                if pic_type != 'Map':
                    self.timeLine.add(self.project, time_set)
                else:
                    self.page.add(self.project)
            if pic_type == 'Map':
                self.script_list = self.page.get_js_dependencies()
                return self.page.render_embed()
            else:
                self.script_list = self.timeLine.get_js_dependencies()
                return self.timeLine.render_embed()


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

