from typing import List, Optional

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


# Estrutura de nó para o exercício de árvore
class TreeNode:
    """
    Classe para representar um nó de uma árvore binária.
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ==============================================================================
# Problema 6
# ==============================================================================

def problema_6(raiz: Optional[TreeNode]) -> int:
    """
    Dada uma árvore binária de busca (BST) T com $n$ nós contendo inteiros, projete
    um algoritmo que encontre a menor diferença absoluta entre dois nós diferentes 
    da árvore. O algoritmo deve ter complexidade $O(n)$ no pior caso.
    """
    head = TreeNode(val=float('-inf'))

    def inserir_em_lista(node):  # Pior caso: precisa percorrer n-1 elementos
        atual = head
        while (atual.right and atual.right.val < node.val):
            atual = atual.right

        node.right = atual.right
        if atual.right:
            atual.right.left = node

        atual.right = node
        node.left = atual

    def percorrer_arvore(node):
        """
        Percorre toda a árvore, passando por cada elemento
        uma vez: n vezes
        """
        if node is None:
            return

        inserir_em_lista(TreeNode(node.val))
        percorrer_arvore(node.left)
        percorrer_arvore(node.right)

    percorrer_arvore(raiz)  # O(n)
    atual = head.right
    min = float('inf')
    while atual.right:  # O(n) percorre toda a lista de n elementos
        if abs(atual.right.val - atual.val) < min:
            min = atual.right.val - atual.val
        atual = atual.right

    return min

# ==============================================================================
# Problema 7
# ==============================================================================

def problema_7(A: List[int]) -> List[int]:
    """
    Desenvolva um algoritmo $O(n)$ que particiona um array $A$ em números pares e ímpares. 
    O algoritmo deve terminar com A contendo todos os seus elementos pares precedendo todos 
    os seus elementos ímpares. A solução deve ser um algoritmo in-place, o que significa que 
    ele pode usar apenas um espaço de memória constante além do próprio $A$. Na prática, 
    isso significa que você não pode usar outro array auxiliar.
    """
    j = 0
    for k in range(len(A)):
        if A[k] % 2 == 0:  # Par
            if A[j] % 2 != 0:
                temp = A[j]
                A[j] = A[k]
                A[k] = temp
            j += 1
    return A
# ==============================================================================
# Problema 8
# ==============================================================================

def problema_8_a(A: List[int], k: int) -> int:
    """
    Dado um inteiro k e uma lista A que contém n inteiros, projete um algoritmo 
    que retorne a quantidade de pares de inteiros em A cuja soma seja k. 
    Mais especificamente, retorne a quantidade de pares $(i,\, j)$ com $i<j$, 
    tal que $A_i + A_j = k$

    Projete o algoritmo com complexidade de execução $O(n)$
    """
    dicio = {}
    total = 0

    for n in A:

        complemento = k - n
        if (complemento) in dicio:
            total += dicio[complemento]

        dicio[n] = dicio.get(n, 0) + 1

    return total

def problema_8_b(A: List[int], k: int) -> int:
    """
    [...]
    Agora assuma que A esteja ordenado ($A_i\le A_j \ \forall \ i<j$), projete 
    o algoritmo com complexidade de execução $O(n \log n)$ e complexidade de 
    espaço $O(1)$
    """
    A.sort() # Ignorar esta parte, foi feito somente para garantir 
             # a análise  com um array ordenado

    left = 0
    right = len(A) - 1
    total = 0
    while(left < right):
        if (A[right] + A[left] < k):
            left += 1

        elif (A[right] + A[left] > k): 
            right -= 1

        else:
            cont1 = 0
            cont2 = 0
            ele1 = A[left]
            ele2 = A[right]
            while(left <= right and A[left] == ele1):
                cont1 += 1
                left += 1
            while(left <= right and A[right] == ele2):
                cont2 += 1
                right -= 1

            if ele1 == ele2:
                total += (cont1 * (cont1 - 1)) // 2
            else:
                total += cont1 * cont2

    return total

def problema_8_c(A: List[int], k: int) -> int:
    """
    [...]
    Novamente assumindo que A está ordenado, projeto o algoritmo com complexidade 
    de execução $O(n)$ e complexidade de espaço $O(1)$
    """
    A.sort() # Ignorar esta parte, foi feito somente para garantir 
             # a análise  com um array ordenado

    left = 0
    right = len(A) - 1
    total = 0
    while(left < right):
        if (A[right] + A[left] < k):
            left += 1

        elif (A[right] + A[left] > k): 
            right -= 1

        else:
            cont1 = 0
            cont2 = 0
            ele1 = A[left]
            ele2 = A[right]
            while(left <= right and A[left] == ele1):
                cont1 += 1
                left += 1
            while(left <= right and A[right] == ele2):
                cont2 += 1
                right -= 1

            if ele1 == ele2:
                total += (cont1 * (cont1 - 1)) // 2
            else:
                total += cont1 * cont2

    return total
