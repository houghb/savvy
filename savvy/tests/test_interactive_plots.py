import data_processing as dp
from collections import OrderedDict
import numpy as np
import pandas as pd

import os
import sys
import interactive_plots as ip
from nose.tools import assert_equal, assert_in
import matplotlib
from matplotlib.testing.decorators import image_comparison
from plotting import make_plot, make_second_order_heatmap
from bokeh.plotting import figure, show, output_notebook, output_file

output_notebook()

sa_dict = dp.get_sa_data()

@image_comparison(baseline_images=['daily_totals'],
                  extensions=['png'])
def test_plot_daily_totals():
    """
    tests that the plot matches exactly with following instructions

    data = get_trips_and_weather()
    fig, ax = plt.subplots(2, figsize=(14, 6), sharex=True)
    data['Annual Member'].plot(ax=ax[0], title='Annual Member')
    data['Short-Term Pass Holder'].plot(
                ax=ax[1], title='Short-Term Pass Holder')

    """
    ip.interact_with_make_plot(sa_dict, demo = True)

if __name__ == "__main__":
    import nose
    nose.runmodule(argv=['-s', '--with-doctest'], exit=False)