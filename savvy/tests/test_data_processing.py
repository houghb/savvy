import unittest
import os

from pandas.util.testing import assert_frame_equal
try:
    import cPickle as pickle
except:
    import pickle

from ..data_processing import get_sa_data, find_unimportant_params

sample_files_path = os.getcwd().split('savvy')[0] + 'savvy/sample_data_files/'
comparisons = pickle.load(open(sample_files_path+'unittest_comparisons.pkl',
                               'rb'))


class TestGetSAData(unittest.TestCase):
    """Tests for get_sa_data()"""

    def test_returns_expected_dict(self, comps=comparisons,
                                   path=sample_files_path):
        """Does get_sa_data() return the expected dictionaries?"""
        # compare two dataframes with all sensitivity results
        df1 = comps[0]['sample-output1'][0]
        df2 = get_sa_data(path)['sample-output1'][0]
        df3 = comps[0]['sample-output2'][1]
        df4 = get_sa_data(path)['sample-output2'][1]
        # These are df's without second order indices
        df5 = comps[1]['sample-output3-no_second_order'][0]
        df6 = get_sa_data(path + 'without_second_order_indices/')[
            'sample-output3-no_second_order'][0]

        # assert_frame_equal returns None if the two dataframes are the same
        self.assertIsNone(assert_frame_equal(df1, df2),
                          msg='The `sample-output1` dataframes do not match')
        self.assertIsNone(assert_frame_equal(df3, df4),
                          msg='The `sample-output2` dataframes do not match')
        self.assertIsNone(assert_frame_equal(df5, df6),
                          msg='The `sample-output3` dataframes do not match')


class TestFindUnimportantParams(unittest.TestCase):
    """Tests for find_unimpotant_params()"""

    def test_header_error_raised(self):
        """Is an error raised if an inappropriate header is passed?"""
        self.assertRaises(ValueError, find_unimportant_params, 'St',
                          sample_files_path)
        self.assertRaises(ValueError, find_unimportant_params, 8,
                          sample_files_path)

    def test_returns_expected_output(self):
        """Does the function return the expected unimportant parameters?"""
        expected_results = ['k182', 'k202', 'k221', 'k241', 'k315', 'k335',
                            'k344', 'k384', 'k395']
        self.assertEquals(find_unimportant_params('S1', sample_files_path),
                          expected_results)


if __name__ == '__main__':
    unittest.main()
