"""
This module creates plots for visualizing sensitivity analysis dataframes.

- make_plot() creates a radial plot of the first and total order indices.
- make_second_order_heatmap() creates a square heatmap showing the second
order interactions between model parameters.
"""
from collections import OrderedDict

import numpy as np
import pandas as pd

from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import HoverTool
from bokeh.charts import Bar


def make_plot(dataframe,  top=100, minvalues=0.01, stacked=True, lgaxis=True):
    """Basic method to plot sensitivity anlaysis.

    This is the method to generate a bokeh plot similar to the burtin example
    template at the bokeh website. For clarification, parameters refer to an
    input being measured (Tmax, C, k2, etc.) and stats refer to the 1st or
    total order sensitivity index.

    Parameters:
    -----------
    dataframe : Dataframe containing sensitivity analysis results to be plotted

    top: Integer indicating the number of parameters to display (highest
                 sensitivity values)

    minvalues: Cutoff minimum for which parameters should be plotted (float)

    stacked: Boolean indicating in bars should be stacked for each parameter.

    lgaxis: Boolean indicating if log axis should be used (True) or if a
            linear axis should be used (False).

    Returns:
    --------
    p: Figure of the data to be plotted
    """
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
    colors = ["#a1d99b", "#31a354", "#546775", "#225ea8"]
    s1color = np.array(["#31a354"]*df.S1.size)
    sTcolor = np.array(["#a1d99b"]*df.ST.size)
    errs1color = np.array(["#225ea8"]*df.S1.size)
    errsTcolor = np.array(["#546775"]*df.ST.size)
    firstorder = np.array(["1st (S1)"]*df.S1.size)
    totalorder = np.array(["Total (ST)"]*df.S1.size)

    if len(df) <= 5:
        if stacked is False:
            data = {
                    'Sensitivity': pd.Series.append(df.ST, df.S1),
                    'Parameter': pd.Series.append(df.Parameter, df.Parameter),
                    'Order': np.append(np.array(['ST']*len(df)),
                                       np.array(['S1']*len(df))),
                    'Confidence': pd.Series.append(df.ST_conf,
                                                   df.S1_conf)
                    }
            p = Bar(data, values='Sensitivity', label=['Parameter'],
                    group='Order', legend='top_right',
                    color=["#31a354", "#a1d99b"])
        else:
            data = {
                    'Sensitivity': pd.Series.append(df.S1, (df.ST-df.S1)),
                    'Parameter': pd.Series.append(df.Parameter, df.Parameter),
                    'Order': np.append(np.array(['S1']*len(df)),
                                       np.array(['ST']*len(df))),
                    'Confidence': pd.Series.append(df.S1_conf,
                                                   df.ST_conf)
                    }
            p = Bar(data, values='Sensitivity', label=['Parameter'],
                    color=['Order'], legend='top_right',
                    stack='Order', palette=["#31a354", "#a1d99b"])
        return p

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
        small_angle = big_angle / 5
    else:
        small_angle = big_angle / 3

    plottools = "hover, wheel_zoom, save, reset, resize"  # , tap"
    # Initialize figure with tools, coloring, etc.
    p = figure(plot_width=width, plot_height=height, title="",
               x_axis_type=None, y_axis_type=None,
               x_range=(-350, 350), y_range=(-350, 350),
               min_border=0, outline_line_color="#e6e6e6",
               background_fill_color="#e6e6e6", border_fill_color="#e6e6e6",
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
    cols = np.array(['S1', 'ST'])
    for statistic in range(0, 2):
        if lgaxis is True:
            radius_of_stat = (((np.log10(df[cols[statistic]] / labels[0])) +
                              labels.size) * (outer_radius - inner_radius) /
                              labels.size + inner_radius)
            lower_of_stat = (((np.log10((df[cols[statistic]] -
                               df[cols[statistic]+'_conf']) / labels[0])) +
                              labels.size) * (outer_radius - inner_radius) /
                             labels.size + inner_radius)
            higher_of_stat = (((np.log10((df[cols[statistic]] +
                               df[cols[statistic]+'_conf']) / labels[0])) +
                              labels.size) * (outer_radius - inner_radius) /
                              labels.size + inner_radius)
        else:

            radius_of_stat = ((outer_radius - inner_radius) *
                              df[cols[statistic]]/labels[0] + inner_radius)
            lower_of_stat = ((outer_radius - inner_radius) *
                             (df[cols[statistic]] -
                             df[cols[statistic]+'_conf'])/labels[0] +
                             inner_radius)
            higher_of_stat = ((outer_radius - inner_radius) *
                              ((df[cols[statistic]] +
                               df[cols[statistic]+'_conf'])/labels[0]) +
                              inner_radius)

        if stacked is False:
            startA = -big_angle + angles + (2*statistic + 1)*small_angle
            stopA = -big_angle + angles + (2*statistic + 2)*small_angle
            df[cols[statistic]+'_err_angle'] = pd.Series((startA+stopA)/2,
                                                         index=df.index)
        else:
            startA = -big_angle + angles + (1)*small_angle
            stopA = -big_angle + angles + (2)*small_angle
            if statistic == 0:
                df[cols[statistic]+'_err_angle'] = pd.Series((startA*2 +
                                                              stopA)/3,
                                                             index=df.index)
            if statistic == 1:
                df[cols[statistic]+'_err_angle'] = pd.Series((startA +
                                                              stopA*2)/3,
                                                             index=df.index)
        df[cols[statistic]+'radial'] = pd.Series(radius_of_stat,
                                                 index=df.index)
        df[cols[statistic]+'upper'] = pd.Series(higher_of_stat,
                                                index=df.index)
        df[cols[statistic]+'lower'] = pd.Series(lower_of_stat,
                                                index=df.index)
        df[cols[statistic]+'_start_angle'] = pd.Series(startA,
                                                       index=df.index)
        df[cols[statistic]+'_stop_angle'] = pd.Series(stopA,
                                                      index=df.index)

        # df[cols[statistic]+'_err_angle'] = pd.Series((startA+stopA)/2,
        #                                              index=df.index)
        inner_rad = np.ones_like(angles)*inner_radius
        df[cols[statistic]+'lower'] = df[cols[statistic]+'lower'].fillna(90)
    # Store plotted values into dictionary to be add glyphs
    pdata = pd.DataFrame({
                         'x': np.append(np.zeros_like(inner_rad),
                                        np.zeros_like(inner_rad)),
                         'y': np.append(np.zeros_like(inner_rad),
                                        np.zeros_like(inner_rad)),
                         'ymin': np.append(inner_rad, inner_rad),
                         'ymax': pd.Series.append(df[cols[1]+'radial'],
                                                  df[cols[0]+'radial']
                                                  ).reset_index(drop=True),
                         'starts': pd.Series.append(df[cols[1] +
                                                    '_start_angle'],
                                                    df[cols[0] +
                                                    '_start_angle']
                                                    ).reset_index(drop=True),
                         'stops': pd.Series.append(df[cols[1] +
                                                      '_stop_angle'],
                                                   df[cols[0] +
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
                    color="#999999")
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

    return p


def make_second_order_heatmap(df, top=20, name='', mirror=True, include=[]):
    """
    Plot a heat map of the second order sensitivity indices from a given
    dataframe.  If you are choosing a high value of `top` then making
    this plot gets expensive and it is recommended to set mirror to False.

    Parameters:
    -----------
    df     : The dataframe with second order sensitivity indices. This
             dataframe should be formatted in the standard output format
             from a Sobol sensitivity analysis in SALib.
    top    : An integer specifying the number of parameter interactions to
             plot (those with the 'top' greatest values are displayed).
    name   : An optional string indicating the name of the output measure
             you are plotting.
    mirror : A boolean indicating whether you would like to plot the mirror
             image (reflection across the y=-1 axis).  This mirror image
             contains the same information as plotted already, but will increase
             the computation time for large dataframes.
    include: a list of parameters that you would like to make sure are shown
             on the heatmap (even if they are not in the top subset you specify)

    Returns:
    --------
    p : A bokeh figure to be plotted
    """

    # Colormap to use for plot
    colors = ["#f7fbff", "#deebf7", "#c6dbef", "#9ecae1", "#6baed6",
              "#4292c6", "#2171b5", "#08519c", "#08306b"]

    # Make a new dataframe with only the top parameters
    df_top = df.sort_values('S2', ascending=False).head(top)
#     df = df.head(top)
#     df = df.reset_index(drop=True)

    # Make a list of all the parameters that interact with each other
    labels = list(set(
        [x for x in pd.concat([df_top.Parameter_1, df_top.Parameter_2])]))
    for item in include:
        if item not in labels:
            labels.append(item)
    xlabels = labels
    ylabels = labels

    # Use this to scale the heatmap so the max sensitivity index is darkest
    maxval = round(np.max(df.S2), 2)

    xlabel = []
    ylabel = []
    color = []
    s2 = []
    s2_conf = []
    for px in xlabels:
        for py in ylabels:
            xlabel.append(px)
            ylabel.append(py)
            # sens is a dataframe with S2 and S2_conf that is stored for
            # each box of the heatmap
            sens = (df[df.Parameter_1.isin([px]) & df.Parameter_2.isin([py])]
                    .ix[:, ['S2', 'S2_conf']])
            # dfs can be empty if there are no corresponding pairs in the
            # source dataframe (for example a parameter interacting with
            # itself).
            if sens.empty and not mirror:
                s2.append(float('NaN'))
                s2_conf.append(float('NaN'))
                color.append("#b3b3b3")
            elif sens.empty and mirror:
                # This heat map is symmetric across the diagonal, so this
                # if statement populates the mirror image if you've chosen to
                sens_mirror = (df[df.Parameter_1.isin([py]) &
                                  df.Parameter_2.isin([px])]
                               .ix[:, ['S2', 'S2_conf']])
                if sens_mirror.empty:
                    s2.append(float('NaN'))
                    s2_conf.append(float('NaN'))
                    color.append("#b3b3b3")
                else:
                    s2.append(sens_mirror.S2.values[0])
                    s2_conf.append(sens_mirror.S2_conf.values[0])
                    color.append(colors[int(round((sens_mirror.S2.values[0] /
                                                   maxval) * 7) + 1)])
            else:
                s2.append(sens.S2.values[0])
                s2_conf.append(sens.S2_conf.values[0])
                color.append(colors[int(round((sens.S2.values[0] /
                                               maxval) * 7) + 1)])

    source = ColumnDataSource(data=dict(xlabel=xlabel, ylabel=ylabel, s2=s2,
                              s2_conf=s2_conf, color=color))

    plottools = "resize,hover,save,pan,box_zoom,wheel_zoom"
    p = figure(title="%s second order sensitivities" % name,
               x_range=list(reversed(labels)), y_range=labels,
               x_axis_location="above", plot_width=700, plot_height=700,
               toolbar_location="right", tools=plottools)

    p.grid.grid_line_color = None
    p.axis.axis_line_color = None
    p.axis.major_tick_line_color = None
    p.axis.major_label_text_font_size = "8pt"
    p.axis.major_label_standoff = 0
    p.xaxis.major_label_orientation = 1.1

    p.rect("xlabel", "ylabel", 1, 1, source=source,
           color="color", line_color=None)

    p.select_one(HoverTool).tooltips = [
        ('Interaction', '@xlabel-@ylabel'),
        ('S2', '@s2'),
        ('S2_conf', '@s2_conf'),
        ]

    return p
