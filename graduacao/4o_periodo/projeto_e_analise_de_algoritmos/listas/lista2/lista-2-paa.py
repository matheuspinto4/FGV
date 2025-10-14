from typing import List, Tuple

############ Atenção ################
# Não altere a assinatura das funções.
# Não altere a classe TreeNode.
# Você pode criar outras funções ou classes se julgar necessário, mas deve defini-las no corpo da função do exercicio.

# ==============================================================================
# Problema de exemplo
# ==============================================================================
def problema_0(A: List[int]) -> List[bool]:
    """
    Recebe uma lista de inteiros e retorna uma lista de booleanos
    indicando se cada numero é primo em tempo O(n * sqrt(maxval)).
    """
    def eh_primo(n: int) -> bool:
        if n==2:
            return True
        if n <= 1 or n%2==0:
            return False
        
        # Iterando apenas nos impares para diminuir a constante
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True

    resultado = []
    for num in A:
        resultado.append(eh_primo(num))

    return resultado


# ==============================================================================
# Problema 1 - A Biblioteca de Alexandria
# ==============================================================================

def problema_1(eventos: List[Tuple[int, int]]) -> Tuple[int, Tuple[int, int]]:
    """
    A administração da biblioteca busca compreender o padrão de uso de seus
    frequentadores e, para isso, precisa identificar o período de pico, ou
    seja, o intervalo de tempo em que há o maior número de usuários presentes.

    O algoritmo deverá receber $n$ pares de inteiros $(a, b)$, onde $a$
    representa o horário de entrada e $b$ o de saída de um usuário. Como
    resultado, ele deve retornar $k, (u, v)$, onde $k$ é a quantidade
    máxima de pessoas na biblioteca e $(u, v)$ é o intervalo de tempo
    maximal (de maior tamanho) correspondente a esse pico. Se houver mais
    de um intervalo de pico maximal, retorne aquele com menor $u$.

    O algoritmo deve ter tempo de execução $O(n \log n)$.
    """
    eventos_entrada_saida = []
    for e in eventos:
        eventos_entrada_saida.append((e[0], 1))
        eventos_entrada_saida.append((e[1], -1))
    eventos_entrada_saida.sort()

    contagem_max = 0
    contagem = 0
    melhor_intervalo = (0,0)
    intervalo = (0,0)
    inicio = -1
    for e in eventos_entrada_saida:
        tempo, valor = e
        
        contagem += valor

        # Contagem > contagem_max => novo pico se inicia aqui, então o início do melhor intervalo é este agora:
        if contagem > contagem_max:
            melhor_intervalo = (tempo, tempo)
            intervalo = (tempo, tempo)
            inicio = tempo
            contagem_max = contagem

        # A contagem é a mesma que o maior, então temos duas opções: novo pico ou o pico continua.
        elif contagem == contagem_max:
            if inicio != -1: # Pico continua
                intervalo = (intervalo[0],tempo) 
            else: # Novo pico
                intervalo = (tempo, tempo)
                inicio = tempo
            
            if intervalo[1] - intervalo[0] > melhor_intervalo[1] - melhor_intervalo[0]:
                melhor_intervalo = intervalo
                
        elif contagem < contagem_max:
            if inicio != -1:
                intervalo = (intervalo[0], tempo)
                if intervalo[1] - intervalo[0] > melhor_intervalo[1] - melhor_intervalo[0]:
                    melhor_intervalo = intervalo
            inicio = -1

    return contagem_max, melhor_intervalo


# ==============================================================================
# Problema 2 - Sisi e a Sorveteria
# ==============================================================================

def problema_2(sabores: List[int]) -> int:
    """
    Sisi quer saber qual foi o período mais longo, em dias consecutivos, que
    ela passou sem repetir um único sabor de sorvete.

    Você deve desenvolver um algoritmo com tempo de execução $O(n)$ que receba
    a sequência de sabores consumidos e retorne o tamanho da maior
    subsequência contínua de valores distintos.
    """
    contagem_maxima = 0
    dicio = {}
    contagem = 0
    inicio_janela = 0
    for i, sabor in enumerate(sabores):
        if sabor in dicio and dicio[sabor] >= inicio_janela:
            inicio_janela = dicio[sabor] + 1

        contagem = i - inicio_janela + 1
        dicio[sabor] = i
        contagem_maxima = max(contagem_maxima, contagem)

    return contagem_maxima


# ==============================================================================
# Problema 3 - Hotel de Hilbert
# ==============================================================================

def problema_3(estadias: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
    """
    O Grande Hotel de Hilbert receberá $n$ hóspedes. Para cada hóspede,
    conhecemos um par de inteiros $(a, b)$, que representam seu tempo de
    chegada e de partida, respectivamente. Para minimizar os custos, o
    gerente deseja utilizar o menor número possível de quartos. Duas pessoas
    podem ocupar o mesmo quarto, desde que o período de estadia delas não se
    sobreponha.

    O algoritmo deverá receber $n$ pares de inteiros $(a, b)$ e retornar
    $k, [r_1, r_2, \dots, r_n]$, onde $k$ é a quantidade mínima de quartos
    necessários e $r_i$ é o quarto que o i-ésimo hóspede (na mesma ordem da
    entrada) deverá utilizar.

    O algoritmo deve ter tempo de execução $O(n \log n)$.
    """
    eventos_entrada_saida = []
    for index, e in enumerate(estadias):
        eventos_entrada_saida.append((e[0], 1, index))
        eventos_entrada_saida.append((e[1], -1, index))
    eventos_entrada_saida.sort(key=lambda x:(x[0], -x[1]))
    dicio = {}
    total_max = -1
    total = 0
    num_quartos_ocupados = 0
    quartos_desocupados = [1]
    lista_ocupacoes = [0] * len(estadias)
    for e in eventos_entrada_saida:
        tempo, valor, index = e
        
        total += valor
        if total >= total_max:
            total_max = total

        if valor == 1: # Pessoa acabou de entrar no hotel
            if len(quartos_desocupados) != 0: # Há um quarto desocupado na lista
                num_quarto = quartos_desocupados[-1]
                dicio[index] = num_quarto
                lista_ocupacoes[index] = num_quarto
                num_quartos_ocupados += 1
                quartos_desocupados.pop()
            else: # Não há quartos disponíveis, então se cria mais um
                num_quarto = num_quartos_ocupados + 1
                num_quartos_ocupados += 1
                dicio[index] = num_quarto 
                lista_ocupacoes[index] = num_quarto

        else: # Pessoa está saindo do hotel
            num_quarto = dicio[index]
            quartos_desocupados.append(num_quarto)
            num_quartos_ocupados -= 1
    
    return total_max, lista_ocupacoes


# ==============================================================================
# Problema 4 - Quadra
# ==============================================================================

def problema_4(A: List[int], k: int) -> Tuple[int, int, int, int]:
    """
    Dado um vetor $A$ com $n$ inteiros e um valor alvo $k$, encontre quatro
    índices distintos cuja soma dos elementos seja igual a $k$.

    O algoritmo deve retornar uma tupla com os quatro índices em ordem
    crescente, $(a, b, c, d)$ com $a<b<c<d$, que satisfaça a condição
    $A_a + A_b + A_c + A_d = k$.

    Caso existam múltiplas soluções, retornar qualquer uma delas é suficiente.
    Se nenhuma combinação válida for encontrada, o algoritmo deve retornar
    (-1, -1, -1, -1).

    O algoritmo deve ter uma complexidade de tempo de $O(n^2 \log n)$.
    """
    somas = []
    for i in range(len(A)):
        for j in range(i+1, len(A)):
            somas.append((A[i] + A[j], i, j))

    somas.sort()
    
    for indice, s in enumerate(somas):
        comp = k - s[0]
        inicio = indice
        fim = len(somas) - 1
        while (inicio <= fim):
            meio = (fim + inicio) // 2
            s2 = somas[meio]
            if s2[0] == comp and len({s[1], s[2], s2[1], s2[2]}) == 4: 
                return tuple(sorted((s[1] + 1, s[2] + 1, s2[1] + 1, s2[2] + 1)))
            
            if s2[0] < comp:
                inicio = meio + 1
            else:
                fim = meio - 1
    
    return (-1,-1,-1,-1)


# ==============================================================================
# Problema 5 - Os blocos
# ==============================================================================

def problema_5(blocos: List[int]) -> int:
    """
    Você recebeu $n$ blocos de madeira e seu desafio é empilhá-los, formando
    o menor número possível de torres, seguindo duas regras:
    1. Um bloco só pode ser colocado sobre outro se o seu tamanho for menor ou
       igual ao do bloco inferior.
    2. Os blocos devem ser processados um a um, na sequência predefinida em
       que são apresentados.

    A cada bloco, você deve decidir se o coloca no topo de uma torre existente
    ou se inicia uma nova torre com ele. O algoritmo deve encontrar o número
    mínimo de torres necessárias com complexidade $O(n \log n)$.
    """
    topos = [blocos[0]]

    for bloco in blocos:
        indice_ideal = None
        inicio = 0
        fim = len(topos) - 1

        while(inicio <= fim):
            meio = (fim + inicio) // 2
            if (topos[meio] == bloco): 
                indice_ideal = meio
                break

            if (topos[meio] < bloco):
                inicio = meio + 1
            else: 
                indice_ideal = meio
                fim = meio - 1

        if indice_ideal == None:
            topos.append(bloco)

        else:
            topos[indice_ideal] = bloco

    total = len(topos)    
    return total


# ==============================================================================
# Problema 6: O Grande Sistema Planetário
# ==============================================================================

def problema_6(A: List[int], k: int) -> int:
    """
    Dado um conjunto de períodos orbitais $A_1, A_2, \dots, A_n$ e um número
    alvo de voltas $k$, encontre o menor número inteiro de anos, $T$, no qual
    a soma total de órbitas completadas por todos os $n$ planetas do sistema
    seja maior ou igual a $k$.

    A complexidade esperada é de $O(n \cdot \log(M))$, onde $M$ é a maior
    resposta possível.
    """
    def soma(A, tempo):
        total = 0
        for valor in A:
            total += tempo // valor
        return total

    inicio = 0
    fim = int(10 ** 18)
    resposta = fim

    while inicio <= fim:
        meio = inicio + (fim - inicio) // 2
        val = soma(A, meio)

        if val >= k:
            resposta = meio
            fim = meio - 1
        else:
            inicio = meio + 1
    
    return resposta


# ==============================================================================
# Problema 7: Otimização
# ==============================================================================

def problema_7(A: List[int]) -> int:
    """
    Dado um vetor $A$ com $n$ inteiros, projete um algoritmo linear que retorna
    o menor valor inteiro $k$ que minimiza a soma:
    $$ \sum_{i=1}^{n} |A_i-k| $$
    A complexidade de tempo deve ser $O(n)$.
    """
    def select_kth(arr, k):
        if len(arr) <= 10:
            return sorted(arr)[k]

        medians = [sorted(arr[i:i+5])[len(arr[i:i+5])//2] for i in range(0, len(arr), 5)]
        pivot = select_kth(medians, len(medians)//2)

        less = [x for x in arr if x < pivot]
        equal = [x for x in arr if x == pivot]
        greater = [x for x in arr if x > pivot]

        if k < len(less): return select_kth(less, k)
        if k < len(less) + len(equal): return pivot
        return select_kth(greater, k - len(less) - len(equal))

    median_pivot = select_kth(A, (len(A) - 1) // 2)
    return median_pivot