from __future__ import annotations

from pathlib import Path
from typing import List

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from analise import ResultadoBenchmark

_PASTA_GRAFICOS = Path(__file__).parent / "graficos"


def formatar_valores_matriz(matriz: List[List[float | int]]) -> np.ndarray:
    return np.array(matriz, dtype=float)


def exibir_figura(fig: plt.Figure, nome_arquivo: str) -> None:
    """Salva o grafico em disco e exibe se o backend for interativo."""
    _PASTA_GRAFICOS.mkdir(exist_ok=True)
    caminho = _PASTA_GRAFICOS / nome_arquivo
    fig.savefig(caminho, dpi=150, bbox_inches="tight")

    backend = matplotlib.get_backend().lower()
    if backend == "agg":
        print(f"Grafico salvo em: {caminho}")
        plt.close(fig)
        return

    print(f"Grafico salvo em: {caminho}")
    plt.show()


def exibir_painel_benchmark(resultado: ResultadoBenchmark) -> None:
    ordens = resultado.ordens
    speedup = [
        cof / ope if ope > 0 else 0
        for cof, ope in zip(resultado.tempos_cofatores, resultado.tempos_operacoes)
    ]

    fig, axes = plt.subplots(2, 2, figsize=(12, 9))
    fig.suptitle(
        "Trabalho 3 - Comparacao: Cofatores vs Operacoes Elementares",
        fontsize=14,
        fontweight="bold",
    )

    ax1 = axes[0, 0]
    ax1.plot(ordens, resultado.tempos_cofatores, "o-", label="Cofatores", linewidth=2)
    ax1.plot(ordens, resultado.tempos_operacoes, "s-", label="Operacoes elementares", linewidth=2)
    ax1.set_yscale("log")
    ax1.set_xlabel("Ordem da matriz")
    ax1.set_ylabel("Tempo medio (s) - escala log")
    ax1.set_title("Tempo de execucao x ordem")
    ax1.set_xticks(ordens)
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    ax2 = axes[0, 1]
    ax2.plot(ordens, resultado.operacoes_cofatores, "o-", label="Cofatores", linewidth=2)
    ax2.plot(ordens, resultado.operacoes_elementares, "s-", label="Operacoes elementares", linewidth=2)
    ax2.set_yscale("log")
    ax2.set_xlabel("Ordem da matriz")
    ax2.set_ylabel("Operacoes - escala log")
    ax2.set_title("Crescimento das operacoes")
    ax2.set_xticks(ordens)
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    ax3 = axes[1, 0]
    ax3.bar(ordens, speedup, color="#3498db", edgecolor="black")
    ax3.set_xticks(ordens)
    ax3.set_xticklabels([str(o) for o in ordens])
    ax3.axhline(1, color="gray", linestyle="--", linewidth=1)
    ax3.set_xlabel("Ordem da matriz")
    ax3.set_ylabel("Speedup (tempo cofatores / tempo op. elementares)")
    ax3.set_title("Ganho de desempenho por ordem")
    ax3.grid(True, axis="y", alpha=0.3)

    ax4 = axes[1, 1]
    ax4.axis("off")
    linhas = [
        "Resumo da analise obrigatoria:",
        "",
        f"1. Resultados coincidem? {'Sim' if all(resultado.coincidencias) else 'Nao'}",
        "2. Metodo mais eficiente: Operacoes elementares",
        "3. Cofatores crescem ~O(n!); inviavel para n grande",
        "4. Cofatores uteis pedagogicamente em n <= 3",
        "",
        "Detalhes por ordem:",
    ]
    for det in resultado.detalhes:
        status = "OK" if det.resultados_coincidem else "DIFERENTE"
        linhas.append(
            f"n={det.ordem}: cof={det.tempo_cofatores:.6f}s | "
            f"ope={det.tempo_operacoes:.6f}s | {status}"
        )
    ax4.text(
        0.02,
        0.98,
        "\n".join(linhas),
        va="top",
        ha="left",
        fontsize=10,
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="#f7f7f7", edgecolor="#cccccc"),
    )

    plt.tight_layout()
    exibir_figura(fig, "benchmark.png")


def exibir_analise_matriz(
    matriz: List[List[int]],
    comparacao: dict,
) -> None:
    fig = plt.figure(figsize=(14, 6))
    gs = fig.add_gridspec(2, 3, height_ratios=[1.4, 0.8], hspace=0.35, wspace=0.35)
    fig.suptitle("Analise da matriz informada", fontsize=14, fontweight="bold")

    matriz_np = formatar_valores_matriz(matriz)
    triangular_np = formatar_valores_matriz(comparacao["matriz_triangular"])

    ax1 = fig.add_subplot(gs[0, 0])
    im1 = ax1.imshow(matriz_np, cmap="Blues")
    ax1.set_title("Matriz inicial")
    ax1.set_xticks(range(matriz_np.shape[1]))
    ax1.set_yticks(range(matriz_np.shape[0]))
    for i in range(matriz_np.shape[0]):
        for j in range(matriz_np.shape[1]):
            ax1.text(j, i, f"{int(matriz_np[i, j])}", ha="center", va="center", color="black")
    fig.colorbar(im1, ax=ax1, fraction=0.046)

    ax2 = fig.add_subplot(gs[0, 1])
    im2 = ax2.imshow(triangular_np, cmap="Greens")
    ax2.set_title("Matriz triangular (op. elementares)")
    ax2.set_xticks(range(triangular_np.shape[1]))
    ax2.set_yticks(range(triangular_np.shape[0]))
    for i in range(triangular_np.shape[0]):
        for j in range(triangular_np.shape[1]):
            ax2.text(
                j,
                i,
                f"{triangular_np[i, j]:.1f}",
                ha="center",
                va="center",
                color="black",
                fontsize=8,
            )
    fig.colorbar(im2, ax=ax2, fraction=0.046)

    ax3 = fig.add_subplot(gs[0, 2])
    ax3.axis("off")
    mais_rapido = (
        "Operacoes elementares"
        if comparacao["tempo_operacoes"] <= comparacao["tempo_cofatores"]
        else "Cofatores"
    )
    texto = (
        f"Determinante (cofatores): {comparacao['determinante_cofatores']}\n"
        f"Determinante (op. elementares): {comparacao['determinante_operacoes']:.0f}\n"
        f"Coincidem: {'Sim' if comparacao['coincidem'] else 'Nao'}\n\n"
        f"Tempo cofatores: {comparacao['tempo_cofatores']:.6f} s\n"
        f"Tempo op. elementares: {comparacao['tempo_operacoes']:.6f} s\n"
        f"Mais rapido: {mais_rapido}\n\n"
        f"Operacoes cofatores: {comparacao['operacoes_cofatores']}\n"
        f"Operacoes elementares: {comparacao['operacoes_elementares']}\n"
        f"Chamadas recursivas: {comparacao['chamadas_recursivas']}\n"
        f"Trocas de linhas: {comparacao['trocas_linhas']}"
    )
    ax3.text(
        0.05,
        0.95,
        texto,
        va="top",
        ha="left",
        fontsize=11,
        family="monospace",
        bbox=dict(boxstyle="round", facecolor="#fff8e1", edgecolor="#ffcc80"),
    )

    ax_bar = fig.add_subplot(gs[1, :])
    tempos = [comparacao["tempo_cofatores"], comparacao["tempo_operacoes"]]
    labels = ["Cofatores", "Op. elem."]
    posicoes = [0, 1]
    ax_bar.bar(posicoes, tempos, color=["#e67e22", "#27ae60"], width=0.5)
    ax_bar.set_xticks(posicoes)
    ax_bar.set_xticklabels(labels)
    ax_bar.set_ylabel("Tempo (s)")
    ax_bar.set_title("Comparacao de tempo")
    ax_bar.grid(True, axis="y", alpha=0.3)

    exibir_figura(fig, "analise_matriz.png")
