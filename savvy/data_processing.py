"""
Tools for reading and processing the sensitivity analysis data files.
Some of the files are specific to our project (`input_parameters.csv' and
`results.csv`), but the results of sensitivity analyses are formatted
as any SALib analysis results will be from a sobol analysis.

Our data files are stored outside this repository because they are too large,
so users need to specify the path to their data.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os

import pandas as pd


def _map_pretty_names(df, column_names, pretty_names):
    for name in column_names:
        df[name] = df[name].map(pretty_names).fillna(df[name])
    return df 


def format_salib_output(salib_output, run_name, pretty_names=None):
    """
    Function reads the output of SALib.analyze and returns a dictionary that savvy expects.

    Parameters
    ----------
    path      : dict
                salib analyze output

    run_name  : str, 
                the name of the simulation
                
    pretty_names: dict, optional
                a dictionary mapping old names to new names

    Returns   : dict
    """
    df_list = salib_output.to_df()

    # combine S1 and ST
    df_list[0] = pd.concat((df_list[0], df_list[1]), axis=1)
    df_list.pop(1)

    # Make the Parameter Column
    # for i, _ in enumerate(df_list):
    df_list[0]['Parameter'] = df_list[0].index
    if pretty_names:
        df_list[0] = _map_pretty_names(df_list[0], ['Parameter'], pretty_names)
    df_list[0].reset_index(inplace=True, drop=True)

    # split up the parameters from S2
    df_list[-1][['Parameter_1', 'Parameter_2']] = df_list[-1].index.to_series().apply(pd.Series)
    df_list[-1].reset_index(inplace=True, drop=True)
    if pretty_names:
        df_list[-1] = _map_pretty_names(df_list[-1], ['Parameter_1', 'Parameter_2'], pretty_names)

    return {run_name: df_list}




def read_file(path, numrows=None, drop=False, sep=','):
    """
    Function reads a file of input parameters or model results
    and returns a pandas dataframe with its contents.
    The first line of the input should contain headers
    corresponding to the column names.

    Parameters
    ----------
    path      : str
                the complete filename, including
                absolute or relative path.
    numrows   : int, optional
                number of rows of the file to read.
                If you don't specify this parameter all rows
                will be read.
    drop      : list, optional
                list of strings indicating which (if any)
                of the named columns you do not want to include
                in the resulting dataframe. (ex. ['cats', 'dogs'],
                default is not to drop any rows).
    sep       : str
                string indicating the column separator in the
                file (optional, default = ',').

    Returns
    --------
    df : pandas dataframe
         A pandas dataframe with the contents of the file,
         limited to the number of rows specified and without the
         columns named in "drop".
    """

    df = pd.read_csv(path, sep=sep, nrows=numrows)
    if not drop:
        df.drop(drop, axis=1, inplace=True)

    return df


def get_params(path='./input_parameters.csv',
               numrows=None, drop=['End_time', 'Oxygen']):
    """
    NOTE: This function is specific to our lignin modeling dataset
          and is not needed for the visualization features of savvy

    Returns a pandas dataframe with all the parameters analyzed in
    the sensitivity analysis, but not additional parameters like
    end time and oxygen content.  If you would like all of the
    parameters (even those not analyzed for sensitivity) then pass
    drop=False.

    Parameters
    ----------
    path    : str, optional
              string containing the path to the parameters csv.
    numrows : int, optional
              the number of rows of the input_parameters file to read
              (default is to read all rows).
    drop    : list, optional
              a list of strings for which parameters you do not want to
              include in the returned dataframe.  If you want all params
              then pass drop=False.

    Returns
    -------
    pandas dataframe

    """

    return read_file(path, numrows=numrows, drop=drop)


def get_results(path='./results.csv',
                numrows=None, drop=['light_aromatic_C-C',
                                    'light_aromatic_methoxyl']):
    """
    NOTE: This function is specific to our lignin modeling dataset
          and is not needed for the visualization features of savvy

    Returns a pandas dataframe with the results of running all of the
    simulations for the parameters sets in `input_parameters.csv`. This
    function drops two unused functional groups from the results file.

    Parameters
    ----------
    path    : str, optional
              the path to the results csv file.
    numrows : int, optional
              the number of rows of the input_parameters file to read
              (default is to read all rows).
    drop    : list, optional
              a list of strings for which output measures to drop from
              the returned dataframe.  If you want all outputs use
              drop=False.

    Returns
    -------
    pandas dataframe
    """

    return read_file(path, numrows=numrows, drop=drop)


def get_sa_data(path='.'):
    """
    This function reads and processes all the sensitivity analysis results
    in a specified folder and returns a dictionary with the corresponding
    dataframes for first/total order sensitivity indices and second order
    indices (if present).

    Sensitivity analysis results should be in the default SALib output
    format and must start with the word 'analysis'.

    NOTE: there are two lines of code at the beginning of this function
    (the filenames.remove lines) that are specific to our lignin modeling
    dataset.  Future users can remove or modify these lines to use
    with other datasets.

    Parameters
    -----------
    path : str, optional
           String containing the relative or absolute path of the directory
           where analysis_*.txt files are stored.  There cannot be any
           files or folders within this directory that start with 'analysis'
           except those generated by the SALib sensitivity analysis.  All
           `analysis*` files in this path should correspond to outputs from
           one sensitivity analysis project, and if second order sensitivity
           indices are included in any of the files they should be present in
           all the others.

    Returns
    --------
    sens_dfs : dict
               Dictionary where keys are the names of the various output
               measures (one output measure per analysis file in the folder
               specified by path).  Dictionary values are a list of pandas
               dataframes.

               sens_dfs['key'][0] is a dataframe with the first and total
               order indices of all the parameters with respect to the "key"
               output variable.

               sens_dfs['key'][1] is a dataframe with the second order
               indices for pairs of parameters (if second order indices are
               present in the analysis file).  If there are no second order
               results in the analysis file then this value is a boolean,
               False.
    """

    filenames = [filename for filename in os.listdir(
                 path) if filename.startswith('analysis')]

    # These two functional groups are not present in the light oil fraction
    if 'analysis_light_aromatic-C-C.txt' in filenames:
        filenames.remove('analysis_light_aromatic-C-C.txt')
    if 'analysis_light_aromatic-methoxyl.txt' in filenames:
        filenames.remove('analysis_light_aromatic-methoxyl.txt')

    # Make a dictionary where keys are the different output measures
    # (one for each analysis file) and values are lists of dataframes
    # with the first/total analysis results, and the second order results.
    sens_dfs = {}
    for filename in filenames:
        name = filename[9:].replace('.txt', '')

        with open(path + filename) as result:
            contents = []
            contents.append(result.readlines())
            # find the line number in the file where 2nd order results appear
            for j, line in enumerate(contents[0]):
                # End this loop when you reach the line that separates
                # the first/total indices from the second order indices
                if line.startswith('\n'):
                    break
                # If no second order indices in file
                else:
                    j = False
            # If there are second order indices in the file
            if j:
                sens_dfs[name] = [pd.read_csv(path + filename, sep=' ',
                                              nrows=(j - 1)),
                                  pd.read_csv(path + filename, sep=' ',
                                              skiprows=j)
                                  ]
            else:
                sens_dfs[name] = [pd.read_csv(path + filename, sep=' '),
                                  False]

        # Deal with negative values.  All negative values appear to be close
        # to zero already; they are the result of machine precision issues or
        # setting n too low when generating parameter sets.  To properly
        # correct this issue you should re-run your model with n greater,
        # but sometimes that is too expensive so this is a hack to allow
        # display of them in a logical way.
        # .
        # adjust confidence interval to account for shifting sensitivity value
        sens_dfs[name][0].loc[sens_dfs[name][0]['S1'] < 0, 'S1_conf'] = (
            sens_dfs[name][0]['S1_conf'] + sens_dfs[name][0]['S1'] - 0.0001)
        # set the new sensitivity value = 0.0001
        sens_dfs[name][0].loc[sens_dfs[name][0]['S1'] < 0, 'S1'] = 0.0001
        # do the same for total and second order indices
        sens_dfs[name][0].loc[sens_dfs[name][0]['ST'] < 0, 'ST_conf'] = (
            sens_dfs[name][0]['ST_conf'] + sens_dfs[name][0]['ST'] - 0.0001)
        sens_dfs[name][0].loc[sens_dfs[name][0]['ST'] < 0, 'ST'] = 0.0001
        if isinstance(sens_dfs[name][1], pd.DataFrame):
            sens_dfs[name][1].loc[sens_dfs[name][1]['S2'] < 0, 'S2_conf'] = (
                sens_dfs[name][1]['S2_conf'] + sens_dfs[name][1]['S2'] -
                0.0001)
            sens_dfs[name][1].loc[sens_dfs[name][1]['S2'] < 0, 'S2'] = 0.0001

        # Change 'rxn' to 'k' for consistency with inputs file
        sens_dfs[name][0].Parameter = (sens_dfs[name][0].Parameter
                                       .str.replace('rxn', 'k', case=False))

    return sens_dfs


def find_unimportant_params(header='ST', path='.'):
    """
    This function finds which parameters have sensitivities and confidence
    intervals equal to exactly 0.0, which means those parameters have no
    role in influencing the output variance for any of the calculated output
    measures.

    These parameters could be considered for removal from the model
    (although it is possible they might play a role in other, unsaved
    outputs)

    Parameters
    -----------
    header : str, optional
             string of the column header for the sensitivity index you choose.
    path   : str, optional
             string with the path to the folder where your analysis files
             are located.

    Returns
    --------
    unimportant : list
                  a list of the parameters that don't matter for these outputs.
    """

    if header not in set(['ST', 'S1']):
        raise ValueError('header must be ST or S1')

    zero_params = []
    sa_dict = get_sa_data(path)
    for key in sa_dict.keys():
        df = sa_dict[key][0]
        zero_params.append(df[(df[header] == 0.0) &
                              (df['%s_conf' % header] == 0.0)]
                           .loc[:, 'Parameter'].values.tolist())

    result = set(zero_params[0])
    for s in zero_params[1:]:
        result.intersection_update(s)
    unimportant = list(result)
    unimportant.sort()

    print('The following %s parameters have %s==0 for all outputs:\n' % \
          (len(unimportant), header), unimportant, '\n')
    return unimportant


# THIS IS A FUNCTION THAT MIGHT BE USEFUL IN THE FUTURE
# BUT I HAVEN'T WRITTEN YET.
# def combine_sens(order):
#     """
#     STILL WORKING ON WRITING THIS FUNCTION
#
#     This function creates a pandas dataframe that has all the sensitivity
#     indices and confidence values of a specified order (first, total) from
#     every output measure.
#
#     The output of this function can be used to plot the sensitivity indices
#     of all of the output measures for a given input parameter.
#
#     Parameters
#     -----------
#     order : String indicating which order indices to combine (first, total)
#
#     Returns
#     --------
#
#     """
