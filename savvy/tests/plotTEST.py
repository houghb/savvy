'''Unit tests for make_plot'''

import unittest
from plotting import make_plot
import pandas as pd
import data_processing as dp


class TestPlots(unittest.TestCase):

    def test_incorrect_dataframe(self):
        """Check dataframe has incorrect headers"""
        sa_dict = dp.get_sa_data()
        with self.assertRaises(Exception) as context:
            make_plot()
        self.assertTrue('Dataframe not formatted correctly' in
                        context.exception)

    def test_correct_dataframe(self):
        """Check dataframe has correct headers"""
        sa_dict = dp.get_sa_data()
        make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                  top=100, minvalues=0.01, stacked=True, lgaxis=True,
                  errorbar=True, showS1=True, showST=True)
        self.assert_(True)

    def test_correct_height(self):
        """Check radial plot height is 800"""
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(result.properties_with_values()['plot_height'], 800)

    def test_correct_width(self):
        """Check radial plot width is 800"""
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(result.properties_with_values()['plot_width'], 800)

    def test_correct_number_of_glyphs_radial(self):
        """Check number of glyph renders created (radial plot)"""
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['renderers']), 12)

    def test_correct_number_of_tools_radial(self):
        """Check number of tools created (radial plot)"""
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['tools']), 5)

    def test_correct_number_of_glyphs_bar(self):
        """Check number of glyph renders created (bar chart)"""
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=5, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['renderers']), 15)

    def test_correct_number_of_tools_bar(self):
        """Check number of tools created (bar chart)"""
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=5, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertEqual(len(result.properties_with_values()['tools']), 7)

if __name__ == '__main__':
    unittest.main()
