import unittest
import os
import numpy as np

from ..sensitivity_tools import gen_params

cwd = os.getcwd()


class TestGenParams(unittest.TestCase):
    """Tests for gen_params"""

    def test_num_vars_not_integer(self):
        """Is an error raised if num_vars is not an integer?"""
        names = ['para1', 'para2', 'para3']
        bounds = [[0, 1], [2, 6], [0, 2.3]]
        self.assertRaises(TypeError, gen_params, 9.6, names, bounds, 10,
                          cwd, True)
        self.assertRaises(TypeError, gen_params, '10', names, bounds, 10,
                          cwd, True)

    def test_missing_bounds(self):
        """Is an error raised when there are different numbers
        of bounds than num_vars?"""
        names = ['para1', 'para2', 'para3']
        bounds = [[0, 1], [2, 6], [0, 2.3]]
        self.assertRaises(ValueError, gen_params, 5, names, bounds, 10,
                          cwd, True)

    def test_names_exist_for_all_params(self):
        """Is an error raised if the length of names != num_vars"""
        names = ['para1', 'para2', 'para3']
        bounds = [[0, 1], [2, 6], [0, 2.3], [0, 1], [0, 2]]
        self.assertRaises(ValueError, gen_params, 5, names, bounds, 10,
                          cwd, True)

    def test_gen_params_gives_expected_sets(self):
        """Does gen_params return the expected parameter sets?"""
        names = ['para1', 'para2', 'para3']
        bounds = [[0, 1], [2, 6], [0, 2.3]]
        expectedt = np.array([[0.21972656,  2.38671875,  1.19267578],
                              [0.67675781,  2.38671875,  1.19267578],
                              [0.21972656,  3.12109375,  1.19267578],
                              [0.21972656,  2.38671875,  2.08662109],
                              [0.21972656,  3.12109375,  2.08662109],
                              [0.67675781,  2.38671875,  2.08662109],
                              [0.67675781,  3.12109375,  1.19267578],
                              [0.67675781,  3.12109375,  2.08662109]])
        expectedf = np.array([[0.21972656,  2.38671875,  1.19267578],
                              [0.67675781,  2.38671875,  1.19267578],
                              [0.21972656,  3.12109375,  1.19267578],
                              [0.21972656,  2.38671875,  2.08662109],
                              [0.67675781,  3.12109375,  2.08662109]])
        self.assertEqual(gen_params(3, names, bounds, 1, cwd, False).all(),
                         expectedf.all())
        self.assertEqual(gen_params(3, names, bounds, 1, cwd, True).all(),
                         expectedt.all())

    def tearDown(self):
        [os.remove(cwd+'/'+name) for name in os.listdir(cwd)
         if name.startswith('saparams')]

# the function `analyze_sensitivity` is not being tested because this
# function does not do anything that has not already been tested in SALib
# (`analyze_sensitivity` just formats the bash command that runs the analysis)

if __name__ == '__main__':
    unittest.main()
