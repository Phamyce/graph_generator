import networkx as nx

def gen(n = None, m = None, p = None, k = None):
    try:
        if n and m:
            return nx.barabasi_albert_graph(n, m), f"Barabasi-Albert-{n}-nodes-{m}-edges"
        if n and p:
            return nx.erdos_renyi_graph(n, p), f"Erdos-Renyi-{n}-nodes-{p}-prob"
        if n and k and p:
            return nx.watts_strogatz_graph(n, k, p), f"Watts-Strogatz-{n}-nodes-{k}-neighbors-{p}-prob"
    except Exception as e:
        raise RuntimeError(f"Generation failed: {e}")