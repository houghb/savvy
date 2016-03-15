"""Unit tests for make_plot"""

import unittest
import os.path as op

try:
    import cPickle as pickle
except:
    import pickle

import savvy
from ..plotting import make_plot, make_second_order_heatmap

# Load a sample file to use for testing
path = op.join(savvy.__path__[0], 'sample_data_files/')
comparisons = pickle.load(open(path+'unittest_comparisons.pkl',
                               'rb'))
# Dataframe of first/total order sample data
df = comparisons[0]['sample-output1'][0]
# Dataframe of second order indices
df2 = comparisons[0]['sample-output1'][1]


class TestMakePlot(unittest.TestCase):
    """Tests for make_plot()"""

    def test_incorrect_dataframe(self):
        """Check dataframe has incorrect headers"""
        with self.assertRaises(Exception) as context:
            make_plot()
        self.assertTrue('Dataframe not formatted correctly' in
                        context.exception)

    def test_correct_dataframe(self):
        """Check dataframe has correct headers"""
        make_plot(dataframe=df, highlight=[],
                  top=100, minvalues=0.01, stacked=True, lgaxis=True,
                  errorbar=True, showS1=True, showST=True)
        self.assert_(True)

    def test_correct_height(self):
        """Check radial plot height is 800"""
        result = make_plot(dataframe=df, highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(result.plot_height, 800)

    def test_correct_width(self):
        """Check radial plot width is 800"""
        result = make_plot(dataframe=df, highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(result.plot_width, 800)

    def test_correct_number_of_glyphs_radial(self):
        """Check number of glyph renders created (radial plot)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.renderers), 12)

    def test_correct_number_of_tools_radial(self):
        """Check number of tools created (radial plot)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.tools), 5)

    def test_correct_number_of_glyphs_bar(self):
        """Check number of glyph renders created (bar chart)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=5, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.renderers), 15)

    def test_correct_number_of_tools_bar(self):
        """Check number of tools created (bar chart)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=5, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.tools), 7)


class TestMakeSecondOrderHeatmap(unittest.TestCase):
    """Tests for make_second_order_heatmap()"""

    def test_df_contains_second_order_data(self):
        """Is a TypeError raised if make_second_order_heatmap is provided a
        dataframe with incorrect headers?"""
        self.assertRaises(TypeError, make_second_order_heatmap, df)

    def test_default_arguments(self):
        """Does make_second_order_heatmap succeed with default args?"""
        make_second_order_heatmap(df2)
        self.assert_(True)

    def test_top_is_negative(self):
        """Can make_second_order_heatmap handle `top` < 0?"""
        make_second_order_heatmap(df2, top=-10)
        self.assert_(True)

    def test_top_is_zero(self):
        """Can make_second_order_heatmap handle `top` = 0?"""
        make_second_order_heatmap(df2, top=0)
        self.assert_(True)

    def test_top_is_greater_than_num_interactions(self):
        """Can make_second_order_heatmap handle `top` much greater than the
        total number of interactions in the dataframe?"""
        make_second_order_heatmap(df2.head(3), top=10)
        self.assert_(True)

    def test_name_populates_plot_title(self):
        """Does `name` successfully show up in plot title?"""
        plot = make_second_order_heatmap(df2, name='test_name')
        displayed_name = plot.title
        expected_name = 'test_name second order sensitivities'
        self.assertEqual(displayed_name, expected_name)

    def test_include_adds_boxes_to_plot(self):
        """Are entries in `include` added to the plot?"""
        incl = ['Tmax', 'Carbon', 'k199']
        plot = make_second_order_heatmap(df2, top=1, include=incl)
        displayed_params = plot.y_range.factors
        expected_params = ['k81', 'k316', 'Tmax', 'Carbon', 'k199']
        self.assertTrue(set(displayed_params) == set(expected_params))

    def test_correct_width_and_height(self):
        """Are the plotted dimensions correct"""
        plot = make_second_order_heatmap(df2)
        self.assertEqual(plot.plot_height, 700)
        self.assertEqual(plot.plot_width, 700)

    def test_correct_number_of_tools(self):
        """Are the number of tools in the plot correct?"""
        plot = make_second_order_heatmap(df2)
        self.assertEqual(len(plot.tools), 7)

    def test_correct_number_of_renderers(self):
        """Are the number of renderers plotted correct?"""
        plot = make_second_order_heatmap(df2)
        self.assertEqual(len(plot.renderers), 6)


if __name__ == '__main__':
    unittest.main()
