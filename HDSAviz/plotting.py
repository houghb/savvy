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

    # Remove rows which have values less than cutoff values
    df = df[df['S1'] > minvalues]
    df = df[df['ST'] > minvalues]
    df = df.dropna()

    # Only keep top values indicated by variable top
    df = df.sort_values('ST', ascending=False)
    df = df.head(top)
    df = df.reset_index(drop=True)

    # Create arrays of colors and order labels for plotting
    colors = ["#a1d99b", "#31a354", "#546775", "#a8cfeb"]
    s1color = np.array(["#31a354"]*df.S1.size)
    sTcolor = np.array(["#a1d99b"]*df.ST.size)
    errs1color = np.array(["#a8cfeb"]*df.S1.size)
    errsTcolor = np.array(["#546775"]*df.ST.size)
    firstorder = np.array(["1st (S1)"]*df.S1.size)
    totalorder = np.array(["Total (ST)"]*df.S1.size)

    # Create Dictionary of colors
    stat_color = OrderedDict()
    error_color = OrderedDict()
    for i in range(0, 2):
        stat_color[i] = colors[i]
    # Reset index of dataframe.
    for i in range(2, 4):
        error_color[i] = colors[i]
    # Sizing parameters
    width = 800
    height = 800
    inner_radius = 90
    outer_radius = 300 - 10

    # Determine wedge size based off number of parameters
    big_angle = 2.0 * np.pi / (len(df)+1)
    # Determine division of wedges for plotting bars based on # stats plotted
    # for stacked or unstacked bars
    if stacked is False:
        small_angle = big_angle / (5)
    else:
        small_angle = big_angle / (3)
    # pdb.set_trace()
    # params = df['Parameter']
    # S1vals = df['S1']
    # S1vals = df['ST']

    # plottools = [BoxZoomTool(), ResetTool(), PreviewSaveTool(),
    #             ResizeTool(), PanTool(), PolySelectTool(),
    #             WheelZoomTool(), HoverTool(), BoxSelectTool()]
    plottools = "hover, wheel_zoom, save, reset, resize"  # , tap"
    # Initialize figure with tools, coloring, etc.
    p = figure(plot_width=width, plot_height=height, title="",
               x_axis_type=None, y_axis_type=None,
               x_range=(-420, 420), y_range=(-420, 420),
               min_border=0, outline_line_color="black",
               background_fill_color="#f2f2f2", border_fill_color="#f2f2f2",
               tools=plottools)
    # Specify labels for hover tool
    hover = p.select(dict(type=HoverTool))
    hover.tooltips = [("Order", "@Order"), ("Parameter", "@Param"),
                      ("Sensitivity", "@Sens"), ("Confidence", "@Conf")]
    hover.point_policy = "follow_mouse"

    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None

    # annular wedges divided into smaller sections for bars
    # Angles for axial line placement
    num_lines = np.arange(0, len(df)+1, 1)
    line_angles = np.pi/2 - big_angle/2 - num_lines*big_angle

    # Angles for data placement
    angles = np.pi/2 - big_angle/2 - df.index.to_series()*big_angle

    # circular axes and labels
    labels = np.power(10.0, np.arange(0, -3, -1))

    # Set max radial line to correspond to 1.1 * maximum value + error
    maxvalST = max(df.ST+df.ST_conf)
    maxvalS1 = max(df.S1+df.S1_conf)
    maxval = max(maxvalST, maxvalS1)
    labels = np.append(labels, 0.0)
    labels[0] = round(1.1*maxval, 1)

    # Determine if radial axis are log or linearly scaled
    if lgaxis is True:
            radii = (((np.log10(labels / labels[0])) +
                     labels.size) * (outer_radius - inner_radius) /
                     labels.size + inner_radius)
            radii[-1] = inner_radius
    else:
        labels = np.delete(labels, -2)
        radii = (outer_radius - inner_radius)*labels/labels[0] + inner_radius

    # Adding axis lines and labels
    p.circle(0, 0, radius=radii, fill_color=None, line_color="white")
    p.text(0, radii[:], [str(r) for r in labels[:]],
           text_font_size="8pt", text_align="center", text_baseline="middle")

    # Convert sensitivity values to the plotted values
    # Same conversion as for the labels above
    # Also calculate the angle to which the bars are placed
    # Add values to the dataframe for future reference
    Cols = np.array(['S1', 'ST'])
    for statistic in range(0, 2):
        if lgaxis is True:
            radius_of_stat = (((np.log10(df[Cols[statistic]] / labels[0])) +
                              labels.size) * (outer_radius - inner_radius) /
                              labels.size + inner_radius)
            lower_of_stat = (((np.log10((df[Cols[statistic]] -
                               df[Cols[statistic]+'_conf']) / labels[0])) +
                              labels.size) * (outer_radius - inner_radius) /
                             labels.size + inner_radius)
            higher_of_stat = (((np.log10((df[Cols[statistic]] +
                               df[Cols[statistic]+'_conf']) / labels[0])) +
                              labels.size) * (outer_radius - inner_radius) /
                              labels.size + inner_radius)
        else:

            radius_of_stat = ((outer_radius - inner_radius) *
                              df[Cols[statistic]]/labels[0] + inner_radius)
            lower_of_stat = ((outer_radius - inner_radius) *
                             (df[Cols[statistic]] -
                             df[Cols[statistic]+'_conf'])/labels[0] +
                             inner_radius)
            higher_of_stat = ((outer_radius - inner_radius) *
                              ((df[Cols[statistic]] +
                               df[Cols[statistic]+'_conf'])/labels[0]) +
                              inner_radius)

        if stacked is False:
            startA = -big_angle + angles + (2*statistic + 1)*small_angle
            stopA = -big_angle + angles + (2*statistic + 2)*small_angle
            df[Cols[statistic]+'_err_angle'] = pd.Series((startA+stopA)/2,
                                                         index=df.index)
        else:
            startA = -big_angle + angles + (1)*small_angle
            stopA = -big_angle + angles + (2)*small_angle
            if statistic == 0:
                df[Cols[statistic]+'_err_angle'] = pd.Series((startA*2 +
                                                              stopA)/3,
                                                             index=df.index)
            if statistic == 1:
                df[Cols[statistic]+'_err_angle'] = pd.Series((startA +
                                                              stopA*2)/3,
                                                             index=df.index)
        df[Cols[statistic]+'radial'] = pd.Series(radius_of_stat,
                                                 index=df.index)
        df[Cols[statistic]+'upper'] = pd.Series(higher_of_stat,
                                                index=df.index)
        df[Cols[statistic]+'lower'] = pd.Series(lower_of_stat,
                                                index=df.index)
        df[Cols[statistic]+'_start_angle'] = pd.Series(startA,
                                                       index=df.index)
        df[Cols[statistic]+'_stop_angle'] = pd.Series(stopA,
                                                      index=df.index)

        # df[Cols[statistic]+'_err_angle'] = pd.Series((startA+stopA)/2,
        #                                              index=df.index)
        inner_rad = np.ones_like(angles)*inner_radius
        df[Cols[statistic]+'lower'] = df[Cols[statistic]+'lower'].fillna(90)
    # Store plotted values into dictionary to be add glyphs
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
                         'Error Colors': np.append(errsTcolor, errs1color),
                         'Conf': pd.Series.append(df.ST_conf,
                                                        df.S1_conf
                                                  ).reset_index(drop=True),
                         'Order': np.append(totalorder, firstorder),
                         'Sens': pd.Series.append(df.ST, df.S1
                                                  ).reset_index(drop=True),
                         'Lower': pd.Series.append(df.STlower,
                                                   df.S1lower
                                                   ).reset_index(drop=True),
                         'Upper': pd.Series.append(df.STupper,
                                                   df.S1upper,
                                                   ).reset_index(drop=True),
                         'Err_Angle': pd.Series.append(df.ST_err_angle,
                                                       df.S1_err_angle,
                                                       ).reset_index(drop=True)
                         })

    pdata_s = ColumnDataSource(pdata)
    # Specify that the plotted bars are the only thing to activate hovertool
    hoverable = p.annular_wedge(x='x', y='y', inner_radius='ymin',
                                outer_radius='ymax',
                                start_angle='starts',
                                end_angle='stops',
                                color='Colors',
                                source=pdata_s
                                )
    hover.renderers = [hoverable]

    # dictdata = df.set_index('Parameter').to_dict()

    # plot lines to separate parameters
    p.annular_wedge(0, 0, inner_radius-10, outer_radius+10,
                    -big_angle+line_angles, -big_angle+line_angles,
                    color="black")
    p.annular_wedge(0, 0, pdata['Lower'], pdata['Upper'],
                    pdata['Err_Angle'],
                    pdata['Err_Angle'],
                    color=pdata['Error Colors'])

    p.annular_wedge(0, 0, pdata['Lower'], pdata['Lower'],
                    pdata['starts'],
                    pdata['stops'],
                    color=pdata['Error Colors'])

    p.annular_wedge(0, 0, pdata['Upper'], pdata['Upper'],
                    pdata['starts'],
                    pdata['stops'],
                    color=pdata['Error Colors'])
    # Placement of parameter labels
    xr = (radii[0]*1.1)*np.cos(np.array(-big_angle/2 + angles))
    yr = (radii[0]*1.1)*np.sin(np.array(-big_angle/2 + angles))

    label_angle = np.array(-big_angle/2+angles)
    label_angle[label_angle < -np.pi/2] += np.pi

    # Placing Labels and Legend
    legend_text = ['ST', 'ST Conf', 'S1', 'S1 Conf']
    p.text(xr, yr, df.Parameter, angle=label_angle,
           text_font_size="9pt", text_align="center", text_baseline="middle")

    p.rect([-40, -40], [30, -10], width=30, height=13,
           color=list(stat_color.values()))
    p.rect([-40, -40], [10, -30], width=30, height=1,
           color=list(error_color.values()))
    p.text([-15, -15, -15, -15], [30, 10, -10, -30], text=legend_text,
           text_font_size="9pt", text_align="left", text_baseline="middle")
    # output_file('HoverTrial.html', title="HoverTrial.py example")
    # show(p)
    return p
# sa = dp.get_sa_data()

# make_plot(sa['totaltars'][0], 20, 0, True, True)
