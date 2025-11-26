import heapq
from math import sqrt
from typing import List, Tuple, Optional
from collections import deque


"""
QUESTÃO 1
"""
class Sensor:
    def __init__(self, id: int, x: float, y: float, r: float):
        self.id = id
        self.x = x
        self.y = y
        self.r = r

def question_1(sensors: List[Sensor], s_i: int, s_f: int) -> list:
    """
    Uma organização ambiental desenvolveu um sistema para monitoramento de florestas
    cuja comunicação é baseada em uma rede de sensores sem fio. Um sensor A consegue
    enviar uma mensagem para um sensor B diretamente se a distância entre eles for
    menor ou igual ao raio de transmissão de A. Dado um conjunto de sensores S, em
    que cada elemento s possui uma localização (s.x,s.y) e um raio de transmissão s.r
    em metros, projete um algoritmo capaz de calcular a rota para transmitir uma
    mensagem entre s_i e s_f através dos sensores da rede, de forma que percorra a
    menor distância possível em metros. O algoritmo deve retornar uma sequência de
    sensores representando o caminho completo que a mensagem irá percorrer: primeiro
    os sensores utilizados para enviar a requisição de s_i até s_f, e em seguida os
    sensores utilizados para enviar a resposta de s_f até s_i. Caso não seja possível
    estabelecer a comunicação, o algoritmo deve retornar None.

    Exemplo:
        Entrada:
            sensors = [
                Sensor(0, 0.0, 0.0, 30.0),
                Sensor(1, 25.0, 0.0, 25.0),
                Sensor(2, 50.0, 0.0, 30.0),
                Sensor(3, 15.0, 20.0, 35.0),
                Sensor(4, 35.0, 25.0, 25.0),
                Sensor(5, 75.0, 10.0, 15.0),
                Sensor(6, 70.0, 20.0, 20.0),
                Sensor(7, 55.0, 25.0, 25.0)
            ]
            s_i = 0
            s_f = 5

        Saída: [0, 1, 2, 5, 6, 7, 4, 3, 0]

    ESPACO DO ALUNO:
    <Descrever aqui informações adicionais>
    """
    pass


"""
QUESTÃO 2
"""
def question_2(graph: list[list[int]], n: int, vi: int, vj: int) -> bool:
    """
    Considere um grafo G=(V,E) conexo e não-dirigido. Dizemos que uma aresta e∈E é uma
    ponte se a sua remoção produzir um grafo G’ não-conexo.
    a) Se existir uma aresta e=(v_i,v_j) que não é uma ponte podemos afirmar que existe
       um ciclo em G que contém os vértices v_i e v_j. Por que?
	b) Projete um algoritmo que receba uma aresta e=(v_i,v_j) e determina se a mesma é
	   uma ponte em O(V+E).

	Exemplo:
        Entrada:
            n = 5
            graph = [[] for _ in range(n)]
            edges = [(0, 1), (0, 3), (1, 2), (1, 4), (3, 4)]
            for u, v in edges:
                graph[u].append(v)
                graph[v].append(u)

        Saída:
            (1,2) -> True
            (4,3) -> False
            (0,1) -> False

    ESPACO DO ALUNO:
    a)  <escreva a resposta aqui>
    """
    #  Podemos realizar uma BST iniciando no nó v_i num subgrafo de G sem a aresta (v_i, v_j).
    #  Caso a distância de v_i à v_j seja diferente de infinito, então a aresta (v_i, v_j) não é uma ponte


    #  Criando um subgrafo:
    sub_G = graph.copy()
    sub_G[vi].remove(vj)
    sub_G[vj].remove(vi)
    
    #  BST:
    queue = deque([vi])
    visitados = set()
    while queue:
        u = queue.popleft()
        visitados.add(u)
        for v in sub_G[u]:
            if v not in visitados:
                queue.append(v)
    if vj in visitados: return False
    else: return True
"""
QUESTÃO 3
"""
class Task:
    def __init__(self, start, end, value, name):
        self.start = start
        self.end = end
        self.value = value
        self.name = name

def question_3(tasks: list[Task]) -> tuple[int, list[Task]]:
    """
    Considere o problema de agendamento de tarefas: dado o conjunto de tarefas T={t_1,..,t_n} com
    n elementos, cada uma com um tempo de início t_k.start, um tempo de término t_k.end, e um valor
    t_k.value, encontre o subconjunto de tarefas S ⊆ T que pode ser alocado sem sobreposição temporal
    de forma que a soma do valor das tarefas em S seja máximo.
	a) Projete um algoritmo (auxiliar) que receba como parâmetro uma tarefa e retorne a tarefa anterior
	   compatível (ou seja, que pode ser alocada sem sobreposição temporal) com o tempo de término mais
	   próximo.
	b) Projete um algoritmo para agendamento de tarefas que produza sempre a solução ótima, utilizando
	   o algoritmo auxiliar criado em (a). O algoritmo deverá respeitar as características descritas no
	   enunciado acima.
	c) Qual técnica de projeto você utilizou para projetar o algoritmo de (b)?
    d) Analise a complexidade do algoritmo e justifique a sua resposta.

    Exemplo:
        Entrada:
            tasks = [
                Task(1, 3, 50, "A"),
                Task(4, 6, 30, "B"),
                Task(7, 9, 30, "C"),
                Task(2, 5, 20, "D"),
                Task(5, 7, 40, "E"),
                Task(6, 8, 60, "F"),
            ]

        Saída: ['A', 'B', 'F']

    ESPACO DO ALUNO:
    c) <escreva a resposta aqui>
    d) <escreva a resposta aqui>
    """
    #  (a)
    def previous_compatible(tasks, j):
        #  Supõe que tasks está ordenado pelo tempo de término de forma crescente 
        for i in reversed(range(len(tasks))):
            if tasks[i].end <= tasks[j].start:  #  Foi achado a tarefa antecessora mais proxima da tarefa j
                return i
        return -1
        
    #  (b) 
    #   Podemos ordenar a lista com base nesse critério: valor * end;
    #   Para cada valor, começando do final até atingir o valor -1, iremos adicionar ele na lista e realiza a contagem
    tasks.sort(key=lambda x: x.end * x.value)
    seq = []
    cont = 0
    j = len(tasks)-1
    while j != -1:
        cont += tasks[j].value
        seq.append(tasks[j].name)
        j = previous_compatible(tasks, j)
    
    print(cont, seq)
    return (cont, seq)


"""
QUESTÃO 4
"""
def question_4() -> None:
    """
    Para cada uma das afirmações abaixo indique se é verdadeira (V) ou falsa (F):

    ESPACO DO ALUNO:
    ( ) Se um problema A pode ser reduzido a um problema B em tempo polinomial, e B
        está em P, então A também está em P.
    ( ) Todo problema NP-Difícil é necessariamente NP-Completo.
    ( ) Se encontrarmos um algoritmo polinomial para um problema NP-Completo, isso
        prova que P = NP.
    ( ) Se tivermos um problema A que é NP-Completo e um problema B que é NP-Difícil,
        e A pode ser reduzido a B em tempo polinomial, então B é necessariamente
        NP-Completo.
    ( ) Um problema pode ser simultaneamente NP-Completo e estar em P apenas se P = NP.
    """
    pass


def test_3():
    tasks = [
                Task(1, 3, 50, "A"),
                Task(4, 6, 30, "B"),
                Task(7, 9, 30, "C"),
                Task(2, 5, 20, "D"),
                Task(5, 7, 40, "E"),
                Task(6, 8, 60, "F"),
            ]

    question_3(tasks)


def test_2():
    n = 5
    graph = [[] for _ in range(n)]
    edges = [(0, 1), (0, 3), (1, 2), (1, 4), (3, 4)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    print(question_2(graph, n, 0, 1))
test_2()