""" Functions for setting up and carrying out a Sobol sensitivity analysis
on your model."""

from subprocess import call

from SALib.sample import saltelli


def gen_params(num_vars, names, bounds, n, second=True):
    """
    Generate the parameter sets for the Sobol sensitivity analysis.
    Saves a file with the information required for the analysis
    that will be performed later.

    Parameters:
    -----------
    num_vars : an integer number of parameters you will vary
    names    : a list of strings with the names of the paramters
    bounds   : a list of lists, where each inner list contains the
               upper and lower bounds for a given parameter.
    n        : an integer number of initial samples to generate from
               the pseudo-random Sobol sequence. n parameter sets
               will be generated using the Sobol sequence, then the
               Saltelli cross-sampling method will be applied to give a
               total of 2n(p+1) parameter sets to be run if second = True.
    second   : a boolean to indicate whether or not to calculate second
               order sensitivity indices.  If False, only 1st and total
               order indices will be calculated and n(p+2) parameter sets
               will be generated.

    Returns:
    --------
    param_sets : a numpy ndarray where each row is one set of parameter
                 values.  You must run your model (in whatever environment
                 is appropriate) with each of the sets of parameters from
                 this array.  The output must be stored in the same order
                 as given in this parameter set array (one row of results
                 for each row of parameters).
    """
    problem = {'num_vars': num_vars, 'names': names, 'bounds': bounds}
    param_sets = saltelli.sample(problem, n, calc_second_order=second)

    if second:
        print '%s simulations will be run' % (2*n * (problem['num_vars'] + 1))
    elif second is False:
        print '%s simulations will be run' % (n * (problem['num_vars'] + 2))

    # Write the problem description to a file (required to run the analysis
    # afer your model has been run with all the generated parameter sets)
    body = ''
    for i, name in enumerate(problem['names']):
        body += '%s %s %s\n' % (name, problem['bounds'][i][0],
                                problem['bounds'][i][1])
    with open('../../saparams_%s-parameters_%s-n.txt'
              % (num_vars, n), 'wb') as params:
        params.write(body)

    return param_sets


def analyze_sensitivity(problem, Y, column, delimiter, order, name,
                        parallel=False, processors=4):
    """
    Perform the sensitivity analysis after you have run your model
    with all the parameters from gen_params().  This is done from
    the command line because is is faster and gives the option to
    specify the column of the results file to analyze.  Parallel
    processing is possible.  Results are saved to a file using the
    name parameter.

    Parameters:
    ----------
    problem    : string with the path to the saparams* file that contains
                 the problem definition.
    Y          : string with the path to the results file.  Results should
                 be in a file without a header.  Each line of the file must
                 contain results that correspond to the same line of the
                 param_sets generated in gen_params()
    column     : integer specifying the column number of the results to analyze
    delimiter  : string specifying the column delimiter used in the results
    order      : int; the maximum order of sensitivity indices [1 or 2]
    name       : string with the name of the output measure to use when saving
                 the sensitivity analysis results to a file.
    parallel   : boolean indicating whether to use parallel processing
    processors : if parallel is True, this is an integer specifying the number
                 of processors to use.

    Returns:
    --------
    None
    """

    if parallel:
        call('python -m SALib.analyze.sobol -p %s -Y %s'
             '-c %s --delimiter=%s --max-order=%s --parallel --processors=%s'
             '> analysis_%s.txt' %
             (problem, Y, column, delimiter, order, processors, name),
             shell=True)
    else:
        call('python -m SALib.analyze.sobol -p %s -Y %s'
             '-c %s --delimiter=%s --max-order=%s > analysis_%s.txt' %
             (problem, Y, column, delimiter, order, name), shell=True)
