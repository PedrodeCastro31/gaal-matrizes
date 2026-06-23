from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ResultadoExpansaoCofatores:
    determinante: int
    historico: List[str] = field(default_factory=list)
    operacoes: int = 0
    chamadas_recursivas: int = 0


def matriz_menor(matriz: List[List[int]], i: int, j: int) -> List[List[int]]:
    """
    Retorna a matriz menor de uma matriz quadrada.
    A matriz menor é a matriz resultante da remoção da linha i e da coluna j da matriz original.
    """
    matriz_menor_resultado: list[list[int]] = []
    for x in range(len(matriz)):
        if x != i:
            linha = []
            for y in range(len(matriz)):
                if y != j:
                    linha.append(matriz[x][y])
            matriz_menor_resultado.append(linha)
    return matriz_menor_resultado


def _determinante_recursivo(
    matriz: List[List[int]],
    registrar_historico: bool,
    historico: List[str],
    contador: dict[str, int],
    profundidade: int,
) -> int:
    ordem: int = len(matriz)
    contador["chamadas"] += 1

    if ordem == 1:
        if registrar_historico and profundidade <= 2:
            historico.append(f"[n={ordem}] Caso base 1x1: det = {matriz[0][0]}")
        return matriz[0][0]

    if ordem == 2:
        contador["operacoes"] += 3
        det = matriz[0][0] * matriz[1][1] - matriz[0][1] * matriz[1][0]
        if registrar_historico and profundidade <= 2:
            historico.append(
                f"[n={ordem}] Caso base 2x2: "
                f"{matriz[0][0]}*{matriz[1][1]} - {matriz[0][1]}*{matriz[1][0]} = {det}"
            )
        return det

    if registrar_historico and profundidade == 0:
        historico.append(f"Expansão por cofatores na linha 1 (matriz {ordem}x{ordem})")

    determinante: int = 0
    for coluna in range(ordem):
        cofator: int = (-1) ** coluna
        elemento: int = matriz[0][coluna]
        menor: List[List[int]] = matriz_menor(matriz, 0, coluna)
        contador["operacoes"] += len(matriz) * len(matriz)

        det_menor = _determinante_recursivo(
            menor,
            registrar_historico and profundidade < 1,
            historico,
            contador,
            profundidade + 1,
        )
        contador["operacoes"] += 2
        termo = cofator * elemento * det_menor
        determinante += termo

        if registrar_historico and profundidade == 0:
            historico.append(
                f"  Coluna {coluna + 1}: sinal={cofator:+d}, "
                f"elemento={elemento}, det(menor)={det_menor}, termo={termo}"
            )

    if registrar_historico and profundidade == 0:
        historico.append(f"Determinante final (cofatores) = {determinante}")

    return determinante


def determinante_expansao_cofatores(matriz: List[List[int]]) -> int:
    """
    Calcula o determinante de uma matriz quadrada utilizando a expansão por cofatores.
    """
    return determinante_expansao_cofatores_detalhado(matriz, registrar_historico=False).determinante


def determinante_expansao_cofatores_detalhado(
    matriz: List[List[int]],
    registrar_historico: bool = True,
) -> ResultadoExpansaoCofatores:
    """
    Versão instrumentada da expansão por cofatores.
    Retorna determinante, histórico resumido e contagem de operações.
    """
    historico: List[str] = []
    contador = {"operacoes": 0, "chamadas": 0}

    determinante = _determinante_recursivo(
        matriz,
        registrar_historico,
        historico,
        contador,
        profundidade=0,
    )

    if registrar_historico and len(matriz) > 3:
        historico.append(
            f"(Histórico resumido: matriz {len(matriz)}x{len(matriz)} "
            f"gera {contador['chamadas']} chamadas recursivas.)"
        )

    return ResultadoExpansaoCofatores(
        determinante=determinante,
        historico=historico,
        operacoes=contador["operacoes"],
        chamadas_recursivas=contador["chamadas"],
    )
