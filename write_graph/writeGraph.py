import networkx as nx

def G_write_dot(G, graph_title):
    try:
        nx.drawing.nx_pydot.write_dot(G, f"default_dot\\{graph_title}.dot")
    except Exception as e:
        raise RuntimeError(f"Export failed: {e}")