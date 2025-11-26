import sys
import heapq
from collections import deque
from typing import List, Tuple, Dict, Set

# sys.setrecursionlimit(200010)

##### ATENÇÃO #####
# Não altere o nome deste arquivo.
# Não altere a assinatura das funções.
# Não importe outros módulos além dos já importados.
# Você pode criar outras funções ou classes se julgar necessário, mas deve defini-las no corpo da função do exercicio.

# ==============================================================================
# Problema de exemplo
# ==============================================================================
def problema_0(n: int, m: int, A: List[Tuple[int, int]]) -> int:
    """
    Recebe um grafo com $n$ vertices numerados de $1$ a $n$ e m arestas
    bidirecionadas e retorna o número de componentes conexas do grafo.
    
    Complexidade: O(n + m)
    """

    # Podemos utilizar listas simples, ao invés de dicionários ou conjuntos, para 
    # representar o grafo, já que os vértices são numerados de 1 a n.
    # Isso economiza processamento e memória.
    visited = [False] * (n + 1)
    adj = [[] for _ in range(n + 1)] # lista de adjacência
	
    # Construindo o grafo
    for u, v in A:
        adj[u].append(v)
        adj[v].append(u)

    # No geral, dê preferência a BFS iterativa, pois é mais eficiente que a
    # DFS recursiva (principalmente em Python).
    def bfs(start: int):
        queue = deque([start]) # fila para BFS
        visited[start] = True

        while queue:
            u = queue.popleft() # nó atual

            for v in adj[u]: # vizinhos
                if not visited[v]:
                    visited[v] = True
                    queue.append(v)

    number_of_components = 0
    for u in range(1, n + 1):
        if not visited[u]:
            bfs(u)
            number_of_components += 1

    return number_of_components


# ==============================================================================
# Problema 1 - Sisi e a Sorveteria: Parte 2
# ==============================================================================

def problema_1(n: int, A: List[int]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n)$ que encontre a quantidade
    máxima total de sorvete que Sisi pode obter.

    Entrada:
    A entrada consiste em uma lista de $n$ inteiros $A = [a_1, a_2,  dots, a_n]$,
    onde $a_i$ é o estoque do $i$-ésimo sorvete.

    Saída:
    Retorne um único inteiro $Q$, a quantidade máxima total de sorvete
    que Sisi pode obter.
    """
    Q = 0
    for k in range(n):  
        i = n - k - 1  #  Começando do fim da fila até o início
        if i == n - 1:
            A[i] = A[i]  #  Não altera
        elif A[i] >= A[i + 1]:
            A[i] = max(A[i+1] - 1, 0) #  Recebe o máximo entre 0 e o próximo menos 1
        else:
            A[i] = A[i]

        Q += A[i]
    return Q
    

# ==============================================================================
# Problema 2 - Minimizando Custos de Reparo
# ==============================================================================

def problema_2(n: int, k: int, C1: int, C2: int, A: List[int]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(k * log k)$ que encontre o
    custo mínimo para reparar a estrada.

    Entrada:
    - $n$: O expoente do comprimento da estrada ($L = 2^n$).
    - $C1$, $C2$: As constante de custo.
    - $A = [a_1, a_2,  dots, a_k]$: Uma lista com as $k$ posições dos buracos.

    Saída:
    - Retorne um único inteiro: o custo mínimo total para reparar toda a estrada.
    """
    def computar_custo(n: int, k: int, C1: int, C2: int):
        if k == 0: 
            return C1
        else:
            return (2 ** n) * C2 * k
    
    def busca_binaria(A, mid_term):
        inicio, fim = 0, len(A) - 1
        while(inicio <= fim):
            meio = (inicio + fim) // 2
            if A[meio] > mid_term:
                fim = meio - 1
            else:
                inicio = meio + 1
                
        return inicio
    
    def recursao(n, inicio: int, fim: int, C1: int, C2: int, A_seg: List[int]):
        k_local = len(A_seg)
        custo_t = computar_custo(n, k_local, C1, C2)

        if n == 0:
            return custo_t

        mid_value = (fim + inicio) // 2

        index_meio = busca_binaria(A_seg, mid_value)

        custo_e = recursao(n-1, inicio, mid_value, C1, C2, A_seg[:index_meio]) 
        custo_d = recursao(n-1, mid_value + 1, fim, C1, C2, A_seg[index_meio:])

        return min(custo_t, custo_e + custo_d)
    
    A.sort()
    return recursao(n, 1, 2**n, C1, C2, A) 

# ==============================================================================
# Problema 3 - Subsequências radicais
# ==============================================================================

def problema_3(n: int, A: List[int]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n * sqrt n)$ que retorne
    a quantidade de subsequências radicais.

    Entrada:
    - $A = [a_1, a_2,  dots, a_n]$ (com $1 <= a_i <= n$).

    Saída:
    - A quantidade total de subsequências radicais, módulo $999999937$.
    """

    #  Para cada valor A[i]:
    #       Para k in [1, ..., sqrt(i), i-1]:
    #           Se A[i] for divisível por (k + 1): 
    #               adicionar na lista de divisores de A[i] os valores (k + 1) e A[i] / (k + 1)
    #           Caso contrário: M[k] = M[k]
    #  Total = Sum(M[k])
    #  Return Total

    M = [0] * (n + 1)
    M[0] = 1

    def divisores(a):
        divisores = []
        for k in range(1, int(a ** 0.5) + 1):
            if a % k == 0:
                divisores.append(k)
                if k * k != a: 
                    divisores.append(a // k)
        divisores.sort()
        return divisores
    

    for a in A:
        for k in reversed(divisores(a)):
            if k > n: continue

            M[k] += M[k - 1]
    
    return sum(M) % 999999937 - 1
        

# ==============================================================================
# Problema 4 - Cavalo
# ==============================================================================

def problema_4(n: int) -> List[List[int]]:
    """
    Desenvolva um algoritmo com complexidade $O(n^2)$ que retorne
    a matriz de movimentos mínimos.

    Entrada:
    - $n$: O tamanho do lado do tabuleiro ($3   <= n   <= 10^3$).

    Saída:
    - Retorna uma matriz $A$, onde $A[i][j]$ é o número mínimo de
      movimentos para um cavalo ir da posição (i, j) para a posição (0, 0).
    """

    def possiveis_nos(i, j, n):
        lista = []
        for k in [-1, 1]:
            for t in [-1, 1]:
                if (n - 1 >= i + 2*k >= 0) and (n - 1 >= j + t >= 0):
                    lista.append((i + k*2, j + t))

                if (n - 1 >= i + k >= 0) and (n - 1 >= j + 2*t >= 0):
                    lista.append((i + k, j + 2*t))
        return lista
    

    #  Preenchendo a matriz Tabuleiro T
    T = []
    Antingiu = []
    for i in range(n):
        T.append([])
        Antingiu.append([])
        for j in range(n):
            Antingiu[i].append(False)
            T[i].append(float("inf"))

    Antingiu[0][0] = True
    T[0][0] = 0  
    
    #  bfs:
    queue = deque([(0,0)])
    while len(queue) != 0:
        no = queue.popleft()
        for vizinho in possiveis_nos(*no, n):
            i,j = vizinho 
            if Antingiu[i][j]: 
                continue
            else:
                T[i][j] = T[no[0]][no[1]] + 1
                Antingiu[i][j] = True
                queue.append(vizinho)
    
    return T



# ==============================================================================
# Problema 5 - Escape se for possível
# ==============================================================================

def problema_5(n: int, m: int, grid: List[List[str]]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n^2)$ que retorne
    o menor tempo para escapar.

    Entrada:
    - grid: Uma lista de listas de strings representando a caverna.

    Saída:
    - Retorne o menor tempo para escapar. Se não for possível, retorne -1.
    """
    def get_vizinhos(i, j, n, m):
        vizinhos = []
        for k in [-1, 0, 1]:
            for t in [-1, 0, 1]:
                if abs(k) == abs(t): continue
                if (0 <= i + k < n) and (0 <= j + t < m):
                    vizinhos.append((i + k, j + t))
        return vizinhos
    
    
    #  Ideia:
    #  1: Calcular em qual o menor tempo que cada célula do grid irá ser atingida por água
    #       Usar BFS
    #  2: Calcular o menor caminho até todas as células começando em V
    #       Usar BFS
    #  Subtrair as distancias (1) - (2) para cada célula
    #  Checar Se alguma ponta '.' possui um valor positivo e escolher o menor

    #  Matriz com os tempos e booleanos dizendo se atingiu:
    A = []    
    V = []    
    A_Atingiiu = []
    V_Atingiiu = []
    for i in range(n):
        A.append([])
        V.append([])
        A_Atingiiu.append([])
        V_Atingiiu.append([])
        for j in range(m):
            A[i].append(float("inf"))
            V[i].append(float("inf"))
            A_Atingiiu[i].append(False)
            V_Atingiiu[i].append(False)
    
    fila_agua = deque()
    pos_jogador = None
    fila_jogador = deque()
    for i in range(n):
        for j in range(m):
            if grid[i][j] == 'A': 
                fila_agua.append((i,j))
                A[i][j] = 0
                A_Atingiiu[i][j] = True
            if grid[i][j] == 'V': 
                pos_jogador = (i,j)
                fila_jogador.append(pos_jogador)
                V_Atingiiu[i][j] = True
                V[i][j] = 0

    #  BFS para as aguas:
    while (len(fila_agua) != 0):
        agua = fila_agua.popleft()
        for vizinho in get_vizinhos(*agua, n=n, m=m):
            i_vizinho, j_vizinho = vizinho
            if grid[i_vizinho][j_vizinho] == "#": continue
            if A_Atingiiu[i_vizinho][j_vizinho]: continue
            
            A_Atingiiu[i_vizinho][j_vizinho] = True
            A[i_vizinho][j_vizinho] =  A[agua[0]][agua[1]] + 1
            fila_agua.append(vizinho)

    #  BFS para o Jogador:
    while (len(fila_jogador) != 0):
        jogador = fila_jogador.popleft()
        for vizinho in get_vizinhos(*jogador, n=n, m=m):
            i_vizinho, j_vizinho = vizinho
            if grid[i_vizinho][j_vizinho] == "#": continue
            if V_Atingiiu[i_vizinho][j_vizinho]: continue
            
            V_Atingiiu[i_vizinho][j_vizinho] = True
            V[i_vizinho][j_vizinho] =  V[jogador[0]][jogador[1]] + 1
            fila_jogador.append(vizinho)
    
    for i in range(n):
        for j in range(m):
            if grid[i][j] == "#": continue
            A[i][j] -= V[i][j]


    #  Procurando o menor dos valores nas laterais:
    tempos_possiveis = []
    for j in range(m):
        if grid[0][j] == '.' or grid[0][j] == 'V':
            if A[0][j] > 0 : tempos_possiveis.append(V[0][j])
        if grid[-1][j] == '.' or grid[-1][j] == 'V':
            if A[-1][j] > 0 : tempos_possiveis.append(V[-1][j])
    for i in range(n):
        if grid[i][0] == '.' or grid[i][0] == 'V':
            if A[i][0] > 0 : tempos_possiveis.append(V[i][0])
        if grid[i][-1] == '.' or grid[i][-1] == 'V':
            if A[i][-1] > 0 : tempos_possiveis.append(V[i][-1])
    
    if len(tempos_possiveis) == 0: return -1
    else: return min(tempos_possiveis)

    
# ==============================================================================
# Problema 6 - Viagem Intergalática
# ==============================================================================

def problema_6(n: int, m: int, rotas: List[Tuple[int, int, int]]) -> int:
    """wh
    Desenvolva um algoritmo com complexidade $O(m  log n)$ que retorne
    o custo mínimo total.

    Entrada:
    - $n$: Número de planetas ($1 <= n <= 10^5$).
    - $m$: Número de rotas ($1 <= m <= 2 * 10^5$).
    - rotas: Lista de $m$ tuplas $(a, b, c)$, onde $a$ é a origem,
      $b$ é o destino e $c$ é o custo.

    Saída:
    - Retorne o menor custo total possível para a viagem.
    """
    #  Podemos realizar um dikstra modificado:
    #    Cada aresta possui dois estados: cupom usado e não usado
    #    Se o caminho até ela já usou um cupom, então não pode usar mais
    #    Se o caminho até ela ainda não usou um cupom, então pode-se usar ou não agora
    #    Sempre é escolhido o melhor para os nós na franja.    

    def converter_grafo(lista_arestas, n):
        G = {vertice : {} for vertice in range(1, n+1)}
        
        for aresta in lista_arestas:
            G[aresta[0]][aresta[1]] = aresta[2]  #  (vértice, peso)

        return G
    
    
    G = converter_grafo(rotas, n)
    distancias = {v : ((0, 0) if v == 1 else (float("inf"), float("inf"))) for v in G.keys()}  #  distancias (Cupom usado, cupom não usado) 
    pais = {v : None for v in G.keys()}
    T = [ (0, 1, 0) ]  #  (Custo toal, vertice, copom usado(1) / não usado (0))

    while T:
        custo_v, v, usado = heapq.heappop(T)

        for u, peso_u in G.get(v, {}).items():
            
            if usado == 0:  #  Cupom ainda não usado

                #  Tentando usar o cupom aqui:
                custo_aresta_c_cupom = peso_u // 2
                novo_custo_u_usado  = custo_v + custo_aresta_c_cupom

                #  Relaxamento:
                if novo_custo_u_usado < distancias[u][0]:
                    pais[u] = v
                    distancias[u] = (novo_custo_u_usado, distancias[u][1])
                    heapq.heappush(T, (novo_custo_u_usado, u, 1))
                
                #  Tentando não usar o cupom:
                custo_aresta_s_cupom = peso_u
                novo_custo_u_n_usado = custo_v + custo_aresta_s_cupom

                #  Relaxamento:
                if novo_custo_u_n_usado < distancias[u][1]:
                    distancias[u] = (distancias[u][0], novo_custo_u_n_usado)
                    heapq.heappush(T, (novo_custo_u_n_usado, u, 0))
                    pais[u] = v
            
            else:  #  Cupom já foi usado
                custo_aresta_s_cupom = peso_u
                novo_custo_u_usado = custo_v + custo_aresta_s_cupom

                #  Relaxamento:
                if novo_custo_u_usado < distancias[u][0]:
                    distancias[u] = (novo_custo_u_usado, distancias[u][1])
                    heapq.heappush(T, (novo_custo_u_usado, u, 1))
                    pais[u] = v
    
    return int(min(distancias[n])) 


# ==============================================================================
# Problema 7 - Reparo das Estradas
# ==============================================================================

def problema_7(n: int, m: int, estradas: List[Tuple[int, int, int]]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(m  log n)$ que retorne
    o custo mínimo total para conectar as cidades.

    Entrada:
    - $n$: Número de cidades ($1 <= n <= 10^5$).
    - $m$: Número de estradas ($1 <= m <= 2 * 10^5$).
    - estradas: Lista de $m$ tuplas $(a, b, c)$, onde $a$ e $b$ são
      cidades e $c$ é o custo do reparo.

    Saída:
    - Retorne o custo mínimo total para conectar todas as $n$ cidades.
    """
    #  Podemos usar o algoritmo de prim para montar a mst

    G = {v : {} for v in range(1, n+1)}
    for v, u, peso in estradas: G[v][u] = peso; G[u][v] = peso 
    mst = set()
    T = [(0, 1)]  #  Heap (peso, vértice)
    custo = 0
    
    while T:
        peso, u = heapq.heappop(T)
        if u in mst: continue
        custo += peso
        mst.add(u)
        
        for v, peso_uv in G.get(u, {}).items():
            if v not in mst: # and peso_uv < d[v]:
                heapq.heappush(T, (peso_uv, v))

    return custo

# ==============================================================================
# Problema 8 - Video Game
# ==============================================================================

def problema_8(n: int, m: int, transicoes: List[Tuple[int, int]]) -> int:
    """
    Desenvolva um algoritmo com complexidade $O(n + m)$ que encontre o número
    de formas distintas de ir do estado 1 ao estado $n$.

    Entrada:
    - $n$: O número de estados ($1 <= n <= 10^5$).
    - $m$: O número de transições ($1 <= m <= 2 * 10^5$).
    - transicoes: Uma lista com $m$ tuplas $(a, b)$ representando
      transições válidas.

    Saída:
    - Retorne um único inteiro: o número de formas distintas de ir do
      estado 1 ao estado $n$.
    """
    #  Primeiramente, achamos a ordem topológica do grafo
    #  Começando a partir do último nó desta sequência topológica:
    #       contagem = 0
    #       Para cada aresta sua que se conecta diretamente ao nó "n", soma-se um na contagem
    #       Para cada aresta sua que se liga a outro nó, soma-se à sua contagem a contagem deles
    #  Quando chegar em 1, basta ver a sua contagem 


    #  (1) Preenchendo o grafo:
    G = {}
    for no in range(1, n+1):
        G[no] = [0, 0, []]  # [contagem, grau_entrada, vizinhos]
    
    G[n][0] = 1  #  Caso base para o nó 'n'

    for aresta in transicoes:
        G[aresta[0]][2].append(aresta[1])
        G[aresta[1]][1] += 1

    # (2) Achando a ordem topológica:

    fila = deque()
    for no, valores in G.items():
        if valores[1] == 0:
            fila.append(no)
    
    ordem_topologica = []
    while fila:
        no = fila.popleft()
        ordem_topologica.append(no)  #  Já pode adicionar o nó na ordem topológica
       
        valores = G[no]
        vizinhos_no = valores[2]

        for vizinho in vizinhos_no:
            grau_entrada_vizinho = G[vizinho][1]
            
            grau_entrada_vizinho -= 1  #  Diminui um grau de entrada do vizinho 
            if grau_entrada_vizinho == 0:
                fila.append(vizinho)  #  Já pode adicionar o vizinho na fila

            G[vizinho][1] = grau_entrada_vizinho
    

    #  (3)  Realizando a contagem:
    for no in reversed(ordem_topologica):
        valores = G[no]
        contagem = valores[0]
        grau_entrada = valores[1]
        vizinhos = valores[2]

        for vizinho in vizinhos:
            contagem += G[vizinho][0]  #  Soma-se a contagem do vizinho

        G[no][0] = contagem
    

    #  (4)  Retornando a contagem para o nó 1
    return G[1][0]
                


