from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class ResultadoOperacoesElementares:
    determinante: float
    historico: List[str] = field(default_factory=list)
    matriz_triangular: List[List[float]] = field(default_factory=list)
    trocas_linhas: int = 0
    operacoes: int = 0


def _formatar_matriz(matriz: List[List[float]]) -> str:
    return "\n".join("  ".join(f"{valor:8.2f}" for valor in linha) for linha in matriz)


def determinante_operacoes_elementares(
    matriz: List[List[int | float]],
    registrar_historico: bool = True,
) -> ResultadoOperacoesElementares:
    """
    Calcula o determinante triangularizando a matriz com pivotamento parcial.
    Registra trocas de linhas, corrige o sinal e multiplica a diagonal principal.
    """
    ordem = len(matriz)
    if ordem == 0:
        raise ValueError("A matriz não pode ser vazia.")

    matriz_trabalho = [[float(valor) for valor in linha] for linha in matriz]
    historico: List[str] = []
    trocas = 0
    operacoes = 0

    if registrar_historico:
        historico.append("Matriz inicial:\n" + _formatar_matriz(matriz_trabalho))

    for coluna in range(ordem):
        pivot = coluna
        for linha in range(coluna + 1, ordem):
            if abs(matriz_trabalho[linha][coluna]) > abs(matriz_trabalho[pivot][coluna]):
                pivot = linha
            operacoes += 1

        if abs(matriz_trabalho[pivot][coluna]) < 1e-12:
            if registrar_historico:
                historico.append(
                    f"Coluna {coluna + 1} inteira nula após pivotamento: determinante = 0."
                )
            return ResultadoOperacoesElementares(
                determinante=0.0,
                historico=historico,
                matriz_triangular=matriz_trabalho,
                trocas_linhas=trocas,
                operacoes=operacoes,
            )

        if pivot != coluna:
            matriz_trabalho[coluna], matriz_trabalho[pivot] = (
                matriz_trabalho[pivot],
                matriz_trabalho[coluna],
            )
            trocas += 1
            if registrar_historico:
                historico.append(
                    f"Troca de linhas L{coluna + 1} <-> L{pivot + 1} "
                    f"(sinal do determinante invertido).\n"
                    + _formatar_matriz(matriz_trabalho)
                )

        pivot_valor = matriz_trabalho[coluna][coluna]
        for linha in range(coluna + 1, ordem):
            if abs(matriz_trabalho[linha][coluna]) < 1e-12:
                continue

            fator = matriz_trabalho[linha][coluna] / pivot_valor
            operacoes += 1

            for col in range(coluna, ordem):
                matriz_trabalho[linha][col] -= fator * matriz_trabalho[coluna][col]
                operacoes += 1

            if registrar_historico:
                historico.append(
                    f"L{linha + 1} <- L{linha + 1} - ({fator:.4f}) * L{coluna + 1}\n"
                    + _formatar_matriz(matriz_trabalho)
                )

    determinante = 1.0
    for i in range(ordem):
        determinante *= matriz_trabalho[i][i]
        operacoes += 1

    if trocas % 2 == 1:
        determinante *= -1
        operacoes += 1

    determinante = round(determinante)
    if abs(determinante - round(determinante)) < 1e-9:
        determinante = float(int(round(determinante)))

    if registrar_historico:
        diagonal = " x ".join(f"{matriz_trabalho[i][i]:.2f}" for i in range(ordem))
        sinal = "negativo" if trocas % 2 == 1 else "positivo"
        historico.append(
            f"Matriz triangular final:\n{_formatar_matriz(matriz_trabalho)}\n"
            f"Diagonal principal: {diagonal}\n"
            f"Trocas de linhas: {trocas} (sinal {sinal})\n"
            f"Determinante = {determinante:.0f}"
        )

    return ResultadoOperacoesElementares(
        determinante=determinante,
        historico=historico,
        matriz_triangular=matriz_trabalho,
        trocas_linhas=trocas,
        operacoes=operacoes,
    )
