def longestPalindrome(self, s: str) -> str:
        #  Podemos duplicar a string, criando uma s2 que seja a simétrica de s
        #  Criamos uma matriz M (n + 1) x (n + 1) para representar a memoization
        n = len(s)
        s2 = ""
        for i in reversed(range(n)):
            s2 += s[i]
        M = [[0] * (n + 1) for _ in range(n + 1)]
        # print(s, s2)
        coord_max = (0,0)
        len_max = 0
        for i in range(1,n+1):
            for j in range(1,n+1):
                if s[i - 1] == s2[j - 1]:
                    print(s[i-1], s2[j-1])
                    M[i][j] += M[i-1][j-1] + 1
                    if M[i][j] > len_max:
                        len_max = M[i][j] 
                        coord_max = (i,j)
        
        resposta = ""
        i, j = coord_max
        while(M[i][j] != 0):
            resposta += s[i - 1]
            i -= 1
            j -= 1  
        return resposta
             


s= "aacabdkacaa"
print(longestPalindrome(1,s))