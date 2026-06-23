"""Valida os dois metodos contra numpy.linalg.det."""

from __future__ import annotations

import random

import numpy as np

from analise import gerar_matriz_aleatoria
from expansao_cofatores import determinante_expansao_cofatores
from operacoes_elementares import determinante_operacoes_elementares


def validar_matriz(matriz: list[list[int]]) -> tuple[bool, float, int, float]:
    np_det = round(float(np.linalg.det(np.array(matriz, dtype=float))))
    det_cof = determinante_expansao_cofatores(matriz)
    det_ope = determinante_operacoes_elementares(matriz, registrar_historico=False).determinante
    ok = det_cof == np_det and abs(det_ope - np_det) < 1e-6
    return ok, np_det, det_cof, det_ope


def main() -> None:
    random.seed(42)
    casos_fixos = [
        [[1, 2], [3, 4]],
        [[1, 0], [0, 1]],
        [[2, 0, 0], [0, 3, 0], [0, 0, 4]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[0, 1, 2], [3, 4, 5], [6, 7, 8]],
    ]

    erros = 0
    total = 0

    print("Validacao contra numpy.linalg.det\n")

    for matriz in casos_fixos:
        total += 1
        ok, np_det, det_cof, det_ope = validar_matriz(matriz)
        status = "OK" if ok else "ERRO"
        print(
            f"{status} | numpy={np_det:.0f} cof={det_cof} ope={det_ope:.0f} | "
            f"ordem={len(matriz)}"
        )
        if not ok:
            erros += 1

    for ordem in range(2, 7):
        for _ in range(10):
            total += 1
            matriz = gerar_matriz_aleatoria(ordem)
            ok, np_det, det_cof, det_ope = validar_matriz(matriz)
            if not ok:
                erros += 1
                print(
                    f"ERRO | ordem={ordem} numpy={np_det:.0f} "
                    f"cof={det_cof} ope={det_ope:.0f}"
                )

    print(f"\nTotal: {total} | Erros: {erros}")
    if erros == 0:
        print("Validacao concluida com sucesso.")
    else:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
