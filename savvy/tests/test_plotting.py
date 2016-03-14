'''Unit tests for make_plot'''

import unittest

import pandas as pd
import os
import pdb
try:
    import cPickle as pickle
except:
    import pickle

from ..plotting import make_plot

sample_files_path = os.getcwd().split('savvy')[0] + 'savvy/sample_data_files/'
comparisons = pickle.load(open(sample_files_path+'unittest_comparisons.pkl',
                               'rb'))
# Dataframe of sample data
df = comparisons[0]['sample-output1'][0]


class TestPlots(unittest.TestCase):

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
        self.assertEqual(result.properties_with_values()['plot_height'], 800)

    def test_correct_width(self):
        """Check radial plot width is 800"""
        result = make_plot(dataframe=df, highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(result.properties_with_values()['plot_width'], 800)

    def test_correct_number_of_glyphs_radial(self):
        """Check number of glyph renders created (radial plot)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['renderers']), 12)

    def test_correct_number_of_tools_radial(self):
        """Check number of tools created (radial plot)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['tools']), 5)

    def test_correct_number_of_glyphs_bar(self):
        """Check number of glyph renders created (bar chart)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=5, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['renderers']), 15)

    def test_correct_number_of_tools_bar(self):
        """Check number of tools created (bar chart)"""
        result = make_plot(dataframe=df, highlight=[],
                           top=5, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['tools']), 7)

if __name__ == '__main__':
    unittest.main()
