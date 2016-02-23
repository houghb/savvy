# Overall Aim:
## To come up with a visualization toolkit based on sensitivity data for lignin pyrolysis process which can be generalized to other processes and integrated as add-on to SALIB package + do some correlation and causality analysis if time permits.

## Progress this period:
- Raw Data gathering and initial data cleaning has been completed using [SALIB](http://salib.github.io/SALib/) library.
- Everyone's on page with the scope of project and understands the dataset and sources of it.
- Basic outline of an interactive data visualization system has been chalked out.
- Identified packages like [BOKEH](http://bokeh.pydata.org/en/latest/) for visualization and [SALIB](http://salib.github.io/SALib/)  
for sensitivity analysis.
- Tried pandas correlation and heat maps based visuals

# Current status
- We are now working on creation of small test subsets, and exploring 3-5 visualizations like
[burtins in bokeh](http://bokeh.pydata.org/en/latest/docs/gallery/burtin.html) or [parallel coordinates](http://homes.cs.washington.edu/~jheer//files/zoo/ex/stats/parallel.html)
 using BOKEH package to showcase the high dimensional data in interactive ways for a small subset of data.
- Try to showcase a working demo by next Monday.

# How it compares with the plan
- The plan is still developing but we seem to be on track for this weeks deliverables on visualizing a small set using burtin's antibiotics type graph.

# If behind plan, how compensate to make plan end date
- We will skip correlation analysis if we are running behind and focus on 2-3 good, interactive and highly intuitive visualizations instead of 4-5.

# Challenges to making next deliverables such as:
## Technology uncertainties and blockers
- Need to learn using BOKEH package while also learning necessary aspects of Javascript language.

## Team issues
- Still figuring out if we want to go for correlation type analysis or other statistical methods or just stay with visualization of current data.
- Need to identify together some more intuitive ways for good visualizations.
