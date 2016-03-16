******************
savvy Requirements
******************

These are the dependencies for full functionality in savvy.  Version numbers
are the versions used when developing savvy which are known to work.

Minimum requirements:

* Python - 2.7
* NumPy - 1.10.4
* pandas - 0.18.0
* Bokeh - 0.11.1
* matplotlib - 1.5.1
* ipywidgets - 4.1.1
* Jupyter - 1.0.0


For full functionality:

* SALib - 0.7.1
* graph-tool - 2.12

We assume most users will have SALib installed, as this visualization tool
is intended for use with SALib output.  However, some users may want to
visualize their sensitivity results on a system without SALib, or they may
be reformatting other data to visualize with savvy's tools.  SALib is only
required for the functions in the module ``sensitivity_tools``, which is a
wrapper for generating sensitivity results that are of the appropriate
format for visualizing with savvy.

graph-tool is required to make the network plots in ``network_tools``.  It
can be challenging to install on Windows systems, but is relatively easy to
install in OS X using homebrew (see the "getting-started" page).
