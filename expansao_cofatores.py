def menor(m, i, j):
    # Remove linha i e coluna j da matriz
    return [ [m[x][y] for y in range(len(m)) if y != j] for x in range(len(m)) if x != i ]
    
def determinante_expansao_cofatores(matriz):


    def determinante_recursivo(m):
        n = len(m)
        if n == 1:
            return m[0][0]
        elif n == 2:
            return m[0][0]*m[1][1] - m[0][1]*m[1][0]
        else:
            det = 0
            for j in range(n):
                cof = ((-1) ** (0 + j)) * m[0][j] * determinante_recursivo(menor(m, 0, j))
                det += cof
            return det

    def cofactor(m, i, j):
        # Menor complementar assinado (cofator)
        return ((-1) ** (i + j)) * determinante_recursivo(menor(m, i, j))

    n = len(matriz)
    # Matriz de cofatores
    cofatores = []
    for i in range(n):
        linha_cof = []
        for j in range(n):
            linha_cof.append(cofactor(matriz, i, j))
        cofatores.append(linha_cof)
    det = determinante_recursivo(matriz)
    return cofatores, det