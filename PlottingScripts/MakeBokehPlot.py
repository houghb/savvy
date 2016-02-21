"""This is a basic script for plotting an analysis file."""
from collections import OrderedDict

import numpy as np
import pandas as pd
# import pdb

from bokeh.plotting import figure, show, output_file


def makeplot(Dataframe, Cols, minvalues):
    """Basic method to plot sensitivity anlaysis.

    Template taken from Bokeh wedsite.

    Inputs:
    Dataframe - Name of csv file to be read into as a panda dataframe (String)
    Cols- Names of the columns to be plotted (Array of strings)
    minvalues- Cutoff minimum for which parameters should be plotted (Array of
                floats)
    Outputs:
    Generates an html of the plot.
    """
    # Read in csv file as panda dataframe.
    tdf = pd.read_csv(Dataframe, delimiter=' ', skipinitialspace=True,
                      engine='python')
    df = tdf
    maxval = 0
    # Remove rows which have values less than cutoff values
    for i in range(0, minvalues.size):
        df = df[df[Cols[i]] > minvalues[i]]
        if maxval < max(df[Cols[i]]):
            maxval = max(df[Cols[i]])
    df = df.dropna()

    # Create dictionary of bar colors, assume max stats plotted
    colors = ["#0d3362", "#c64737", "black"]
    stat_color = OrderedDict()
    for i in range(0, Cols.size):
        stat_color[i] = colors[i]

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

    p = figure(plot_width=width, plot_height=height, title="",
               x_axis_type=None, y_axis_type=None,
               x_range=(-420, 420), y_range=(-420, 420),
               min_border=0, outline_line_color="black",
               background_fill="#f0e1d2", border_fill="#f0e1d2")

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # annular wedges
    angles = np.pi/2 - big_angle/2 - df.index.to_series()*big_angle
    # circular axes and lables
    labels = np.power(10.0, np.arange(0, -5, -1))
    # Re-size if no values are above 0.1
    if maxval < 0.1:
        labels = np.delete(labels, 0)

    radii = (-(outer_radius - inner_radius)*1 / (np.log10(labels / labels[0]) -
                                                 1) + inner_radius)
    labels = np.append(labels, 0.0)
    radii = np.append(radii, inner_radius)

    p.circle(0, 0, radius=radii, fill_color=None, line_color="white")
    p.text(0, radii[:], [str(r) for r in labels[:]],
           text_font_size="8pt", text_align="center", text_baseline="middle")

    for c in range(0, Cols.size):
        p.annular_wedge(0, 0, inner_radius, - (outer_radius - inner_radius) *
                        1 / (np.log10(df[Cols[c]] / labels[0]) - 1) +
                        inner_radius,
                        -big_angle + angles + (2*c + 1)*small_angle,
                        -big_angle + angles + (2*c + 2)*small_angle,
                        color=stat_color[c])
    # radial axes
    p.annular_wedge(0, 0, inner_radius-10, outer_radius+10,
                    -big_angle+angles, -big_angle+angles, color="black")

    # bacteria labels
    xr = radii[0]*np.cos(np.array(-big_angle/2 + angles))
    yr = radii[0]*np.sin(np.array(-big_angle/2 + angles))

    label_angle = np.array(-big_angle/2+angles)
    label_angle[label_angle < -np.pi/2] += np.pi

    p.text(xr, yr, df.Parameter, angle=label_angle,
           text_font_size="9pt", text_align="center", text_baseline="middle")

    p.rect([-40, -40, -40], [18, 0, -18], width=30, height=13,
           color=list(stat_color.values()))
    p.text([-15, -15, -15], [18, 0, -18], text=Cols,
           text_font_size="9pt", text_align="left", text_baseline="middle")

    output_file("burtin.html", title="burtin.py example")
    show(p)


makeplot('analysis_CO.txt', np.array(['S1', 'ST']), np.array([0.001, 0.001]))
