def problema_4(A: List[int], k: int) -> Tuple[int, int, int, int]:
    somas = []
    n = len(A)

    for i in range(n):
        for j in range(i,n):
            somas.append((A[i]+A[j], i, j))

    somas = sorted(somas)

    indices = None

    for i in range(n):
        for j in range(i,n):
            esquerda = 0
            direita = n-1
            
            while esquerda <= direita:
                atual = (esquerda + direita)//2

                soma = somas[atual]
                
                if soma[0] + A[i] + A[j] > k:
                    direita = atual - 1
                elif soma[0] + A[i] + A[j] < k:
                    esquerda = atual + 1
                    
                elif len({i, j, soma[1], soma[2]}) == 4:
                    indices = (i+1, j+1, soma[1]+1, soma[2]+1)
                    break
            
            if indices is not None:
                break
        if indices is not None:
            break
    
    if indices is None:
        return (-1,-1,-1,-1)

    indices = sorted(indices)

    return indices