import numpy as np

# ==========================
# Exercícios Básicos
# ==========================

# 1. Criação de Arrays

# (a) Crie um array NumPy de 10 elementos com valores de 0 a 9.
arr1 = np.arange(10)
arr1a = np.arange(10)
print("1(a) Array de 0 a 9:", arr1)
# Resultado esperado: [0 1 2 3 4 5 6 7 8 9]
print()
# (b) Crie um array NumPy de números aleatórios entre 0 e 1 com shape (3,3).
arr2 = np.random.rand(3, 3)
arr2b = np.random.rand(4,4)
print("1(b) Matriz 3x3 de números aleatórios:\n", arr2)
# Resultado: matriz 3x3 com números aleatórios entre 0 e 1
print()
# (c) Crie um array com os números pares de 2 a 20.
arr3 = np.arange(2, 21, 2)
arr3b = np.arange(5, 40, 4)
print("1(c) Array de números pares:", arr3)
# Resultado esperado: [ 2  4  6  8 10 12 14 16 18 20]
print()
# 2. Indexação e Slicing

# (a) Extraia os elementos de índice ímpar de um array de 1D com 10 números.
arr4 = np.arange(10)
odd_indices = arr4[1::2]
print("2(a) Elementos de índice ímpar:", odd_indices)
# Resultado esperado: [1 3 5 7 9]

# (b) Crie uma matriz 3x3 e extraia a segunda coluna.
matrix3x3 = np.arange(1, 10).reshape(3, 3)
second_column = matrix3x3[:, 1]
print("2(b) Segunda coluna da matriz:", second_column)
# Resultado esperado: [2 5 8]

# (c) Inverta a ordem de um array NumPy sem usar [::-1].
reversed_arr = np.flip(arr4)
print("2(c) Array invertido:", reversed_arr)
# Resultado esperado: [9 8 7 6 5 4 3 2 1 0]

# 3. Operações Matemáticas

# (a) Crie dois arrays NumPy e faça operações element-wise.
arr5 = np.array([1, 2, 3])
arr6 = np.array([4, 5, 6])
sum_arr = arr5 + arr6
sub_arr = arr5 - arr6
mul_arr = arr5 * arr6
div_arr = arr5 / arr6
print("3(a) Soma:", sum_arr)  # [5 7 9]
print("3(a) Subtração:", sub_arr)  # [-3 -3 -3]
print("3(a) Multiplicação:", mul_arr)  # [4 10 18]
print("3(a) Divisão:", div_arr)  # [0.25 0.4 0.5]

# ==========================
# Exercícios Intermediários
# ==========================

# 4. Manipulação de Formato

# (a) Transforme um array 4x4 em shape (2,8).
arr7 = np.arange(16).reshape(4, 4)
reshaped_arr = arr7.reshape(2, 8)
print("4(a) Matriz reshaped:\n", reshaped_arr)
# Resultado esperado: matriz 2x8 com os mesmos valores

# (b) Empilhe dois arrays horizontal e verticalmente.
stacked_h = np.hstack((arr7, arr7))
stacked_v = np.vstack((arr7, arr7))
print("4(b) Empilhamento horizontal:\n", stacked_h)
print("4(b) Empilhamento vertical:\n", stacked_v)

# 5. Máscaras e Condições

# (a) Substitua valores negativos por zero.
arr8 = np.array([-1, 2, -3, 4, -5])
arr8[arr8 < 0] = 0
print("5(a) Array com negativos substituídos por 0:", arr8)
# Resultado esperado: [0 2 0 4 0]

# (b) Encontre todos os índices onde os valores são maiores que a média do array.
arr9 = np.array([10, 15, 8, 20, 25])
indices_maiores_que_media = np.where(arr9 > np.mean(arr9))
print("5(b) Índices dos elementos maiores que a média:", indices_maiores_que_media)
# Resultado esperado: (array([1, 3, 4]),)

# ==========================
# Exercícios Avançados
# ==========================

# 6. Álgebra Linear

# (a) Crie uma matriz 3x3 e calcule sua inversa.
matriz_A = np.array([[3, 1, 2], [2, 4, 1], [1, 2, 3]])
matriz_inversa = np.linalg.inv(matriz_A)
print("6(a) Matriz inversa:\n", matriz_inversa)

# (b) Resolva o sistema linear:
# 2x + y = 1
# x - y = 3
A = np.array([[2, 1], [1, -1]])
B = np.array([1, 3])
solucao = np.linalg.solve(A, B)
print("6(b) Solução do sistema (x, y):", solucao)
# Resultado esperado: x = 2, y = -1

# 7. Desafios NumPy

# (a) Crie uma matriz identidade de tamanho 6x6 sem usar np.eye().
identidade6x6 = np.zeros((6, 6))
np.fill_diagonal(identidade6x6, 1)
print("7(a) Matriz identidade 6x6:\n", identidade6x6)
# Resultado esperado: Matriz identidade 6x6

# (b) Gere um array de 1000 elementos com distribuição normal e verifique sua média e desvio padrão.
arr_normal = np.random.randn(1000)
media = np.mean(arr_normal)
desvio_padrao = np.std(arr_normal)
print(f"7(b) Média: {media:.4f}, Desvio padrão: {desvio_padrao:.4f}")
# Resultado esperado: Média próxima de 0, desvio padrão próximo de 1

# (c) Implemente um algoritmo de multiplicação de matrizes sem usar np.dot().
def matrix_multiplication(A, B):
    rows_A, cols_A = A.shape
    rows_B, cols_B = B.shape
    if cols_A != rows_B:
        raise ValueError("Número de colunas de A deve ser igual ao número de linhas de B")
    
    result = np.zeros((rows_A, cols_B))
    for i in range(rows_A):
        for j in range(cols_B):
            for k in range(cols_A):
                result[i, j] += A[i, k] * B[k, j]
    return result

A = np.array([[1, 2], [3, 4]])
B = np.array([[5, 6], [7, 8]])
resultado_multiplicacao = matrix_multiplication(A, B)
print("7(c) Multiplicação de matrizes:\n", resultado_multiplicacao)
# Resultado esperado:
# [[19 22]
#  [43 50]]
