"""
This library adds the interactive features to basic plots
for the sensitivity analysis

Dependencies:
plotting.py
data_processing.py
matplotlib
numpy
pandas
os
bokeh
"""

import data_processing as dp
from plotting import make_plot

import os
from collections import OrderedDict
import numpy as np
import pandas as pd
import matplotlib

from bokeh.models.widgets import Panel, Tabs
from bokeh.io import save, vform
from bokeh.plotting import figure, show, output_notebook, output_file
from bokeh.models.tools import (BoxZoomTool, ResetTool,
                                PreviewSaveTool,
                                ResizeTool,
                                PanTool, PolySelectTool,
                                WheelZoomTool)


from ipywidgets import FloatSlider, BoundedFloatText, ToggleButton,Checkbox, SelectMultiple

from IPython.html.widgets import interact


sa_dict = dp.get_sa_data()


def plot_all_outcomes_burtin(
        minimum_S1_limits_in_decimal_places, top, stacked1, error_bars, log_axis, 
                    highlighted_parameters):
    """
    This function plots the burtin type plots for all the outcome
    variables in different text files.

    Input :
    minimum_S1_limits_in_decimal_places:
    Minimum value of sensitivity for first order effects in 10^-n
    (n is input from interactive slider widget),

    minimum_ST_limits_in_decimal_places:
    Minimum value of sensitivity for total order effects in 10^-n
    (n is input from interactive slider widget)

    Output:
    Tab and slider based interactive plots of sensitivity data in
    burtins format.

    Note: This file also saves some graphs in html format which
    have tabs of all output parameters. the title i these files
    describe minimum sensitivity values used.
    """

    tabs_dictionary = {}
    deci1 = pow(10, -1*minimum_S1_limits_in_decimal_places)
    title_html = (('Single order and total order Sensitivity plots ' +
                  'showing parameters ' + 'for which S1: >= ' +
                   str(deci1) + ' and ' + 'ST: >= ' + str(deci1)))
    outcomes_array = []
    for files in sa_dict.keys():
        outcomes_array.append(sa_dict[files][0])
        # cleaning the file names to get a short name to occupy less
        # space in tabs.
    for i in range(len(sa_dict)):
        p = make_plot(outcomes_array[i], top=top,  minvalues=deci1, stacked=stacked1, errorbar=error_bars,
                  lgaxis=log_axis, highlight= highlighted_parameters)
        p.title = ('Single order and total order Sensitivity plots' +
                   'for S1: >= ' + str(deci1) + ' and ' + 'ST: >= ' +
                   str(deci1))
        p.title_text_align = 'center'
        p.title_text_font_size = '10pt'
        tabs_dictionary[i] = Panel(child=p, title=sa_dict.keys()[i])

    tabs = Tabs(tabs=tabs_dictionary.values())
    try:
        p = show(tabs), save(tabs, filename='Multitab_sensitivity_plot.html',
                             title=title_html)
        output_notebook()
    except:
        pass

    return p


def Interact_with_burtin_plots():
    """
    This function adds capability to adjust the minimum threshold for
    sensitivity plotting

    Output:
    Interactive graph displaying a slider widgets that allow for
    minimum threshold of sensitivity selection
    """
    decimal_box = BoundedFloatText(value=4, min=0, max=8, step=1,
                                   title='minimum decimal places', 
                                   description='minimum decimal places')
    top_box = BoundedFloatText(value=20, min=1, max=1000, step = 1, 
                               description='Show Top')
    stacks = Checkbox(description='Show Stacked Plots',
                          value=False,)
    error_bars = Checkbox(description='Show Error Bars', value=True)
    log_axis = Checkbox(description='Convert linear axis to log axis', value=True)
    highlighted_parameters = SelectMultiple(description="Choose parameters to be highligted", 
                                            options=list(sa_dict['CO'][0].Parameter.values))
    return interact(plot_all_outcomes_burtin,
                    minimum_S1_limits_in_decimal_places=decimal_box,
                   top=top_box, stacked1=stacks, error_bars=error_bars,
                   log_axis=log_axis, highlighted_parameters=highlighted_parameters)


def short_tabs_demo(minimum_S1_limits_in_decimal_places, top, stacked1, error_bars, log_axis, 
                    highlighted_parameters):
    """
    This function plots the burtin type plots for two outcome
    variables in CO and CO2.

    Input :
    S1_Range: Minimum value of sensitivity for first
              order effects * 0.001,
    ST_Range: Minimum value of sensitivity for total
              order effects * 0.001

    Output:
    Tab based plotting of Graphs (Only two tabs for simplicity
    and sanity check experimentation).

    """
    deci1 = pow(10, -1*minimum_S1_limits_in_decimal_places)
    p1 = make_plot(sa_dict['CO'][0], top=top,  minvalues=deci1, stacked=stacked1, errorbar=error_bars,
                  lgaxis=log_axis, highlight= highlighted_parameters)
    p1.title = ('Single order and total order Sensitivity plots' +
                'showing parameters ' +
                'for which S1: >= ' + str(deci1) + ' and ' +
                'ST: >= ' + str(deci1))
    p1.title_text_align = 'center'
    p1.title_text_font_size = '10pt'

    p2 = make_plot(sa_dict['CO2'][0], minvalues=deci1, stacked=stacked1, errorbar=error_bars,
                   lgaxis=log_axis, highlight=highlighted_parameters)
    p2.title = ('Single order and total order Sensitivity plots' +
                'showing parameters ' +
                'for which S1: >= ' + str(deci1) + ' and ' +
                'ST: >= ' + str(deci1))
    p2.title_text_align = 'center'

    p2.title_text_font_size = '10pt'

    output_notebook()

    title_html = ('first_order_S1_values_greater_than_' + str(deci1) +
                  '_and_' + 'Total_order_ST_values__greater_than_ ' +
                  str(deci1))

    tab1 = Panel(child=p1, title='CO')
    tab2 = Panel(child=p2, title='CO2')
    tabs = Tabs(tabs=[tab1, tab2])
    return show(tabs), save(tabs, filename='demo'+'.html', title=title_html)


def short_interactive_demo():
    """
    This function adds capability to adjust the minimum threshold
    for sensitiity plotting for demo and uses only two key factors.

    Output:
    Interactive graph displaying a slider widgets that allow for
    minimum threshold of sensitivity selection
    """

    decimal_box = BoundedFloatText(value=4, min=0, max=8, step=1,
                                   title='minimum decimal places', 
                                   description='minimum decimal places')
    top_box = BoundedFloatText(value=20, min=1, max=1000, step = 1, 
                               description='Show Top')
    stacks = Checkbox(description='Show Stacked Plots',
                          value=True,)
    error_bars = Checkbox(description='Show Error Bars', value=True)
    log_axis = Checkbox(description='Convert linear axis to log axis', value=True)
    highlighted_parameters = SelectMultiple(description="Choose parameters to be highligted", 
                                            options=list(sa_dict['CO'][0].Parameter.values))
    return interact(short_tabs_demo,
                    minimum_S1_limits_in_decimal_places=decimal_box,
                   top=top_box, stacked1=stacks, error_bars=error_bars,
                   log_axis=log_axis, highlighted_parameters=highlighted_parameters)


# for trial runs please uncomment the following when files are in
# correct folder
"""
Small demo's with two outcomes(CO and CO2) plotted as tabs.
"""
# short_tabs_demo(4,4)
# short_interactive_demo()

"""
The interactive plots for all Outcomes with all outcomes as tab.
"""

# plot_all_outcomes_burtin(4, 4)
# Interact_with_burtin_plots()
