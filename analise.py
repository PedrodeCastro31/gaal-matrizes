from __future__ import annotations

import random
import time
from dataclasses import dataclass, field
from typing import List

from expansao_cofatores import determinante_expansao_cofatores_detalhado
from operacoes_elementares import determinante_operacoes_elementares


@dataclass
class ResultadoOrdem:
    ordem: int
    tempo_cofatores: float
    tempo_operacoes: float
    operacoes_cofatores: float
    operacoes_elementares: float
    resultados_coincidem: bool


@dataclass
class ResultadoBenchmark:
    ordens: List[int] = field(default_factory=list)
    tempos_cofatores: List[float] = field(default_factory=list)
    tempos_operacoes: List[float] = field(default_factory=list)
    operacoes_cofatores: List[float] = field(default_factory=list)
    operacoes_elementares: List[float] = field(default_factory=list)
    coincidencias: List[bool] = field(default_factory=list)
    detalhes: List[ResultadoOrdem] = field(default_factory=list)


def gerar_matriz_aleatoria(ordem: int, minimo: int = -9, maximo: int = 9) -> List[List[int]]:
    return [[random.randint(minimo, maximo) for _ in range(ordem)] for _ in range(ordem)]


def _medir_tempo(func, *args, repeticoes: int = 5) -> float:
    inicio = time.perf_counter()
    for _ in range(repeticoes):
        func(*args)
    fim = time.perf_counter()
    return (fim - inicio) / repeticoes


def _resultados_coincidem(det_cofatores: int, det_operacoes: float, tolerancia: float = 1e-6) -> bool:
    return abs(det_cofatores - det_operacoes) <= tolerancia


def executar_benchmark(
    ordem_minima: int = 2,
    ordem_maxima: int = 6,
    matrizes_por_ordem: int = 5,
    repeticoes_tempo: int = 5,
    semeadura: int | None = 42,
) -> ResultadoBenchmark:
    if semeadura is not None:
        random.seed(semeadura)

    resultado = ResultadoBenchmark()

    for ordem in range(ordem_minima, ordem_maxima + 1):
        tempos_cof = []
        tempos_ope = []
        ops_cof = []
        ops_ope = []
        coincidem_todos = True

        repeticoes = repeticoes_tempo if ordem <= 5 else max(1, repeticoes_tempo // 2)

        for _ in range(matrizes_por_ordem):
            matriz = gerar_matriz_aleatoria(ordem)

            tempo_cof = _medir_tempo(
                lambda m=matriz: determinante_expansao_cofatores_detalhado(
                    m, registrar_historico=False
                ),
                repeticoes=repeticoes,
            )
            tempo_ope = _medir_tempo(
                lambda m=matriz: determinante_operacoes_elementares(
                    m, registrar_historico=False
                ),
                repeticoes=repeticoes,
            )

            res_cof = determinante_expansao_cofatores_detalhado(matriz, registrar_historico=False)
            res_ope = determinante_operacoes_elementares(matriz, registrar_historico=False)

            coincidem = _resultados_coincidem(res_cof.determinante, res_ope.determinante)
            coincidem_todos = coincidem_todos and coincidem

            tempos_cof.append(tempo_cof)
            tempos_ope.append(tempo_ope)
            ops_cof.append(res_cof.operacoes)
            ops_ope.append(res_ope.operacoes)

        detalhe = ResultadoOrdem(
            ordem=ordem,
            tempo_cofatores=sum(tempos_cof) / len(tempos_cof),
            tempo_operacoes=sum(tempos_ope) / len(tempos_ope),
            operacoes_cofatores=sum(ops_cof) / len(ops_cof),
            operacoes_elementares=sum(ops_ope) / len(ops_ope),
            resultados_coincidem=coincidem_todos,
        )

        resultado.ordens.append(ordem)
        resultado.tempos_cofatores.append(detalhe.tempo_cofatores)
        resultado.tempos_operacoes.append(detalhe.tempo_operacoes)
        resultado.operacoes_cofatores.append(detalhe.operacoes_cofatores)
        resultado.operacoes_elementares.append(detalhe.operacoes_elementares)
        resultado.coincidencias.append(coincidem_todos)
        resultado.detalhes.append(detalhe)

    return resultado


def comparar_metodos_matriz(matriz: List[List[int]]) -> dict:
    inicio = time.perf_counter()
    res_cof = determinante_expansao_cofatores_detalhado(matriz, registrar_historico=True)
    tempo_cof = time.perf_counter() - inicio

    inicio = time.perf_counter()
    res_ope = determinante_operacoes_elementares(matriz, registrar_historico=True)
    tempo_ope = time.perf_counter() - inicio

    return {
        "determinante_cofatores": res_cof.determinante,
        "determinante_operacoes": res_ope.determinante,
        "coincidem": _resultados_coincidem(res_cof.determinante, res_ope.determinante),
        "tempo_cofatores": tempo_cof,
        "tempo_operacoes": tempo_ope,
        "operacoes_cofatores": res_cof.operacoes,
        "operacoes_elementares": res_ope.operacoes,
        "chamadas_recursivas": res_cof.chamadas_recursivas,
        "historico_cofatores": res_cof.historico,
        "historico_operacoes": res_ope.historico,
        "matriz_triangular": res_ope.matriz_triangular,
        "trocas_linhas": res_ope.trocas_linhas,
    }
