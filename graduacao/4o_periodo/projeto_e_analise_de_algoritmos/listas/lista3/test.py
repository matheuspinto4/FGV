from lista_3_paa import *

def aux(args, resposta_esperada, problema):
        Q = problema(*args)
        print(f"Resposta Obtida: {Q}")
        print(f"Resposta esperada: {resposta_esperada}")
        print('-'*50)
def test_1():


    n = 5
    A = [1, 2, 1, 3, 6] 
    aux((n, A), 10, problema_1)
    n = 5
    A = [3, 2, 5, 4, 10] 
    aux((n, A), 20, problema_1)
    n = 4
    A = [2, 2, 2, 2]
    aux((n, A), 3, problema_1)
    n = 4
    A = [2, 1, 2, 1]
    aux((n, A), 1, problema_1)


def test_2():
    n = 2;
    k = 2
    C1 = 1 
    C2 = 2 
    A = [1, 3]
    r= 6
    aux((n , k, C1, C2, A), r, problema_2)
    n = 3;
    k = 2
    C1 = 1 
    C2 = 2 
    A = [1, 7]
    r= 8
    aux((n , k, C1, C2, A), r, problema_2)
    # A função 'aux' é um placeholder para sua função de teste
    # (ex: def aux(inputs, expected_result, function_to_test): assert function_to_test(*inputs) == expected_result)

    # ==============================================================================
    # 1. Caso Base: Sem Buracos (Apenas custo C1)
    # L = 2^5 = 32. Dividir: C1 + C1 = 200. Consertar: C1 = 100. Min é 100.
    # ==============================================================================
    n = 5;
    k = 0
    C1 = 100 
    C2 = 2 
    A = []
    r = 100
    aux((n , k, C1, C2, A), r, problema_2)

    # ==============================================================================
    # 2. Caso Base: Comprimento 1 (n=0)
    # L = 1. Não pode dividir. Custo: C2 * k * L = 5 * 1 * 1 = 5.
    # ==============================================================================
    n = 0;
    k = 1
    C1 = 10 
    C2 = 5 
    A = [1]
    r = 5
    aux((n , k, C1, C2, A), r, problema_2)

    # ==============================================================================
    # 3. Caso Lógica: Exemplo Padrão (Divisão Vantajosa)
    # O exemplo fornecido na descrição do problema.
    # ==============================================================================
    n = 2;
    k = 2
    C1 = 1 
    C2 = 2 
    A = [1, 3]
    r = 6
    aux((n , k, C1, C2, A), r, problema_2)

    # ==============================================================================
    # 4. Caso Lógica: Buracos Juntos (Teste de Concentração)
    # L = 4. Split: [1,2] tem 2 buracos (custo 4). [3,4] tem 0 (custo 1). Total 5.
    # ==============================================================================
    n = 2;
    k = 2
    C1 = 1 
    C2 = 2 
    A = [1, 2]
    r = 5
    aux((n , k, C1, C2, A), r, problema_2)

    # ==============================================================================
    # 5. Caso Lógica: Teste de Ordenação (Entrada Desordenada)
    # Idêntico ao caso 4, mas com A desordenado para verificar se o sorted() funciona.
    # ==============================================================================
    n = 2;
    k = 2
    C1 = 1 
    C2 = 2 
    A = [2, 1]
    r = 5
    aux((n , k, C1, C2, A), r, problema_2)

    # ==============================================================================
    # 6. Caso Lógica: C1 Caro (Força a minimizar segmentos vazios)
    # L = 8. O segmento [4, 4] vazio tem custo C1=1000. Isso força o algoritmo a dividir 
    # o máximo possível em segmentos com buracos (custo total 8).
    # ==============================================================================
    n = 3;
    k = 7
    C1 = 1000 
    C2 = 1 
    A = [1, 2, 3, 5, 6, 7, 8]
    r = 8
    aux((n , k, C1, C2, A), r, problema_2)

    # ==============================================================================
    # 7. Caso Lógica: O(k*log k) (Estrada Longa, Poucos Buracos)
    # L = 16. k=3. Os buracos estão concentrados. O custo mínimo é 24.
    # ==============================================================================
    n = 4;
    k = 3
    C1 = 10 
    C2 = 1 
    A = [1, 2, 3]
    r = 24
    aux((n , k, C1, C2, A), r, problema_2)


def test_3():
    n = 3
    A = [1, 2, 2]
    r = 6
    aux((n, A), r, problema_3)
    n = 1
    A = [1]
    r = 1
    aux((n, A), r, problema_3)
    n = 2
    A = [1, 2]
    r = 3
    aux((n, A), r, problema_3)
    n = 5
    A = [2, 2, 1, 5, 3]
    r = 7    
    aux((n, A), r, problema_3)
    # Caso 1: A "Pegadinha" do 4 na posição 3
    # Subsequências válidas:
    # Comp 1: [1], [2], [4], [4] (4 subs)
    # Comp 2: [1,2], [1,4], [1,4], [2,4], [2,4], [4,4] (6 subs)
    # Comp 3: [1,2,4]? Não, pois 4 não é divisível por 3.
    # Total: 10
    n = 4
    A = [1, 2, 4, 4]
    r = 10
    aux((n, A), r, problema_3)

    # Caso 2: Todos iguais, mas testando divisores
    # Comp 1: 4 subsequências (2|1 ok)
    # Comp 2: 6 subsequências (2|2 ok) -> C(4,2)
    # Comp 3: 0 subsequências (2 não é divisível por 3)
    # Comp 4: 0 subsequências (2 não é divisível por 4)
    # Total: 10
    n = 4
    A = [2, 2, 2, 2]
    r = 10
    aux((n, A), r, problema_3)

    # Caso 3: O caso do número máximo repetido (n=6)
    # O número 6 funciona nas posições 1, 2, 3 e 6. Falha nas posições 4 e 5.
    # Comp 1: C(6,1) = 6
    # Comp 2: C(6,2) = 15
    # Comp 3: C(6,3) = 20
    # Comp 4: 0 (6%4 != 0)
    # Comp 5: 0 (6%5 != 0)
    # Comp 6: C(6,6) = 1
    # Total: 6 + 15 + 20 + 1 = 42
    n = 6
    A = [6, 6, 6, 6, 6, 6]
    r = 41
    aux((n, A), r, problema_3)

    # Caso 4: Ordem decrescente (mais difícil de formar pares)
    # Apesar da ordem inversa, algumas combinações funcionam, como [5, 4] (4 na pos 2 ok), [5, 4, 3] (3 na pos 3 ok).
    # Total calculado pela PD: 10
    n = 5
    A = [5, 4, 3, 2, 1]
    r = 10
    aux((n, A), r, problema_3)

    # Caso 5: Sequência perfeita
    # [1], [2], [3], [4], [5]
    # [1,2], [1,3]...
    # Total: 12
    n = 5
    A = [1, 2, 3, 4, 5]
    r = 12
    aux((n, A), r, problema_3)

def test_4():
    problema_4(8)

def test_5():
    n=5; m=8; 
    grid=[['#', "#", "#", "#", "#", '#', '#', '#'],
           ['#', "A", ".", ".", "V", '.', '.', '#'],
           ['#', ".", "#", ".", "A", '#', '.', '#'],
           ['#', "A", "#", ".", ".", '#', '.', '.'],
           ['#', ".", "#", "#", "#", '#', '#', '#'],]
    r = 5
    aux((n, m, grid), r, problema_5)
    n=5; m=8; 
    grid = [['#', '#', '#', '#', '#', '#', '#', '#',],
           ['#', '.', '.', '.', 'V', '.', '.', '#',],
           ['#', '.', '#', '.', '.', '#', '.', '#',],
           ['#', '.', 'A', '.', '.', 'A', '.', '.',],
           ['#', '.', '#', '#', '#', '#', '#', '#',],]
    r = -1
    aux((n, m, grid), r, problema_5)
    n=5; m=8; 
    grid=[['#', "#", "#", "#", "#", '#', '#', '#'],
           ['#', "A", ".", ".", ".", '.', '.', '#'],
           ['#', ".", "#", ".", "A", '#', '.', '#'],
           ['#', "A", "#", ".", ".", '#', '.', 'V'],
           ['#', ".", "#", "#", "#", '#', '#', '#'],]
    r = 0
    aux((n, m, grid), r, problema_5)

    n=5; m=8; 
    grid=[['#', "#", "#", "#", "#", '#', '#', '#'],
      ['#', "V", ".", ".", ".", '.', '.', '.'],
      ['#', "#", "#", "#", "#", '#', '#', '#'],
      ['#', ".", "A", ".", ".", '#', '.', '#'],
      ['#', "#", "#", "#", "#", '#', '#', '#']]
    r=6
    aux((n, m, grid), r, problema_5)
    n=3; m=3
    grid = [
    ['#', '#', '#'],
    ['#', '.', '#'],  # Ponto isolado no meio (inalcançável)
    ['#', '#', '#']
    ]
    r=-1
    aux((n, m, grid), r, problema_5)
# V e A não existem (ou estão fora).
# Seu código fará float('inf') - float('inf') aqui.


def test_6():
    n = 3; m = 3; A = [(1, 2, 3), (2, 3, 1), (2, 1 ,10), (1, 3, 7)]; r = 2
    aux((n, m, A), r, problema_6)
    n = 3; m = 3; A = [(1, 2, 3), (2, 3, 3), (1, 3, 7)]; r = 3
    aux((n, m, A), r, problema_6)
    n = 4; m = 4; A = [(1, 2, 3), (2, 3, 3), (1, 3, 7), (3, 4, 10)]; r = 11
    aux((n, m, A), r, problema_6)


def test_7():
    n = 5; m = 6; A = [(1, 2, 3), (2, 3, 5), (2, 4, 2), (3, 4, 8), (5, 1, 7), (5, 4, 4)]; r = 14
    aux((n, m, A), r, problema_7)
    n = 5; m = 6; A = [(1, 2, 3), (2, 3, 5), (2, 4, 2), (3, 4, 0), (5, 1, 7), (5, 4, 4)]; r = 9
    aux((n, m, A), r, problema_7)
    n = 2; m = 1; A = [(1, 2, 0)]; r = 0
    aux((n, m, A), r, problema_7)


def test_8():
    n = 3; m = 2; A = [(1, 2), (2, 3)]; r = 1
    aux((n, m, A), r, problema_8)
    n = 5; m = 7; A = [(1, 3), (3, 4), (1, 2), (2, 5), (1, 4), (4, 5), (3, 5)]; r = 4
    aux((n, m, A), r, problema_8)
    n = 3; m = 2; A = [(1, 2), (3, 2)]; r=0
    aux((n, m, A), r, problema_8)

test_1()
test_2()
test_3()
test_4()
test_5()
test_6()
test_7()
test_8()