"""Visualization.

Toolbox of functions to visualize results from the pathway debugging module.
"""

__all__ = ["plot_pathway"]

from collections import Iterable

import numpy as np
import matplotlib.pyplot as plt

import networkx as nx

from rdkit import Chem
from rdkit.Chem import Draw

# Remove white background and highlight atoms/bonds with white circles/lines, respectively
_DRAWING_OPTIONS = Draw.MolDrawOptions()
_DRAWING_OPTIONS.clearBackground = False
_DRAWING_OPTIONS.setHighlightColour((1, 1, 1))
_DRAWING_OPTIONS.highlightBondWidthMultiplier = 20


def _get_image(inchi, size):
    # Returns a PIL image from an InChI string
    mol = Chem.MolFromInchi(inchi)
    return Draw.MolToImage(
        mol,
        size=size,
        options=_DRAWING_OPTIONS,
        highlightAtoms=[atom.GetIdx() for atom in mol.GetAtoms()],
        highlightBonds=[bond.GetIdx() for bond in mol.GetBonds()],
    )


def plot_pathway(metabolites, offtargets, img_size=0.1, nrows=1, figsize=None):
    """
    Plots a pathway consisting of known intermediates and off-target metabolites resulting from unexpected enzyme
    activity.

    Paramters
    ---------
    metabolites : dict
        Dictionary of (name, InChI depiction) pairs for known pathway intermediates.
    offtargets : dict
        Dictionary of (name, list of InChI depictions) pairs. Names must correspond to the keys specified in
        `metabolites`. Values are a list of InChI strings representing off-target products.
    img_size : float
        Dimension of the metabolite images, specified as a fraction of the figure's width and height.
    nrows : int, default 1
        If greater than 1, the pathway will be split into the specified number of sub-pathways for better readability.
    figsize : tuple
        Tuple containing the figure dimensions (width and height, in inches). If not specified, the default size is
        calculated as 16 in × (4 * `nrows`) in.

    Returns
    -------
    fig : matplotlib.figure.Figure

    axs : array of matplotlib.axes.Axes
    """
    if figsize is None:
        figsize = (16, 4 * nrows)

    fig, axs = plt.subplots(figsize=figsize, nrows=nrows)
    if not isinstance(axs, Iterable):
        axs = [axs]

    fixed_nodes = [*metabolites.values()]
    extra_nodes = [*offtargets.values()]

    n_edges = len(fixed_nodes) - 1

    start = 0
    for i in range(nrows):
        # Divide pathway into even steps
        size = n_edges // nrows + int((i + 1) <= (n_edges % nrows))
        end = start + size + 1

        # Create and populate pathway graph
        nodes = fixed_nodes[start:end]
        graph = nx.Graph()
        graph.add_nodes_from(nodes)
        for j, node in enumerate(nodes, start):
            if j >= start + size:
                continue
            # Add pathway intermediates
            graph.add_edge(node, fixed_nodes[j + 1], offtarget=False)
            # Add off-target metabolites
            for extra_node in extra_nodes[j]:
                if extra_node not in graph:
                    graph.add_node(extra_node)
                    graph.add_edge(node, extra_node, offtarget=True)

        # Obtain node positions
        seed_pos = {node: (x, 0) for node, x in zip(nodes, np.linspace(-0.5, 0.5, size + 1))}
        pos = nx.spring_layout(graph, pos=seed_pos, fixed=nodes)

        # Obtain edge colors
        edges = [[], []]
        for (u, v, d) in graph.edges(data=True):
            edges[d["offtarget"]].append((u, v))

        # Draw nodes and edges
        nx.draw_networkx_nodes(graph, pos, ax=axs[i], node_size=2000, node_color="w")
        nx.draw_networkx_edges(graph, pos, ax=axs[i], edgelist=edges[0], width=3)
        nx.draw_networkx_edges(graph, pos, ax=axs[i], edgelist=edges[1], width=3, edge_color="r", style="dashed")

        # Add molecule drawings
        fig_trans = axs[i].transData.transform
        ax_trans = fig.transFigure.inverted().transform

        for node, coords in pos.items():
            # Calculate image size in pixels
            px_size = np.ceil(fig.get_size_inches() * img_size * fig.dpi).astype(int).tolist()
            img = _get_image(node, px_size)
            # Overlay image
            x, y = ax_trans(fig_trans(coords))
            img_ax = fig.add_axes([x - 0.5 * img_size, y - 0.5 * img_size, img_size, img_size])
            img_ax.imshow(img)
            img_ax.set_aspect("equal")
            img_ax.axis("off")

        axs[i].axis("off")

        start += size

    return fig, axs
