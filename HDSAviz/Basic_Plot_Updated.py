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
                          WheelZoomTool, HoverTool, BoxSelectTool)

# import data_processing as dp


def make_plot(Dataframe, Cols=np.array(['S1', 'S2']), minvalues):
    """Basic method to plot sensitivity anlaysis.

    This is the method to generate a bokeh plot followung the burtin example
    template at the bokeh website. For clarification, parameters refer to an
    output being measured (Tmax, C, k2, etc.) and stats refer to the 1st or
    total order sensitivity index.

    Parameters:
    --------------
    Dataframe : Dataframe containing sensitivity analysis results to be plotted
                {Name of csv file to be read into as a panda dataframe (String)
                **Note file must be in same folder as script.**}
                Delete upon change
    Cols: Names of the columns to be plotted (Array of strings)
    minvalues: Cutoff minimum for which parameters should be plotted (Array of
                floats)
    Returns:
    ---------------
    p: Figure of the data to be plotted
    """
    # Read in csv file as panda dataframe.
    tdf = pd.read_csv(Dataframe, delimiter=' ', skipinitialspace=True,
                      engine='python')
    df = tdf
    # df = Dataframe
    maxval = 0
    # Remove rows which have values less than cutoff values
    for i in range(0, minvalues.size):
        df = df[df[Cols[i]] > minvalues[i]]
        if maxval < max(df[Cols[i]]):
            maxval = max(df[Cols[i]])
    df = df.dropna()

    # Create dictionary of bar colors, assume up to 3 stats are plotted
    # per parameter.
    colors = ["#0d3362", "#c64737", "black"]
    stat_color = OrderedDict()
    for i in range(0, Cols.size):
        stat_color[i] = colors[i]
    # Reset index of dataframe.
    df = df.sort(Cols[1], ascending=False)
    df = df.reset_index(drop=True)
    # Sizing parameters
    width = 800
    height = 800
    inner_radius = 90
    outer_radius = 300 - 10

    # Determine wedge size based off number of parameters
    big_angle = 2.0 * np.pi / (len(df)+1)
    # Determine division of wedges for plotting bars based on # stats plotted
    small_angle = big_angle / (minvalues.size+2)
    # pdb.set_trace()
    # params = df['Parameter']
    # S1vals = df['S1']
    # S1vals = df['ST']

    plottools = "resize,save,pan,box_zoom,wheel_zoom"

    p = figure(plot_width=width, plot_height=height, title="",
               x_axis_type=None, y_axis_type=None,
               x_range=(-420, 420), y_range=(-420, 420),
               min_border=0, outline_line_color="black",
               background_fill_color="#f0e1d2", border_fill_color="#f0e1d2",
               tools=plottools)
    # p.select_one(HoverTool).tooltips = [
    # ('Parameter', '@params')]

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # annular wedges divided into smaller sections for bars
    angles = np.pi/2 - big_angle/2 - df.index.to_series()*big_angle
    # circular axes and labels
    labels = np.power(10.0, np.arange(0, -5, -1))
    extra_labels = np.power(10.0, np.arange(-0.30103, -4.30103, -1))
    # Re-size if no values are above 0.1
    if maxval < 0.1:
        labels = np.delete(labels, 0)
    # Size of radii of each label
    # pdb.set_trace()
    extra_radii = (((np.log10(extra_labels / labels[0])) + labels.size) *
                   (outer_radius - inner_radius) / labels.size + inner_radius)
    radii = (((np.log10(labels / labels[0])) + labels.size) *
             (outer_radius - inner_radius) / labels.size + inner_radius)

    # Add zero label to labels and radii
    labels = np.append(labels, 0.0)
    radii = np.append(radii, inner_radius)
    extra_radii = np.append(extra_radii, radii)

    # Adding axis lines and labels
    p.circle(0, 0, radius=extra_radii, fill_color=None, line_color="white")
    p.text(0, radii[:], [str(r) for r in labels[:]],
           text_font_size="8pt", text_align="center", text_baseline="middle")

    # Plot the values of each stat for each parameter.
    # radius of stat is the value of a statistic converted to the radial
    # value.
    for statistic in range(0, Cols.size):
        radius_of_stat = (((np.log10(df[Cols[statistic]] / labels[0])) +
                          labels.size) * (outer_radius - inner_radius) /
                          labels.size + inner_radius)
        p.annular_wedge(0, 0, inner_radius, radius_of_stat,
                        -big_angle + angles + (2*statistic + 1)*small_angle,
                        -big_angle + angles + (2*statistic + 2)*small_angle,
                        color=stat_color[statistic])
    # radial axes

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
    p.text([-15, -15, -15], [18, 0, -18], text=Cols,
           text_font_size="9pt", text_align="left", text_baseline="middle")
    output_file('unemployment.html', title="unemployment.py example")
    show(p)
make_plot('../../HDSAviz_data/analysis_CO.txt', np.array(['S1', 'ST']),
          np.array([0.005, 0.005]))
