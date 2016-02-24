"""
The current program is meant to draw interactive visualizations using BOKEH
and ipywidgets libraries for sensitivity analysis

Dependencies :
Currently this code needs to be run Inside Ipython notebook.
Python version :2.7

Note:
Please ensure Basic_Plot.py exists in same directory and necessary data files are
located in c:/HDSAviz_data folder

Basically files should be organized as :

C: HDSAviz_data/
C: HDSAviz_data/analysis_CO.txt
C: HDSAviz_data/analysis_CO2.txt
etc.

C: HDSAviz_data/interactivevislib.py
C: HDSAviz_data/Interactive_vis_toolkit.ipynb

"""

#import Basic_Plot  once Basic_Plot.py file is ammended.

import os
from bokeh.models.widgets import Panel, Tabs
from bokeh.io import output_file, output_notebook, show, vform
from ipywidgets import FloatSlider
from IPython.html.widgets import interact
from collections import OrderedDict
from bokeh.plotting import figure, show, output_notebook, output_file

# initializing the range of values for total order (ST) and first order
# (S1) sensitivity tests
ST_Range = 1
S1_Range = 1

def change_directory():
    """
    This function changes the working directory from C:Users/UserName to
    C:/HDSAviz_data/ which is chosen as convention for current project.

    Output:
    Changes working directory and prints current directory
    """
    path = "c:/HDSAviz_data"
    os.chdir(path)
    print 'current working directory: ' + os.getcwd()


def gather_all_analysis_files():
    """
    This function gathers all the analysis files from C:/HDSAvis_data/

    Output:
    Returns a list of analysis files that can be fed into plotting function

    """
    new = !ls
    analysis_files = []
    for files in new:
        if files.startswith("analysis"):
            analysis_files.append(files)
    print 'all analysis files gathered from current directory!'
    return analysis_files

def plot_all_outcomes_burtin(S1_Range,ST_Range):
    """
    This function plots the burtin type plots for all the outcome
    variables in different text files.

    Input :
    S1_Range: Minimum value of sensitivity for first order effects * 0.001,
    ST_Range: Minimum value of sensitivity for total order effects * 0.001

    Output:
    Tab based plotting of Graphs.
    """
    working_dir = !pwd
    if working_dir != 'C:/HDSAviz_data/' :
        change_directory()

    analysis_files = gather_all_analysis_files()
    tabs_dictionary = {}

    for i,files in zip(range(len(analysis_files)), analysis_files):
        # cleaning the file names to get a short name to occupy less
        # space in tabs.
        names = files.replace('analysis_', '' ).replace('.txt','')

        try :
            tabs_dictionary[i] = Panel(child = makeplot(files,
                                np.array(['S1', 'ST']),
                                np.array([0.001*S1_Range, 0.001*ST_Range])),
                                title = names)
        except:
            pass


    tabs = Tabs(tabs=tabs_dictionary.values())

    try :
        p = show(tabs)
        output_notebook()
    except:
        pass

    return p

def Interact_with_burtin_plots():
    """
    This function adds capability to adjust the minimum threshold for
    sensitiity plotting

    Output:
    Interactive graph displaying a slider widgets that allow for
    minimum threshold of sensitivity selection
    """
    output_notebook()
    slider1 = FloatSlider(value = 1, min = 0.1, max = 10,
                          step=0.1, title = 'S1-Range')
    slider2 = FloatSlider(value = 1, min = 0.1, max = 10,
                          step=0.1, title = 'ST-Range')
    return interact(plot_all_outcomes_burtin, S1_Range=slider1,
                    ST_Range=slider2)

def short_tabs_demo(S1_Range,ST_Range):
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
    output_notebook()
    tab1 = Panel(child = makeplot('analysis_CO.txt', np.array(['S1', 'ST']),
                                  np.array([0.001*S1_Range, 0.001*ST_Range])),
                                  title = 'CO')
    tab2 = Panel(child = makeplot('analysis_CO2.txt', np.array(['S1', 'ST']),
                                  np.array([0.001*S1_Range, 0.001*ST_Range])),
                                  title = 'CO2')
    tabs = Tabs(tabs=[tab1,tab2])
    return show(tabs)

def short_interactive_demo ():
    """
    This function adds capability to adjust the minimum threshold
    for sensitiity plotting for demo and uses only two key factors.

    Output:
    Interactive graph displaying a slider widgets that allow for
    minimum threshold of sensitivity selection
    """
    #output_notebook()
    slider1 = FloatSlider(value = 1, min = 0.1, max = 10,
                          step=0.1, title = 'S1-Range')
    slider2 = FloatSlider(value = 1, min = 0.1, max = 10,
                          step=0.1, title = 'ST-Range')
    return interact(short_tabs_demo, S1_Range = slider1,
                    ST_Range = slider2)

# for trial runs please uncomment the following when files are in
# correct folder
"""
Small demo's with two outcomes(CO and CO2) plotted as tabs.
"""
# short_tabs_demo(1,1)
# short_interactive_demo()

"""
The interactive plots for all Outcomes with all outcomes as tab.
"""

print
# plot_all_outcomes_burtin(1, 1)
# Interact_with_burtin_plots()
