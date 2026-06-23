from typing import List

def matriz_menor(matriz: List[List[int]], i: int, j: int) -> List[List[int]]:
    """
    Retorna a matriz menor de uma matriz quadrada.
    A matriz menor é a matriz resultante da remoção da linha i e da coluna j da matriz original.
    """
    
    matriz_menor: list[list[int]] = []
    for x in range(len(matriz)):
        if x != i: # Não adiciona elementos da linha i
            linha = []
            for y in range(len(matriz)):
                if y != j: # Não adiciona elementos da coluna j
                    linha.append(matriz[x][y])
            matriz_menor.append(linha)
    return matriz_menor

def determinante_expansao_cofatores(matriz: List[List[int]]) -> int:
    """
    Calcula o determinante de uma matriz quadrada utilizando a expansão por cofatores.
    """
    ordem: int = len(matriz)
    
    # Caso base: matriz 1x1
    if ordem == 1:
        return matriz[0][0]
    # Caso base: matriz 2x2
    if ordem == 2:
        return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]

    determinante: int = 0
    for coluna in range(ordem):
        cofator: int = ((-1) ** coluna)
        elemento: int = matriz[0][coluna]
        menor: List[List[int]] = matriz_menor(matriz, 0, coluna)
        determinante += cofator * elemento * determinante_expansao_cofatores(menor)
    return determinante