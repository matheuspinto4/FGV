import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


def coinChange(coins, amount: int) -> int:
    l = []
    G = {i: {} for i in range(0, amount + 1)}

    for i in range(0,amount + 1):
        for c in coins:
            j = i + c
            if j <= amount:
                G[i][j] = c
                
    # for v, a in G.items():
    #     print(f"{v}:")
    #     for u, p in a.items():
    #         print(f"    {u}: {p}")
    #     print("_"*50)



    T = deque([0])
    d = {v: float("inf") for v in range(0, amount + 1)}
    d[0] = 0
    pai = {v: None for v in range(0, amount + 1)}
    lista = []
    while T:
        u = T.popleft()
        for v, coin in G[u].items():
            if d[u] + 1 < d[v]:
                d[v] = d[u] + 1
                pai[v] = u
                T.append(v)    

    # filho = amount
    # while(filho):
    #     lista.append(filho - pai[filho])
    #     filho = pai[filho]
    # lista = list(reversed(lista))
    
    return(d[amount])

coins = [1, 3, 4]
amount = 10

print(coinChange(coins, amount))

# print(questao(coins, amount))