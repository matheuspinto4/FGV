# Network Science *Albert-László Barabási*

## Chapter 2 Teoria dos Grafos

### 2.1 As pontes de Konigsberg

A Teoria de grafos tem seu nascimento datado em 1735, quando Euler tentou modelar o problema das pontes da cidade alemã konigsberg

### 2.2 Rede e Grafos

Caso queiramos entender um sistema complexo, primeiramente devemos saber como seus componentes interagem uns com os outros.

* **número de Nós**, ou N,  representa o número de componentes no sistema. Cada nó contém um "id" que o representa.

* **Número de links**, ou L, representa o total de interações entre nós.

**Rede Orientada:** é assim chamada uma rede se todos os seus links são orientados. É **Rede Não-orientada** se todos os seus links são não-orientados. Uma rede pode ser híbrida neste quesito.

### 2.3 Grau, Grau Médio e Dsitribuição de Graus.

Uma propriedade chave de cada nó é o seu grau, representando o número de links que lee tem com outros nós.

#### Grau

Denotamos com **$k_i$** o grau do **$i^{th}$** nó da rede.

Numa rede não direcionada o *número total de links*, L, pode ser expresso desta forma:

**$$
L = \frac{1}{2}\sum_{i=1}^N{k_i}$$**

O fator 1/2 está ali pois cada link é contado duas vezes na soma.

#### Grau Médio

O grau médio é uma importante propriedade.

- **Rede Não direcioanda:**

**$$
\left< k\right> = \frac{1}{N}\sum_{i=1}^N{k_i} = \frac{2L}{N}$$**

- **Rede Direcionada:** 

**$$
L = \sum_{i=1}^{N}{k^{in}} = \sum_{i=1}^{N}{k^{out}}$$**

**$$
\left< k^{in}\right>  = 
\left< k^{out}\right> = \frac{1}{N}\sum_{i=1}^N{k_i^{in}} = \frac{1}{N}\sum_{i=1}^N{k_i^{out}} = \frac{L}{N}$$**

#### Distribuição de Graus

O *grau de distribuição*, **$p_k$**, dá a probabilidade que um nó selecionada aleatóriamente tenha grau **k**. Como $p_k$ é uma probabilidade, ele deve ser normalizado:

**$$
\sum_{k=1}^{\infty}{p_k} = 1$$**

**$$
p_k = \frac{N_k}{N}$$**

onde $N_k$ é o número de nós com grau k.

**$$
\left<k \right> = \sum_{k=1}^{\infty}{kp_k} $$**

### 2.4 Matriz de Adjacência

Um grafo pode ser representado por uma matriz de adjacência, com as seguintes propriedade:

* **$A_{ij} = 1$** se existe um link apontando do nó $j$ para o nó $i$
* **$A_{ij} = 0$** se não existe um link apontando do nó $j$ para o nó $i$


Somar os valores de uma linha $i$ desta matriz retorna o grau de entrada do nó $i$, o oposto ocerre ao somar as linhas de uma coluna $j$.

### 2.5 Rede Reais são Esparsas

Em uma rede com $N$ nós o número total de links **$L \isin \set{0, L_{max}}$** onde

**$$
L_{max} = \binom{N}{2}$$**

Em redes reais $L$ é muito menor do que $L_{max}$

A aplicação prática deste fato é que, quando queremos guardar as informações de um grafo no computador, não precisamos armazenar toda a matriz de adjacência, mas sim apenas os valores onde $A_{ij} \neq 0$.

### 2.6 Redes com Pesos

**$$
A_{ij} = w_{ij}$$**

### 2.7 Grafos Bipartidos

Um grafo pe bipartido quando seus nós podem ser divididos em dois conjuntos diferentes $U$ e $V$, onde os nós do conjunto $U$ não ligam entre si, e os do conjunto $V$ também seguem esta regra.  


### 2.8 Caminhos e Distancias
