"""This is a basic script for plotting an analysis file.

    This script is just the first step in visualizing the data set. This file
    comprises of the method creating an html bokeh plot and a command at the
    end to implement the method.

"""
from collections import OrderedDict

import numpy as np
import pandas as pd
import pdb

from bokeh.plotting import figure, show, output_file
from bokeh.models import (BoxZoomTool, ResetTool, PreviewSaveTool,
                          ResizeTool, PanTool, PolySelectTool,
                          WheelZoomTool, HoverTool, BoxSelectTool,
                          ColumnDataSource)

import data_processing as dp


def make_plot(dataframe,  top=100, minvalues=0.01, stacked=True, lgaxis=True):
    """Basic method to plot sensitivity anlaysis.

    This is the method to generate a bokeh plot followung the burtin example
    template at the bokeh website. For clarification, parameters refer to an
    output being measured (Tmax, C, k2, etc.) and stats refer to the 1st or
    total order sensitivity index.

    Parameters:
    --------------
    dataframe : Dataframe containing sensitivity analysis results to be plotted

    top: Integer indicating the number of parameters to display (highest
                 sensitivity values)

    minvalues: Cutoff minimum for which parameters should be plotted (float)

    stacked: Boolean indicating in bars should be stacked for each parameter.

    lgaxis: Boolean indicating if log axis should be used (True) or if a
            linear axis should be used (False).


    Returns:
    ---------------
    p: Figure of the data to be plotted
    """
    # Read in csv file as panda dataframe.
    # tdf = pd.read_csv(Dataframe, delimiter=' ', skipinitialspace=True,
    #                  engine='python')
    # df = tdf
    df = dataframe
    maxval = 0
    # Remove rows which have values less than cutoff values
    df = df[df['S1'] > minvalues]
    df = df[df['ST'] > minvalues]
    df = df.dropna()

    # Create dictionary of bar colors, assume up to 3 stats are plotted
    # per parameter.
    df = df.sort_values('ST', ascending=False)
    df = df.head(top)
    df = df.reset_index(drop=True)
    colors = ["#0d3362", "#c64737"]
    s1color = np.array(["#c64737"]*df.S1.size)
    sTcolor = np.array(["#0d3362"]*df.ST.size)
    stat_color = OrderedDict()
    for i in range(0, 2):
        stat_color[i] = colors[i]
    # Reset index of dataframe.

    # Sizing parameters
    width = 800
    height = 800
    inner_radius = 90
    outer_radius = 300 - 10

    # Determine wedge size based off number of parameters
    big_angle = 2.0 * np.pi / (len(df)+1)
    # Determine division of wedges for plotting bars based on # stats plotted
    if stacked is False:
        small_angle = big_angle / (4)
    else:
        small_angle = big_angle / (3)
    # pdb.set_trace()
    # params = df['Parameter']
    # S1vals = df['S1']
    # S1vals = df['ST']

    # plottools = [BoxZoomTool(), ResetTool(), PreviewSaveTool(),
    #             ResizeTool(), PanTool(), PolySelectTool(),
    #             WheelZoomTool(), HoverTool(), BoxSelectTool()]
    plottools = "hover, wheel_zoom, save, reset, resize"

    p = figure(plot_width=width, plot_height=height, title="",
               x_axis_type=None, y_axis_type=None,
               x_range=(-420, 420), y_range=(-420, 420),
               min_border=0, outline_line_color="black",
               background_fill_color="#f0e1d2", border_fill_color="#f0e1d2",
               tools=plottools)
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Parameter", "@Param"), ("Sensitivity", "@Sens"),
                      ("Confidence", "@Conf")]
    hover.point_policy = "follow_mouse"

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # annular wedges divided into smaller sections for bars
    angles = np.pi/2 - big_angle/2 - df.index.to_series()*big_angle
    # circular axes and labels
    labels = np.power(10.0, np.arange(0, -3, -1))
    # extra_labels = np.power(10.0, np.arange(-0.30103, -4.30103, -1))
    # Re-size if no values are above 0.1
    # if maxval < 0.1:
    #     labels = np.delete(labels, 0)
    # Size of radii of each label
    # pdb.set_trace()
    # extra_radii = (((np.log10(extra_labels / labels[0])) + labels.size) *
    #                (outer_radius - inner_radius) / labels.size +inner_radius)
    labels = np.append(labels, 0.0)
    if lgaxis is True:
            pdb.set_trace()
            radii = (((np.log10(labels / labels[0])) +
                     labels.size) * (outer_radius - inner_radius) /
                     labels.size + inner_radius)
            radii[-1] = inner_radius
    else:
        labels = np.delete(labels, -1)
        radii = (outer_radius - inner_radius)*labels + inner_radius

    # Add zero label to labels and radii

    # extra_radii = np.append(extra_radii, radii)

    # Adding axis lines and labels
    p.circle(0, 0, radius=radii, fill_color=None, line_color="white")
    p.text(0, radii[:], [str(r) for r in labels[:]],
           text_font_size="8pt", text_align="center", text_baseline="middle")

    # Plot the values of each stat for each parameter.
    # radius of stat is the value of a statistic converted to the radial
    # value.
    Cols = np.array(['S1', 'ST'])
    for statistic in range(0, 2):
        if lgaxis is True:
            radius_of_stat = (((np.log10(df[Cols[statistic]] / labels[0])) +
                              labels.size) * (outer_radius - inner_radius) /
                              labels.size + inner_radius)
        else:
            radius_of_stat = ((outer_radius - inner_radius) *
                              df[Cols[statistic]] + inner_radius)
        if stacked is False:
            startA = -big_angle + angles + (2*statistic + 1)*small_angle
            stopA = -big_angle + angles + (2*statistic + 2)*small_angle
        else:
            startA = -big_angle + angles + (1)*small_angle
            stopA = -big_angle + angles + (2)*small_angle
        df[Cols[statistic]+'radial'] = pd.Series(radius_of_stat,
                                                 index=df.index)
        df[Cols[statistic]+'_start_angle'] = pd.Series(startA,
                                                       index=df.index)
        df[Cols[statistic]+'_stop_angle'] = pd.Series(stopA,
                                                      index=df.index)
        inner_rad = np.ones_like(angles)*inner_radius

    pdata = pd.DataFrame({
                         'x': np.append(np.zeros_like(inner_rad),
                                        np.zeros_like(inner_rad)),
                         'y': np.append(np.zeros_like(inner_rad),
                                        np.zeros_like(inner_rad)),
                         'ymin': np.append(inner_rad, inner_rad),
                         'ymax': pd.Series.append(df[Cols[1]+'radial'],
                                                  df[Cols[0]+'radial']
                                                  ).reset_index(drop=True),
                         'starts': pd.Series.append(df[Cols[1] +
                                                    '_start_angle'],
                                                    df[Cols[0] +
                                                    '_start_angle']
                                                    ).reset_index(drop=True),
                         'stops': pd.Series.append(df[Cols[1] +
                                                      '_stop_angle'],
                                                   df[Cols[0] +
                                                      '_stop_angle']
                                                   ).reset_index(drop=True),
                         'Param': pd.Series.append(df.Parameter,
                                                       df.Parameter
                                                   ).reset_index(drop=True),
                         'Colors': np.append(sTcolor, s1color),
                         'Conf': pd.Series.append(df.ST_conf,
                                                        df.S1_conf
                                                  ).reset_index(drop=True),
                         'Sens': pd.Series.append(df.ST,
                                                  df.S1).reset_index(drop=True)
                         })

    pdata_s = ColumnDataSource(pdata)
    gh = p.annular_wedge(x='x', y='y', inner_radius='ymin',
                         outer_radius='ymax',
                         start_angle='starts',
                         end_angle='stops',
                         color='Colors',
                         source=pdata_s
                         )
    hover.renderers = [gh]
    # p.annular_wedge(0, 0, inner_radius, df.STradial,
    #                 -big_angle + angles + (2*1 + 1)*small_angle,
    #                 -big_angle + angles + (2*1 + 2)*small_angle,
    #                 color=stat_color[1])
    # radial axes

    dictdata = df.set_index('Parameter').to_dict()
    p.annular_wedge(0, 0, inner_radius-10, outer_radius+10,
                    -big_angle+angles, -big_angle+angles, color="black")

    # Placement of parameter labels
    xr = radii[0]*np.cos(np.array(-big_angle/2 + angles))
    yr = radii[0]*np.sin(np.array(-big_angle/2 + angles))

    label_angle = np.array(-big_angle/2+angles)
    label_angle[label_angle < -np.pi/2] += np.pi
    # Placing Labels and Legend
    p.text(xr, yr, df.Parameter, angle=label_angle,
           text_font_size="9pt", text_align="center", text_baseline="middle")

    p.rect([-40, -40, -40], [18, 0, -18], width=30, height=13,
           color=list(stat_color.values()))
    p.text([-15, -15, -15], [18, 0, -18], text=[Cols[1], Cols[0]],
           text_font_size="9pt", text_align="left", text_baseline="middle")
    output_file('HoverTrial.html', title="HoverTrial.py example")
    show(p)

sa = dp.get_sa_data()
make_plot(sa['CO'][0], 10, .001, True, True)
