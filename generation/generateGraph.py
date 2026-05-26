import networkx as nx
import numpy as np
from collections import deque
import random
from math import gcd

def barabasi_albert(n, m):
    return nx.barabasi_albert_graph(n, m), f"Barabasi-Albert_{n}-nodes_{m}-edges"
    
def erdos_renyi(n, p):
    return nx.erdos_renyi_graph(n, p), f"Erdos-Renyi_{n}-nodes"
    
def watts_strogatz(n, k, p):
    return nx.watts_strogatz_graph(n, k, p), f"Watts-Strogatz_{n}-nodes-{k}_neighbors"

def forest_fire(n: int, p: float, r: float, seed=None):
    if seed is not None:
        np.random.seed(seed)
    
    G = nx.DiGraph()
    G.add_node(0)
    
    for v in range(1, n):
        existing_nodes = list(G.nodes)
        w = np.random.choice(existing_nodes)
        G.add_edge(v, w)
        
        visited = {w}
        # Очередь для узлов, для которых нужно сгенерировать x и выбрать соседей
        queue = deque()
        
        x = np.random.geometric(1 - p) - 1
        
        if x > 0:
            # Выбираем x соседей из w, добавляем связи с ними и помещаем в очередь
            new_targets = _sample_neighbors(G, w, visited, r, x)
            for z in new_targets:
                G.add_edge(v, z)
                visited.add(z)
                queue.append(z)
        
        # Рекурсивно обрабатываем узлы из очереди
        while queue:
            u = queue.popleft()
            # Генерируем x_u для текущего узла u
            x_u = np.random.geometric(1 - p) - 1
            if x_u > 0:
                new_targets = _sample_neighbors(G, u, visited, r, x_u)
                for z in new_targets:
                    G.add_edge(v, z)
                    visited.add(z)
                    queue.append(z)
    
    return G, f"Forest-Fire_{n}-nodes"
def _sample_neighbors(G, u, visited, r, k):
    # Списки соседей, ещё не посещённых
    out_neigh = [nbr for nbr in G.successors(u) if nbr not in visited]
    in_neigh  = [nbr for nbr in G.predecessors(u) if nbr not in visited]
    
    # Вероятности выбора типа связи
    prob_out = 1.0 / (1.0 + r) if r > 0 else 1.0
    prob_in = r / (1.0 + r) if r > 0 else 0.0
    
    chosen = set()
    attempts = 0
    # Делаем k попыток; каждая попытка может не дать результата,
    # если выбранный тип соседей отсутствует
    while len(chosen) < k and attempts < k * 10:  # защита от бесконечного цикла
        attempts += 1
        # Определяем, из какого множества будем выбирать
        if len(out_neigh) == 0 and len(in_neigh) == 0:
            break
        if len(out_neigh) == 0:
            # Только входящие
            pool = in_neigh
        elif len(in_neigh) == 0:
            # Только исходящие
            pool = out_neigh
        else:
            # Выбираем тип согласно вероятностям
            if np.random.random() < prob_out:
                pool = out_neigh
            else:
                pool = in_neigh
        
        if pool:
            selected = np.random.choice(pool)
            chosen.add(selected)
    
    return list(chosen)

def copying_model(n, alpha, d, initial_graph=None, seed=None):
    if seed is not None:
        random.seed(seed)

    # Если начальный граф не задан, создаём случайный d-регулярный граф
    if initial_graph is None:
        # Минимальное число вершин для d-регулярного графа
        n0 = max(d + 1, 2)
        # Для нечётного d число вершин должно быть чётным
        if d % 2 == 1 and n0 % 2 == 1:
            n0 += 1
        # Произведение n0 * d должно быть чётным
        if (n0 * d) % 2 != 0:
            n0 += 1
        G = nx.random_regular_graph(d, n0, seed=seed)
        # Преобразуем в мультиграф для возможности добавлять кратные рёбра
        G = nx.MultiGraph(G)
    else:
        # Создаём копию, чтобы не изменять исходный граф
        G = nx.MultiGraph(initial_graph)

    # Список всех вершин для равномерного выбора
    nodes_list = list(G.nodes())
    current_n = G.number_of_nodes()

    # Последовательно добавляем вершины до достижения n
    for new_node in range(current_n, n):
        G.add_node(new_node)
        nodes_list.append(new_node)
        # Старые вершины (исключая только что добавленную)
        existing_nodes = nodes_list[:-1]

        # Добавляем d рёбер из новой вершины
        for _ in range(d):
            # Равновероятно выбираем вершину p из существующих
            p = random.choice(existing_nodes)

            if random.random() < alpha:
                # --- Копирование ---
                # Случайный сосед p
                neighbors_p = list(G.neighbors(p))
                q = random.choice(neighbors_p)

                # Если копирование ведёт в новую вершину или ребро уже существует,
                # то вместо этого создаём ребро в случайную вершину (запасной вариант)
                if q == new_node or G.has_edge(new_node, q):
                    r = random.choice(existing_nodes)
                    G.add_edge(new_node, r)
                else:
                    G.add_edge(new_node, q)
            else:
                # --- Мутация ---
                # Случайная вершина из существующих
                r = random.choice(existing_nodes)
                G.add_edge(new_node, r)

    return G, f"Copying-Model_{n}-nodes_{d}-regular_graph"

def leighton_graph(n, k, b, seed=None):
    if n % k != 0:
        raise ValueError("n должно делиться на k")
    if k < 2:
        raise ValueError("k должно быть не менее 2")
    if b.get(k, 0) < 1:
        raise ValueError("b[k] должно быть не менее 1")
    
    if (n // k) % 2 == 0:
        raise ValueError("n/k должно быть нечётным для выбранной схемы m = k * 2^t")
    
    t = 20
    while k * (1 << t) <= n:
        t += 1
    m = k * (1 << t)
    
    primes = set()
    temp = k
    p = 2
    while p * p <= temp:
        if temp % p == 0:
            primes.add(p)
            while temp % p == 0:
                temp //= p
        p += 1
    if temp > 1:
        primes.add(temp)
    L = 4  # всегда учитываем 4 для условия (v)
    for prime in primes:
        L = L * prime // gcd(L, prime)
    a = 1 + L
    # Убедимся, что a < m
    if a >= m:
        raise ValueError("Не удалось подобрать a < m. Увеличьте t или измените параметры.")
    
    c = 1  # gcd(1, m)=1
    if seed is None:
        x0 = random.randint(0, m-1)
    else:
        random.seed(seed)
        x0 = random.randint(0, m-1)
    
    def y_generator():
        nonlocal x0
        x = x0
        while True:
            x = (a * x + c) % m
            yield x % n
    
    gen = y_generator()
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    for size in range(k, 1, -1):
        count = b.get(size, 0)
        for _ in range(count):
            # Берём size последовательных значений y
            vertices = [next(gen) for _ in range(size)]
            # Добавляем все рёбра между уникальными вершинами
            # (повторы игнорируются, они не создают петель)
            vert_set = set(vertices)
            for u in vert_set:
                for v in vert_set:
                    if u < v:
                        G.add_edge(u, v)
    
    return G, f"Leighton-Graph_{n}-nodes_{k}-chromatic-number"
