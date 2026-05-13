import pygraphviz as pgv

def G_draw(graph_title):
    try:
        G = pgv.AGraph(f"default_exp\\{graph_title}.dot")
        G.layout(prog="dot")
        G.draw(f"default_viz\\{graph_title}.png")
    except Exception as e:
        raise RuntimeError(f"Visualization failed: {e}")