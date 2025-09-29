# **Colinha de Ciência de Redes**
```shell
pip install numpy scipy matplotlib networkx pandas
```
```python 
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from collections import Counter
import pandas as pd
```

## **Construindo Grafos**

- Pela Matriz de Adjacência:
```python 
A # Matriz de Adjacência
G = nx.from_numpy_array(A, create_using=nx.Graph)
```
- Pelas Arestas:
```python 
edge_list = [('A', 'B'), ('B', 'C'), ('C', 'A')]
G = nx.Graph()
G.add_edges_from(edge_list)
```

- A partir de um arquivo:
```python
edge_list = []
with open('rede.txt', 'r') as file:
    for l in file:
        if not l.strip(): continue
        nodes = l.strip().split()
        if len(nodes) == 2: edge_list.append((nodes[0], nodes[1]))
```

## **Mostrando os Grafos**

```python
G # É um grafo
nx.draw(G, pos=nx.spring_layout(G))  # Desenha o próprio grafo
```
- Caso queria legenda (Precisa fazer o passso acima antes):
```python
labels = {n : f"{legenda_para_o_nó_n}" for n in G.nodes()}  
nx.draw_networkx_labels(G, pos=nx.planar_layout(G),  # Mesma que o grafo.
                        labels=labels) 
```


## **Medidas de um Grafo:**

### Componentes conexas:

- Para grafos **direcionados**:
    - **Fortemente Conexa:** segue o sentido das arestas
    - **Fracamente Conexa:** ignora o sentido das arestas
```python
list(nx.connected_components(G))  # [{A, B, C}, {D, F}]
```
### Graus:
```python 
G.degree # lista com (nó, grau)
l_g = [g, for n,d in G.degree]  # Lista Graus
sum(l_g) / G.number_of_nodes()  # grau médio
# Contagem dos graus:
contagem_graus = Counter(l_g)  # Separa os graus por frequência
deg, cnt = zip(*contagem_graus.items())  # Prepara para plotar
plt.bar(deg, cnt)  # Plota

# Grau ponderado de cada nó (levando em conta o peso)
weighted_degree = dict(G.degree(weight="weight"))
avg_weighted_degree = sum(weighted_degree.values()) / len(weighted_degree)


```
### Diâmetro:

- É o maior caminho mais curto entre quaisquer dois nós.
- **desconexos:** calculamos o diâmetro da **maior componente conexa**.
- **direcionados:** calculamos o diâmetro da maior componenente **fortemente conexa**
#### Direcionado:
```python
maior_cc = max(nx.strongly_connected_components(G_direcionado), key=len)
subG = G.subgraph(maior_cc) 

for u, v, d in subG.edges(data=True): 
    d["dist"] = 1 / d["weight"]  # peso não é proporcional a distância
    d["dist"] = d["weight"]      # peso é proporcional a distância
 
diametro_ponderado =  nx.diameter(subG, weight="dist") 
diametro_sem_peso = nx.diameter(subG) 
```
#### não direcionado:
```python
diameter = nx.diameter(G) # normal
diameter_poderado = nx.diameter(G, weight="weight") # ponderado
```

### Centralidade:
| Centralidade | O que mede | Como calcular | Função no NetworkX | Significado |
|--------------|------------|---------------|--------------------|-------------|
| **Grau (Degree)** | Popularidade ou atividade (número de conexões). | Conta as arestas conectadas ao nó. <br> - In-degree: nº de arestas que chegam. <br> - Out-degree: nº de arestas que saem. | `nx.degree_centrality(G)` <br> `nx.in_degree_centrality(G)` <br> `nx.out_degree_centrality(G)` | Nó com alto grau é ativo/popular; em dígrafos: in-degree → prestígio, out-degree → influência. |
| **Proximidade (Closeness)** | Eficiência em alcançar os demais nós. | Inverso da soma das distâncias mínimas: <br> \[ C(v) = \frac{1}{\sum_u d(v,u)} \] | `nx.closeness_centrality(G)` | Nó com alta proximidade consegue difundir ou receber informação rapidamente. |
| **Intermediação (Betweenness)** | Controle sobre fluxos (ponte). | Fração de caminhos mais curtos entre pares que passam pelo nó. | `nx.betweenness_centrality(G)` | Nó com alta intermediação é gargalo; controla fluxos e pode fragmentar a rede se removido. |
| **Autovetor (Eigenvector)** | Influência qualitativa (importância dos vizinhos). | Calculado iterativamente: importância ∝ soma das importâncias dos vizinhos. | `nx.eigenvector_centrality(G)` | Nó é influente se conectado a outros nós já influentes. |
| **PageRank (PR)** | Autoridade em grafos direcionados. | Variante do autovetor com fator de amortecimento (α≈0.85). | `nx.pagerank(G, alpha=0.85)` | Nó é relevante se recebe links de nós importantes (modelo da Web). |

#### PageRank, Cálculo:
- A partir da matriz de adjacência $A$ se constrói $M$:
    - Se $j$ tem $k$ elementos de saída: $M_{i,j} = 1 / k$
    - Cada coluna deve somar $1$
- $R$ é um vetor que começa com seus elementos sendo igual a $\frac{1}{n}$.
- $R^{(t+1)} = \alpha M R^{(t)} + (1 - \alpha) \frac{1}{n}$ 
    - Onde $\alpha$ é um fator de probabilidade de salto entre nós aleatórios.

#### Top centralidades, Calculo computacional:
```python
top10_degree = sorted(nx.degree_centrality(G_direcionado).items(),  # Exemplo com centralidade por grau, basta trocar pelo
                    key=lambda x: x[1], reverse=True)[:10]               
```

### Clustering:
- O coeficiente de agrupamento mede o quanto os vizinhos de um nó também estão conectados entre si.
- $C_i = \frac{\text{nº de triângulos passando por i}}{\text{nº máximo de triângulos possíveis em i = } \frac{k(k-1)}{2}}$
- Coeficiente de agrupamento médio: $\frac{\sum{C_i}}{N} \isin [0,1]$
- Um coeficiente médio perto de $0$ significa que a rede é dispersa.

```python
clustering_por_no = nx.clustering(G)  # coeficiente de agrupamento de cada nó
average_clustering = nx.average_clustering(G)  # coeficiente médio do grafo
```

## **Propriedades Adversas:**
### Projeção em Vértices:
Propriedade de grafos bipartidos.
- Cria-se um novo grafo com a seguinte propriedade:
    - Para um dos conjuntos ($U$ ou $V$), se dois vértices conectam um mesmo vértice do outro conjunto, então eles serão conectados no novo grafo.
- Forma computacional:
```python
### Calculando para o Conjunto V:
B = A[6:, :6] # Conjunto V: {5,6,7,8,9,10}
B_proj = B @ B.T
B_proj = (B_proj > 0).astype(np.uint8)
np.fill_diagonal(B_proj, 0)
print(B_proj)
G_proj = nx.from_numpy_array(B_proj, create_using=nx.Graph)
nx.draw(G_proj)
```

### Mundo Pequeno:
Um grafo apresenta esta propriedade quando:
1. O número médio de passos necessários para ir de um nó até outro é muito pequeno 
    1.1 O caminho mínimo médio apresenta um crescimento logaritmo do número de nós: $l \propto \ln N$ 

2. Alto coeficiente de Clustering. Ou seja, uma componente conexa.
## **Modelos de Grafos:**

### Modelo Aleatório (Erdős-Rényi - ER)
| Métrica                       | Comportamento no Modelo ER                  | Explicação Teórica                                                                                                                                          |
|-------------------------------|---------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| N° de Componentes Conexas  | Varia muito com a densidade (p).             | A rede passa por uma transição de fase. Abaixo de um limiar de grau médio (⟨k⟩<1), há muitas componentes pequenas. Acima do limiar (⟨k⟩>lnN), a rede tem apenas uma grande componente (o *giant component*) e poucas ilhas isoladas. |
| Tamanho Relativo da LCC    | 0 ou ≈1 (depende da transição).              | O tamanho da Maior Componente Conexa (LCC) salta de zero para quase o tamanho total da rede (N) quando o grau médio ⟨k⟩ ultrapassa o valor crítico ⟨k⟩=lnN. |
| Grau Médio (⟨k⟩)           | Fácil de calcular: ⟨k⟩=N⋅p                   | O grau médio é determinado pela probabilidade p de uma aresta existir e é previsível.                                                                       |
| Variância dos Graus        | Baixa. Varia de acordo com a média (Var(k)=⟨k⟩). | Como a distribuição é de Poisson, a variância é baixa. Isso significa que todos os nós têm graus muito próximos à média; a rede é homogênea.               |
| Distribuição dos Graus     | Distribuição de Poisson (ou Binomial).       | Uma distribuição com uma cauda curta e um pico bem definido no grau médio (⟨k⟩). A probabilidade de um hub existir é exponencialmente pequena.             |



### Modelo de Mundo Pequeno (Watts-Strogatz - WS)

| Métrica                       | Comportamento no Modelo WS                  | Explicação Teórica                                                                                                                                          |
|-------------------------------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| N° de Componentes Conexas      | Geralmente 1.                              | O processo de "refiação" de arestas (adicionando atalhos) garante que a rede se torne rapidamente uma única componente gigante altamente conectada, mesmo para valores baixos de probabilidade de refiação (β). |
| Tamanho Relativo da LCC        | ≈1.                                        | A LCC abrange quase todos os nós, garantindo que o conceito de "mundo pequeno" se aplique à maior parte da rede.                                           |
| Grau Médio (⟨k⟩)               | Fixo. ⟨k⟩ é constante.                     | O grau médio é fixado pelo grau inicial K (número de vizinhos em anel) e não muda, pois a refiação apenas move arestas, sem criar nem destruir.           |
| Variância dos Graus            | Baixa. Similar ao ER, mas pode ser ligeiramente maior. | A aleatoriedade do refiamento introduz alguma variância, mas a distribuição ainda é concentrada em torno da média. Não há a formação de hubs massivos.   |
| Distribuição dos Graus         | Distribuição de Poisson (similar ao ER).   | A distribuição é concentrada em torno do grau médio. A estrutura em anel domina e o refiamento aleatório não é suficiente para criar uma cauda de Lei de Potência. |



### Modelo de Anexação Preferencial (Barabási-Albert - BA)

| Métrica                       | Comportamento no Modelo BA                  | Explicação Teórica                                                                                                                                          |
|-------------------------------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| N° de Componentes Conexas      | Geralmente 1.                              | O processo de crescimento contínuo e a regra de anexação preferencial garantem que cada novo nó se conecte a um nó existente. Isso assegura que a rede se mantenha como uma única componente gigante desde o início. |
| Tamanho Relativo da LCC        | ≈1.                                        | Essencialmente, a LCC é a rede inteira.                                                                                                                    |
| Grau Médio (⟨k⟩)               | Constante. ⟨k⟩=2m                          | O grau médio é determinado pelo parâmetro m (o número de arestas que cada novo nó adiciona) e é constante à medida que a rede cresce.                     |
| Variância dos Graus            | Muito Alta.                                | A variância é alta porque há uma grande disparidade de graus. Os poucos hubs têm graus que são ordens de magnitude maiores que o grau médio, enquanto a maioria dos nós tem grau muito baixo. |
| Distribuição dos Graus         | Lei de Potência (P(k)∝k−3).               | Uma distribuição de cauda longa. Isso significa que a maioria dos nós tem grau baixo (a cauda curta), mas os hubs com grau extremamente alto, embora raros, são muito mais prováveis do que seriam em uma rede aleatória. |
