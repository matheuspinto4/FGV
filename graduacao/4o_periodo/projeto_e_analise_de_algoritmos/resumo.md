# Projeto e Análise de Algoritmos

## Notação Assintótica

### Objetivo

Discutir como avaliar a complexidade e apresentar a **notação assintótica** como solução para analisar e comparar algoritmos

### Definições

- O que é um **algoritmo**?
  - É uma **sequência de passos** que podem ser **computados** com o objetivo de **solucionar um problema**.


- Um **problema** pode apresentar mais de uma solução


- A **entrada de um algoritmo** é o conjunto de dados submetidos à uma execução do mesmo

- A **saída de um algoritmo** é o conjunto de dados resultantes de uma execução.

### Análise da Complexidade

Podemos definir a ocmplexidade de um determinado algoritmo através de uma função como:

$$
T(n) = \text{número de instruções} \\
\text{executadas considerando} \\ 
\text{a intância que exercita o} \\
\text{pior caso}
$$

### Notação Assintótica

#### Motivação

Determinar **com precisão** a função que descreve a complexidade de um algoritmo pode ser uma tarefa difícil e muito trabalhosa

- A **ordem assintótica de crescimento** de $T(n)$ é definida encontrando as funções que descrevem os **limites superior e inferior** de $T(n)$

#### Notação O:

**$T(n)$** pertence ao conjunto **$O(f(n))$** se existirem constantes positivas **$c$** e **$n_0$** tais que:

**$$
T(n) \le c f(n) \text{ }\forall \text{ }
 n \ge n_0$$**

#### Notação $\Omega$:


**$T(n)$** pertence ao conjunto **$\Omega(f(n))$** se existirem constantes positivas **$c$** e **$n_0$** tais que:

**$$
c f(n) \le T(n)\text{ }\forall \text{ }
 n \ge n_0$$**


#### Notação $\Theta$:

$T(n)$ pertence ao conjunto $\Theta(f(n))$ se $T(n)$ for $O(f(n))$ e $\Omega(f(n))$

## Recorrências

### Objetivo

  Apresentar **recorrêcnias** como solução para avaliar a complexidade de **algoritmos recursivos** e técnicas para resolvê-las

### Métodos
- **Substituição**
- **Árvore de recursão**
- **Iteração**
- **Mestre**

#### Substituição
O método se baseia em dar um hipótese de indução e tentar provar ela.

$$
T(n) = T(n/2) + n \\
T(n) \le cn\log(n) \text{ hipótese} \\
T(n/2) \le c\frac{n}{2}\log(\frac{n}{2}) \\
T(n) \le cn\log(n)
$$

#### Árvore de Recursão

No método se somam sa complexidades de cada nó da árvore.


#### Método da Iteração

Se expande a expressão e tenta resolver.

#### Método Mestre

**$$
T(n) = aT(\frac{n}{b}) + f(n)$$**


Temos 3 casos:

1. Se $f(n) = O(n^{\log_b{a-\epsilon}})$ for some constant $\epsilon > 0$, then $T(n) = \Theta(n^{\log_ba})$

\

2. Se $f(n) = \Theta(n^{\log _b a})$, then $T(n) = \Theta(n^{\log_ba}\lg n)$

\

3. Se $f(n) = \Omega(n^{\log_ba + \epsilon})$ for some constant $\epsilon > 0$, and if $af(n/b) \le cf(n)$ for some constant $c < 1$ and all sufficiently large $n$, then $T(n) = \Theta(f(n))$


## Algoritmos de Busca

### Busca em Vetor Ordenado

Complexidade: $O(\log n)$
```C
int search(int v[], int leftInx, int rightInx, int x)
{
    int midInx = (leftInx + rightInx) / 2;
    int midValue = v[midInx];
    if (midValu == x) return midInx;
    if (leftInx >= rightInx) return -1;
    if (x > midValue)
    {
        return search(v, midInx + 1, rightInx, x);
    } else
    {
      return search(v, leftInx, midInx - 1, x);
    }
}
```

## Tabelas de Dispersão

