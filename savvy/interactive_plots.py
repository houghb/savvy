"""
This modules adds interactivity to plots in plotting.py through Bokeh tabs and
ipython widgets.

Dependencies:
plotting.py
data_processing.py
matplotlib
numpy
pandas
os
bokeh
ipywidgets
collections

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from bokeh.models.widgets import Panel, Tabs
from bokeh.plotting import show
from ipywidgets import BoundedFloatText, IntText, Checkbox, SelectMultiple
from IPython.html.widgets import interact, fixed

from .plotting import make_plot, make_second_order_heatmap

import warnings; warnings.filterwarnings('ignore')

def plot_all_outputs(sa_dict, demo=False, min_val=0.01, top=100, stacked=True,
                     error_bars=True, log_axis=True,
                     highlighted_parameters=[]):
    """
    This function calls plotting.make_plot() for all the sensitivity
    analysis output files and lets you choose which output to view
    using tabs.

    Parameters
    -----------
    sa_dict                : dict
                             a dictionary with all the sensitivity analysis
                             results.
    demo                   : bool, optional
                             plot only two outcomes instead of all outcomes
                             for demo purpose.
    min_val                : float, optional
                             a float indicating the minimum sensitivity value
                             to be shown.
    top                    : int, optional
                             integer indicating the number of parameters to
                             display (highest sensitivity values).
    stacked                : bool, optional
                             Boolean indicating in bars should be stacked for
                             each parameter.
    error_bars             : bool, optional
                             Boolean indicating if error bars are shown (True)
                             or are omitted (False).
    log_axis               : bool, optional
                             Boolean indicating if log axis should be used
                             (True) or if a linear axis should be used (False).
    highlighted_parameters : list, optional
                             List of strings indicating which parameter wedges
                             will be highlighted.

    Returns
    --------
    p : bokeh plot
        a Bokeh plot generated with plotting.make_plot() that includes tabs
        for all the possible outputs.
    """

    tabs_dictionary = {}
    outcomes_array = []
    if demo:
        for files in sa_dict.keys()[0:2]:
            outcomes_array.append(sa_dict[files][0])
    else:
        for files in sa_dict.keys():
            outcomes_array.append(sa_dict[files][0])

    for i in range(len(outcomes_array)):
        p = make_plot(outcomes_array[i],
                      top=top,
                      minvalues=min_val,
                      stacked=stacked,
                      errorbar=error_bars,
                      lgaxis=log_axis,
                      highlight=highlighted_parameters
                      )
        tabs_dictionary[i] = Panel(child=p, title=list(sa_dict.keys())[i])

    tabs = Tabs(tabs=list(tabs_dictionary.values()))
    p = show(tabs)

    return p


def interact_with_plot_all_outputs(sa_dict, demo=False, manual=True):
    """
    This function adds the ability to interactively adjust all of the
    plotting.make_plot() arguments.

    Parameters
    ----------
    sa_dict : dict
              a dictionary with all the sensitivity analysis results.
    demo    : bool, optional
              plot only few outcomes for demo purpose.

    Returns
    -------
    Interactive widgets to control plot
    """
    min_val_box = BoundedFloatText(value=0.01, min=0, max=1,
                                   description='Min value:')
    top_box = IntText(value=20, description='Show top:')
    stacks = Checkbox(description='Show stacked plots:', value=True,)
    error_bars = Checkbox(description='Show error bars:', value=True)
    log_axis = Checkbox(description='Use log axis:', value=True)

    # get a list of all the parameter options
    key = list(sa_dict.keys())[0]
    param_options = list(sa_dict[key][0].Parameter.values)
    highlighted = SelectMultiple(description="Choose parameters to highlight",
                                 options=param_options, value=[])

    return interact(plot_all_outputs,
                    sa_dict=fixed(sa_dict),
                    demo = fixed(demo),
                    min_val=min_val_box,
                    top=top_box,
                    stacked=stacks,
                    error_bars=error_bars,
                    log_axis=log_axis,
                    highlighted_parameters=highlighted,
                    __manual=manual
                    )


def plot_all_second_order(sa_dict, top=5, mirror=True, include=[]):
    """
    This function calls plotting.make_second_order_heatmap() for all the
    sensitivity analysis output files and lets you choose which output to view
    using tabs

    Parameters
    -----------
    sa_dict : dict
              a dictionary with all the sensitivity analysis results.
    top     : int, optional
              the number of parameters to display
              (highest sensitivity values).
    include : list, optional
              a list of parameters you would like to include even if they
              are not in the top `top` values.

    Returns
    --------
    p : bokeh plot
        a Bokeh plot that includes tabs for all the possible outputs.
    """

    tabs_dictionary = {}
    outcomes_array = []

    for files in sa_dict.keys():
        outcomes_array.append(sa_dict[files][1])

    for i in range(len(sa_dict)):
        p = make_second_order_heatmap(outcomes_array[i],
                                      top=top,
                                      mirror=mirror,
                                      include=include
                                      )
        tabs_dictionary[i] = Panel(child=p, title=list(sa_dict.keys())[i])

    tabs = Tabs(tabs=list(tabs_dictionary.values()))
    p = show(tabs)

    return p

import warnings; warnings.filterwarnings('ignore')
