**************************
Getting Started with savvy
**************************

================
Installing savvy
================

Clone the github repo: https://github.com/houghb/savvy.git

In command line, enter the the savvy repo and run the command:

``python setup.py install``

This will install savvy on your machine so it can be called anywhere!

============================
Installing required packages
============================

In command line, enter the the savvy repo and run the command:
``pip install -r requirements.txt``

This will install the following packaged required to run savvy:

* numpy 1.10.4
* pandas 0.18.0
* Bokeh 0.11.1
* matplotlib 1.5.1
* ipywidgets 4.1.1
* SALib 0.7.1 (To perform sensitivity analysis)

*graph-tool is excluded because it cannot be installed via pip install

===============================
Installing graph-tool (for mac)
===============================
This method of installation requires the use of Homebrew.
For other options see https://graph-tool.skewed.de/download

Using Homebrew in the command line, enter the following commands:
``brew tap homebrew/science``

``brew install graph-tool``

====================
Quick Start Tutorial
====================
This is a quick start that generates a radial plot, heatmap, and network plot using sample datafiles.

.. code:: python

  import copy

  from bokeh.plotting import show, output_notebook
  import os.path as op

  import savvy
  import savvy.data_processing as dp
  import savvy.interactive_plots as ip
  from savvy.plotting import make_plot, make_second_order_heatmap
  import savvy.network_tools as nt

  output_notebook()

  # path to sample data files
  path = op.join(savvy.__path__[0], 'sample_data_files/')

  # store all of the data files into a dictionary
  sa_dict = dp.get_sa_data(path)

  # create interactive radial plots (or bar charts)
  ip.interact_with_plot_all_outputs(sa_dict)

  # Plot the second order plots with tabs for all the options
  ip.plot_all_second_order(sa_dict, top=5, mirror=True)


  # Network plot of the second order interactions
  # and first/total order indices
  # (set inline to false for an interactive window)
  sa_dict_net = copy.deepcopy(sa_dict)
  g = nt.build_graph(sa_dict_net['sample-output1'], sens='ST', top=40,
                     min_sens=0.01, edge_cutoff=0.0)
  nt.plot_network_circle(g, inline=True)
