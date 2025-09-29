from typing import List, Tuple

def problema_1(eventos: List[Tuple[int, int]]) -> Tuple[int, Tuple[int, int]]:
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


def problema_2(sabores: List[int]) -> int:
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
            

def problema_3(estadias: List[Tuple[int, int]]) -> Tuple[int, List[int]]:
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


def problema_4(A: List[int], k: int) -> Tuple[int, int, int, int]:
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

        

def problema_5(blocos: List[int]) -> int:
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


def problema_6(A: List[int], k: int) -> int:
    
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


def problema_7(A: List[int]) -> int:
    
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


def test_1():
    lista1 = [(5, 8), (2, 4), (3, 9)]
    lista2 = [(5, 8), (2, 6), (3, 9)]
    print(problema_1(lista1))
    print(problema_1(lista2))

def test_2():
    sabores = [1, 2, 1, 4]
    print(problema_2(sabores=sabores))
    sabores = [11, 22, 11, 33, 22, 77, 44, 22]
    print(problema_2(sabores=sabores))
    sabores = [3,3,3,3,3,3,3]
    print(problema_2(sabores=sabores))

def test_3():
    l = [(1, 2), (3, 3), (4, 5)]
    print(problema_3(l))
    l = [(2, 4), (1, 2), (4, 4)]
    print(problema_3(l))
    l = [(1, 2), (2, 4), (4, 4)]
    print(problema_3(l))
    l = [(1, 4), (1, 2), (2, 4)]
    print(problema_3(l))
    

def test_4():
    A =[3, 2, 6, 1]
    k = 7
    print(problema_4(A, k))
    A = [3, 2, 6, 1]
    k = 12
    print(problema_4(A, k))
    A =[3, 2, 5, 8, 1, 3, 2, 3]
    k = 15
    print(problema_4(A, k))

def test_5():
    l = [1, 2, 1, 4] #3 [1, 1], [2], [4]
    print(problema_5(l))
    l = [11, 22, 11, 33, 22, 77, 44, 22]# 4 [11, 11], [22, 22, 22], [33], [77, 44]
    print(problema_5(l))
    l = [3, 3, 3, 3, 3, 3]# 1 [3, 3, 3, 3, 3, 3]
    print(problema_5(l))


def test_6():
    A = [3, 2, 6] 
    k = 7
    print(problema_6(A, k), f"Esperado = {8}") 

    A = [3, 2, 6, 5, 8, 2, 1] 
    k = 1234
    print(problema_6(A, k), f"Esperado = {438}") 
    testes = [
    ([3, 2, 6], 7, 8),                      # Teste 1: Básico
    ([3, 2, 6, 5, 8, 2, 1], 1234, 438),     # Teste 2: Alvo alto, vários períodos
    ([100, 100], 5, 300),                   # Teste 3: Máquinas idênticas
    ([10], 1000, 10000),                    # Teste 4: Uma única máquina
    ([1, 1000000000], 10, 10),              # Teste 5: Um planeta muito rápido
    ([1000000000, 1000000000, 1000000000], 3, 1000000000), # Teste 6: Ai = 10^9
    ([2, 3, 5, 7], 10000, 8504),           # Teste 8: Primos e alvo grande
    ]

    print("--- Testes do 'Grande Sistema Planetário' ---")
    print("-" * 50)

    for i, (A, k, esperado) in enumerate(testes, 1):
        resultado = problema_6(A, k)
        status = "OK" if resultado == esperado else "FALHOU"
        
        # Formatação para lidar com números grandes
        A_formatado = f"[...{len(A)} valores...]" if len(str(A)) > 50 else str(A)

        print(f"Teste {i}:")
        print(f"  A (Períodos): {A_formatado}")
        print(f"  k (Alvo): {k:,}")
        print(f"  -> Resultado: {resultado:,} | Esperado: {esperado:,} [{status}]")
        print("-" * 50)
    

def test_7():
    A = [3, 2, 6, 1] 
    print(problema_7(A))
    A = [3, 2, 5, 8, 1, 3, 2, 3] 
    print(problema_7(A))
    A = [33, 10] 
    print(problema_7(A))


