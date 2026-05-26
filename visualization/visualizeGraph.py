import pygraphviz as pgv

def G_viz(graph_title):
    try:
        G = pgv.AGraph(f"default_dot\\{graph_title}.dot")
        G.layout(prog="fdp")
        G.draw(f"default_png\\{graph_title}.png")
    except Exception as e:
        raise RuntimeError(f"Visualization failed: {e}")