'''Unit tests for make_plot'''

import unittest
from savvy import plotting.make_plot
import pandas as pd
from savvy import data_processing as dp


class TestPlots(unittest.TestCase):

    # Test for primes
    def test_incorrect_dataframe(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=pd.Series(), highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertFalse(result)

    def test_correct_dataframe(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=100, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertTrue(result[1])

    def test_bar_plot(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=1, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertFalse(result[2])

    def test_radial_plot(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.0, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertTrue(result[2])

    def test_bar_plot_min(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=2, minvalues=0.01, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertTrue(result[3])

    def test_radial_plot_min(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertTrue(result[3])

    def test_S1_plotted(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertTrue(result[4])

    def test_S1_not_plotted(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=True, showS1=False, showST=True)
        self.assertFalse(result[4])

    def test_ST_plotted(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=True)
        self.assertTrue(result[5])

    def test_ST_not_plotted(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=False)
        self.assertFalse(result[5])

    def test_data_on_axis(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=False)
        self.assertTrue(result[6])

    def test_show_error_bars(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=True, showS1=True, showST=False)
        self.assertTrue(result[7])

    def test_no_error_bars(self):
        sa_dict = dp.get_sa_data()
        result = make_plot(dataframe=sa_dict['totaltars'][0], highlight=[],
                           top=10, minvalues=0.001, stacked=True, lgaxis=True,
                           errorbar=False, showS1=True, showST=False)
        self.assertFalse(result[7])

if __name__ == '__main__':
    unittest.main()
