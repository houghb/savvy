"""
This module contains functions to create and display network graphs of the
sensitivity analysis results.  It is included as an independent module in
this package because graph-tools is an uncommon package that is slightly
more involved to install than normal conda- or pip-accessible packages.  All
the other visualization functionality of savvy is accessible with the more
readily available bokeh plots.

The plots generated in this module offer a good visualization of which
parameters have the highest sensitivities, and which are connected by
second order interactions.  Relative sizes of vertices on these plots are not
very good representations of the actual difference in magnitude between
sensitivities (a value of 0.02 appears similar to a value of 0.2).  The bokeh
visualizations offer better insight into these relative magnitudes.
"""

try:
    import graph_tool.all as gt
    from graph_tool import Graph, draw
    from graph_tool.all import minimize_nested_blockmodel_dl
except ImportError:
    print ('----\ngraph-tool package is not installed - please install it to '
           'use network_tools!\nOther modules in savvy are independent'
           'of graph-tool.')


def build_graph(df_list, sens='ST', top=410, min_sens=0.01,
                edge_cutoff=0.0):
    """
    Initializes and constructs a graph where vertices are the parameters
    selected from the first dataframe in 'df_list', subject to the
    constraints set by 'sens', 'top', and 'min_sens'.  Edges are the second
    order sensitivities of the interactions between those vertices,
    with sensitivities greater than 'edge_cutoff'.

    Parameters
    -----------
    df_list     : list
                  A list of two dataframes.  The first dataframe should be
                  the first/total order sensitivities collected by the
                  function data_processing.get_sa_data().
    sens        : str, optional
                  A string with the name of the sensitivity that you would
                  like to use for the vertices ('ST' or 'S1').
    top         : int, optional
                  An integer specifying the number of vertices to display (
                  the top sensitivity values).
    min_sens    : float, optional
                  A float with the minimum sensitivity to allow in the graph.
    edge_cutoff : float, optional
                  A float specifying the minimum second order sensitivity to
                  show as an edge in the graph.

    Returns
    --------
    g : graph-tool object
        a graph-tool graph object of the network described above.  Each
        vertex has properties 'param', 'sensitivity', and 'confidence'
        corresponding to the name of the parameter, value of the sensitivity
        index, and it's confidence interval.  The only edge property is
        'second_sens', the second order sensitivity index for the
        interaction between the two vertices it connects.
    """

    # get the first/total index dataframe and second order dataframe
    df = df_list[0]
    df2 = df_list[1]

    # Make sure sens is ST or S1
    if sens not in set(['ST', 'S1']):
        raise ValueError('sens must be ST or S1')
    # Make sure that there is a second order index dataframe
    try:
        if not df2:
            raise Exception('Missing second order dataframe!')
    except:
        pass

    # slice the dataframes so the resulting graph will only include the top
    # 'top' values of 'sens' greater than 'min_sens'.
    df = df.sort_values(sens, ascending=False)
    df = df.loc[df[sens] > min_sens, :].head(top)
    df = df.reset_index()

    # initialize a graph
    g = Graph()

    vprop_sens = g.new_vertex_property('double')
    vprop_conf = g.new_vertex_property('double')
    vprop_name = g.new_vertex_property('string')
    eprop_sens = g.new_edge_property('double')

    g.vertex_properties['param'] = vprop_name
    g.vertex_properties['sensitivity'] = vprop_sens
    g.vertex_properties['confidence'] = vprop_conf
    g.edge_properties['second_sens'] = eprop_sens

    # keep a list of all the vertices
    v_list = []

    # Add the vertices to the graph
    for i, param in enumerate(df['Parameter']):
        v = g.add_vertex()
        vprop_sens[v] = df.loc[i, sens]
        vprop_conf[v] = 1 + df.loc[i, '%s_conf' % sens] / df.loc[i, sens]
        vprop_name[v] = param
        v_list.append(v)

    # Make two new columns in second order dataframe that point to the vertices
    # connected on each row.
    df2['vertex1'] = -999
    df2['vertex2'] = -999
    for vertex in v_list:
        param = g.vp.param[vertex]
        df2.loc[df2['Parameter_1'] == param, 'vertex1'] = vertex
        df2.loc[df2['Parameter_2'] == param, 'vertex2'] = vertex

    # Only allow edges for vertices that we've defined
    df_edges = df2[(df2['vertex1'] != -999) & (df2['vertex2'] != -999)]
    # eliminate edges below a certain cutoff value
    pruned = df_edges[df_edges['S2'] > edge_cutoff]
    pruned.reset_index(inplace=True)
    # Add the edges for the graph
    for i, sensitivity in enumerate(pruned['S2']):
        v1 = pruned.loc[i, 'vertex1']
        v2 = pruned.loc[i, 'vertex2']
        e = g.add_edge(v1, v2)
        # multiply by a number to make the lines visible on the plot
        eprop_sens[e] = sensitivity * 150

    # These are ways you can reference properties of vertices or edges
    # g.vp.param[g.vertex(77)]
    # g.vp.param[v_list[0]]

    print ('Created a graph with %s vertices and %s edges.\nVertices are the '
           'top %s %s values greater than %s.\nOnly S2 values (edges) '
           'greater than %s are included.' %
           (g.num_vertices(), g.num_edges(), top, sens, min_sens, edge_cutoff))

    return g


def plot_network_random(g, inline=True, filename=None, scale=300.0):
    """
    Display a plot of the network, g, with the vertices placed in an
    unstructured, apparently random layout.  Vertices are the model
    parameters and they are connected by edges whose thickness indicates the
    value of the second order sensitivity.

    Parameters
    -----------
    g        : graph-tool graph
               The graph to plot.
    inline   : bool, optional
               Boolean indicating whether the plot should be shown inline in
               an ipython notebook.  If false the plot is created in its own
               window and is somewhat interactive.
    filename : str, optional
               If you would like to save the plot to a file specify a
               filename (with an extension of pdf or png).
    scale    : float, optional
               If you would like to resize the vertices you can change the
               value of this float.

    Returns
    --------
    graph-tool plot
    """
    for i in range(g.num_vertices()):
        g.vp['sensitivity'][i] = scale * g.vp['sensitivity'][i]

    draw.graph_draw(g,
                    vertex_text=g.vp['param'],
                    vertex_font_size=10,
                    vertex_text_position=-0.1,
                    # vertex_text_color='black',
                    vertex_size=g.vp['sensitivity'],
                    vertex_color='#006600',
                    vertex_fill_color='#006600',
                    vertex_halo=True,
                    vertex_halo_color='#b3c6ff',
                    vertex_halo_size=g.vp['confidence'],
                    edge_color='#002699',
                    edge_pen_width=g.ep['second_sens'],
                    output_size=(600, 600),
                    inline=inline,
                    output=filename
                    )


def plot_network_circle(g, inline=True, filename=None, scale=300.0):
    """
    Display a plot of the network, g, with the vertices placed around the
    edge of a circle.  Vertices are the model parameters and they are
    connected by edges whose thickness indicates the value of the second
    order sensitivity.

    Parameters
    -----------
    g        : graph-tool graph
               The graph to plot.
    inline   : bool, optional
               Boolean indicating whether the plot should be shown inline in
               an ipython notebook.  If false the plot is created in its own
               window and is somewhat interactive.
    filename : str, optional
               If you would like to save the plot to a file specify a
               filename (with an extension of pdf or png).
    scale    : float, optional
               If you would like to resize the vertices you can change the
               value of this float.

    Returns
    --------
    graph-tool plot
    """

    for i in range(g.num_vertices()):
        g.vp['sensitivity'][i] = scale * g.vp['sensitivity'][i]

    state = minimize_nested_blockmodel_dl(g, )  # deg_corr=True)
    gt.draw_hierarchy(state,
                        vertex_text=g.vp['param'],
                        vertex_text_position=-0.1,
                        # vertex_text_color='black',
                        vertex_font_size=10,
                        vertex_size=g.vp['sensitivity'],
                        vertex_color='#006600',
                        vertex_fill_color='#006600',
                        vertex_halo=True,
                        vertex_halo_color='#b3c6ff',
                        vertex_halo_size=g.vp['confidence'],
                        edge_pen_width=g.ep['second_sens'],
                        # subsample_edges=100,
                        output_size=(600, 600),
                        inline=inline,
                        output=filename
                        )
