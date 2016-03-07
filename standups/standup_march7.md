## — Progress this week —
- Generated and processed additional data so we can explore how our tool deals with larger datasets
- Created plotting functions to show the second order sensitivity indices in bokeh and graph tool
- Improved the visual appeal of 1st and total order plot (label placement, colors, etc)
- Added error bars to show confidence interval data
- Added condition to create a histogram instead of normal plot if the data set shrinks to a small subset (the original plot looked awkward with only a few bars).
 ### - How it compares to the plan -
 - Still need to merge the interactive components into the rest of the code. Otherwise on schedule

 ### - How to get back on schedule
 - Meet this week to address conflicts between branches and get everything compiled

## — Deliverables next week —
- Determine which interactive widgets/tools we want to add for each plot and integrate them
- Write unit tests for each aspect of our package
- Write documentation
- Travis testing
- Finish project and complete poster


## —Challenges —
### Team issues
- Still have un-merged branch. As before, branch relies on functions from other branches and changes to those over functions over time has led to conflicts.

### Technology uncertainties.
- Some of the Bokeh tools require the use of Java Script for customization which is tough to fully learn and execute in such a short timespan. There are not a lot of examples provided and the documentation doesn't typically include JS.

- Writing meaningful unit tests for interactive components

- The newer, larger data set poses some potential issues with regards to the speed of generating certain plots (each of the 30 new analysis files is about 85,000 lines x 4 columns).  Processing information from pandas dataframes with this data is a little slow and using ipywidgets for tools (Bokeh tools may be faster).
