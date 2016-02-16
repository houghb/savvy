We have 34 files in our dataset, described below.  These files were generated to complete a global sensitivity analysis of a system of stiff ODE equations that models the pyrolysis of lignin.

# input_parameters.csv
-  4.74GB
-  824,000 x 412 matrix
-  Each row in this CSV file contains 412 parameters necessary to run one simulation of the lignin pyrolysis model.  Entries are as follows:
    -  End time [s], Tmax [K], h [c/min], Carbon [mole fraction], Hydrogen [mole fraction], Oxygen [mole fraction], followed by 406 rate constant adjustment factors for all the reactions in the model
-  There is no header in the file.  Each entry is separated by a comma. 

# results.txt
-  385.9MB
-  824,000 x 32 matrix
-  Each row in this file contains 32 output measures of interest from the lignin pyrolysis model.  These are the final values for the given measures at the end of the pyrolysis reaction.  Entries are as follows in this order:
    - mass fraction of: solids lighttars heavytars totaltars CO CO2 othergases totalgases H20 
    - H-C-ratio
    - Moisture content of tar (wt%) 
    - distribution of functional groups (% of carbon) from: tot_C--O tot_aromaticC-O tot_aromaticC-C tot_aromaticC-H tot_aliphaticC-O tot_aromatic methoxyl tot_aliphaticC-C heavy_C--O heavy_aromatic_C-O heavy_aromatic_C-C heavy_aromatic_C-H heavy_aliphatic_C-O heavy_aromatic_methoxyl heavy_aliphatic_C-C light_C--O light_aromatic_C-O light_aromatic_C-C light_aromatic_C-H light_aliphatic_C-O light_aromatic_methoxyl light_aliphatic_C-C 
-  There is no header in the file.  Each entry is separated by a space.

# analysis_*.txt
-  There are 32 of these files
-  Each file is about 18KB
-  Each is a 411 x 5 matrix
-  These files are the results of the sobol sensitivity analysis.  Each row contains:
    -  Parameter name, 1st order sensitivity index, 1st order index confidence interval, total sensitivity index, total index confidence interval
-  There is a header with column names.  Entries are separated by a space.



It is trivial to create a subset of all these three data sources for unit tests.  Individual rows from the input_parameters and results files would make good test cases for unit tests.  Likewise, we could either use individual rows from particular analysis* files, or use a single analysis* file for unit tests of the appropriate components.
