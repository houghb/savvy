High Dimensionality Sensitivity Analysis visualization toolkit (HDSAviz_toolkit_v1.0)
========================================================

**_High Dimensionality Sensitivity Analysis visualization toolkit_** is a modelling and data visualization toolkit that aims to provide interactive visualization capabilities to understand effects of chemical reaction parameters like Tmax, rate constant adjustment factors, carbon, hydrogen and oxygen content etc. on chemical reaction outcomes such as yield, moisture content etc. for a process like lignin pyrolysis.

----------------------
Directory structure
----------------------
The contents of the package are organized in a structure as follows
```
HDSAViz Home (master)
│     convert_bash_script.ipynb
|     Motivation_and_Design.md
|     LICENSE
|     Data_Description.md
|     .gitignore
|     readme.md
|  
|-----HDSAviz folder
|     |   __init__.py
|     |
|     |-----tests subfolder
|     |      |    __init_.py
|     |      |
|     |
|
|-----doc folder
      |
```
---------------------
Software dependencies and license information
----------------------
**All the required software is open source.**
The implementation was done using the following languages and packages.  

Programming language:   
Python version 2.7  
[https://www.python.org/](https://www.python.org/)

Python packages needed:
- numpy
- pandas
- bokeh
- Salib
- matplotlib

__coming soon__  - versions of the packages used.

**Operating system specific information:**

It should be easy to install Python on typical systems such as Mac OS X, Windows and Unix-like operating systems. The required packages are also availabe as simple pip install commands without too many additional dependencies.

**License information:**   

The choice of licence is BSD 2-clause “Simplified” License. The objective behind this choice of licensing is to make the content reproducible and make it useful for as many people as possible. The idea is to maximize the two-way collaborations with minimum restrictions, so that developers of other projects can easily utilize, patch, improve, and cite this code.
For detailed description of the contents of license please refer to [License](https://github.com/houghb/HDSAviz/blob/master/LICENSE)


---------
Folders
---------

**[HDSAviz](https://github.com/houghb/HDSAviz/tree/master/HDSAviz)** - The script running the model and visualization kit will read the input files from this folder.  The folder currently contains only an initialization file __init__.py.      
**_coming soon_** - we will be hosting the setup.py file that can be used for making the package installable on any machine, and necessary data files including example input data that can be used for testing the model after compilation soon in this folder.

**[doc](https://github.com/houghb/HDSAviz/tree/master/doc)** - empty now  
**_coming soon_** - This directory will be used to host the sphinx or shablona/doc template and other necessary documentation files

**[tests](https://github.com/houghb/HDSAviz/tree/master/HDSAviz/tests)** - Currently only contains the __init__.py file.  
**_coming soon_** - We will host the unit tests and necessary files to verify the example output is generated correctly by the model here.  

-------------------
Files
-------------------
1. **[.gitignore](https://github.com/houghb/HDSAviz/blob/master/.gitignore)** :  This file specifies intentionally untracked files that Git should ignore. Files already tracked by Git are not affected

2. **[Data_Description.md](https://github.com/houghb/HDSAviz/blob/master/Data_Description.md)** : Contains details about the sample dataset used for sensitivity analysis using the sofware.

3. **[LICENSE](https://github.com/houghb/HDSAviz/blob/master/LICENSE)** : Contains specific documentation about the license. we are using BST new type of license to encourage collaboration and further development.

4. **[Motivation_and_Design.md](https://github.com/houghb/HDSAviz/blob/master/Motivation_and_Design.md)** : contains information about the specific tasks that can be implemented with the software. It also describes the motivation for writing the code and some sample use cases for the toolkit and sensitivity analysis.

5. **[convert_bash_script.ipynb](https://github.com/houghb/HDSAviz/blob/master/convert_bash_script.ipynb)** : This is an ipython notebook file which cleans and combines the input bash script (**to be included**) and composition list data file (**to be included**) to provide a complete set of the input parameters sampled in the sensitivity analysis.

6. **[README.md](https://github.com/houghb/HDSAviz/blob/master/README.md)** : current file provides overview of the repository and its software,  data, documents and licence information

-------------------
Instructions
-------------------
__coming soon__ - This segment will be used to guide the user on how to setup the software and implement basic setup tasks.
This will also host any reference links which a user might find useful.


-----------------
Data
-----------------
__coming soon__  - This section will give a brief overview of the data sets.
Breifly - We have 34 files in our sample dataset, which is described in detail in [here](https://github.com/houghb/HDSAviz/blob/master/Data_Description.md). These files were generated to complete a global sensitivity analysis of a system of stiff ODE equations that models the pyrolysis of lignin.
