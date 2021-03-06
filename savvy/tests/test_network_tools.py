import unittest
import os.path as op

try:
    import cPickle as pickle
except:
    import pickle

import savvy
from ..network_tools import (build_graph, plot_network_random,
                             plot_network_circle)

# Load a sample file to use for testing
path = op.join(savvy.__path__[0], 'sample_data_files/')
comps = pickle.load(open(path+'unittest_comparisons.pkl', 'rb'))


class TestBuildGraph(unittest.TestCase):
    """Tests for build_graph() function"""

    def test_for_acceptable_sens_arg(self):
        """Is an exception raised if sens is an inappropriate value?"""
        df_list = comps[0]['sample-output1']
        self.assertRaises(ValueError, build_graph, df_list, 'tot', 10,
                          0.01, 0.0)
        self.assertRaises(ValueError, build_graph, df_list, 1, 10,
                          0.01, 0.0)

    def test_for_second_order_df(self):
        """Is an exception raised if there is not a second order dataframe?"""
        df_list = comps[1]['sample-output3-no_second_order']
        self.assertRaises(Exception, build_graph, df_list, 'ST', 10,
                          0.01, 0.0)

    def test_for_correct_num_vertices(self):
        """Does the graph object produced by build_graph have the correct
        number of vertices?"""
        df_list = comps[0]['sample-output2']
        g = build_graph(df_list, 'ST', 30, 0.01, 0.0)
        expected_vertices = 27
        self.assertEqual(expected_vertices, g.num_vertices(),
                         msg='num_vertices does not match expected')

    def test_for_correct_num_edges(self):
        """Does the graph object produced by build_graph have the correct
        number of edges?"""
        df_list = comps[0]['sample-output2']
        g = build_graph(df_list, 'ST', 30, 0.01, 0.0)
        expected_edges = 351
        self.assertEqual(expected_edges, g.num_edges(),
                         msg='num_edges does not match expected')


# Both of the plot* functions return None, so there is no object to perform
# comparisons on except for a saved figure of what was plotted. Since
# the plots can appear different when run on different systems, we could
# not think of a robust way to unittest them that would not constantly lead
# to failed tests for different users.  We leave it up to the user to notice
# if the plotting functions have problems, and rely on the unittest for
# build_graph to catch problems with new versions of graph-tool.

if __name__ == '__main__':
    unittest.main()
