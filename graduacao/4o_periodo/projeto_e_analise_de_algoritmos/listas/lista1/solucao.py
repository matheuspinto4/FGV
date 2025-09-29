class TreeNode:
    """
    Classe para representar um nó de uma árvore binária.
    """
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def problema_6(raiz):
    """winget search Microsoft.PowerShell
    Ideia:  Percorrer toda a árvore
            e ir criando uma lista ordenada da seguinte maneira:
                Para um dado nó atual, percorrer a lista
                até que um valor seja maior do que ele, adicionar
                logo na seguida deste valor.
                Podemos aproveitar a estrutura de nós já existente
                e criar uma lista encadeada.
            Por fim, percorre-se a lista encadeada, achando a
            menor diferença absoluta entre dois termos.
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


def problema_7(A):
    j = 0
    for k in range(len(A)):
        if A[k] % 2 == 0:  # Par
            if A[j] % 2 != 0:
                temp = A[j]
                A[j] = A[k]
                A[k] = temp
            j += 1
    return A


def problema_8_a(A, k):
    """
    Podemos adicionar os elementos em uma hashtable, Assim,
    iremos percorrer por todos os elementos da lista e ver se
    o complemento dele se encontra presente na hashtable e
    à contagem a frequência que este complemento já apareceu.
    """
    dicio = {}
    total = 0

    for n in A:

        complemento = k - n
        if (complemento) in dicio:
            total += dicio[complemento]

        dicio[n] = dicio.get(n, 0) + 1

    return total


def problema_8_b(A, k):
    """
    Podemos percorrer o array ordenado e, para cada valor dela, realizar
    uma busca binária pelo seu complemento no mesmo array. Ou seja, teremos
    O(nlog(n)) em complexidade de tempo e O(1) em complexidade de armazenamento
    """

    def busca_binaria(lista, inicio, fim, valor, contador=0):
        if inicio >= fim:
            return contador

        meio = (inicio + fim) // 2
        if lista[meio] == valor:
            contador += 1
            esquerda = busca_binaria(lista, inicio=inicio, fim=meio-1, valor=valor, contador=contador)
            direita = busca_binaria(lista, inicio=meio+1, fim=fim, valor=valor, contador=contador)
            return esquerda + direita + 1

        elif lista[meio] < valor:
            return busca_binaria(lista, inicio=meio + 1, fim=fim, valor=valor)
        else:
            return busca_binaria(lista, inicio, fim=meio - 1, valor=valor)

    A.sort() # Ignorar esta parte, foi feito somente para garantir 
             # a análise  com um array ordenado
    total = 0
    print(A)
    for i in range(len(A)):
        left = i
        right = len(A) - 1
        complemento = k - A[i]
        total += busca_binaria(lista=A, inicio=left, fim=len(A)-1, valor=complemento,contador=0)
        # if A[right] == complemento:
        #     cont = 0
        #     while (left <= right and A[right] == complemento):
        #         print((A[i], complemento))
        #         cont  += 1
        #         right -=1
        #     total += cont
        #     print()
        #     continue
        
        # while (left <= right):
            # mid = (left + right) // 2
            # if (A[mid] == complemento):
                # print((A[i], complemento))
                # cont = 0
                # while (left <= mid and A[mid] == complemento):
                    # cont += 1
                    # mid  -=1
                # total += cont
                # break

            # if (complemento < A[mid]):
                # right = mid - 1
            # else:
                # left = mid + 1

    return total


def problema_8_c(A, k):
    """
    Podemos percorrer o array ordenado pela esquerda e direita ao mesmo
    tempo. Passando por cada elemento somente uma vez. Ou seja, o algoritmo
    é O(n) em questão de complexidade de execução e O(1) em armazenamento
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
