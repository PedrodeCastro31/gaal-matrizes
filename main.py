from __future__ import annotations

from analise import comparar_metodos_matriz, executar_benchmark, gerar_matriz_aleatoria
from visualizacao import exibir_analise_matriz, exibir_painel_benchmark


def ler_ordem() -> int:
    print("Insira a ordem da matriz (2 a 6):")
    while True:
        try:
            ordem = int(input("> "))
            if 2 <= ordem <= 6:
                return ordem
            print("Por favor, digite um numero entre 2 e 6.")
        except ValueError:
            print("Por favor, digite um numero valido entre 2 e 6.")


def ler_matriz(ordem: int) -> list[list[int]]:
    matriz: list[list[int]] = []
    print(f"Insira os elementos da matriz {ordem}x{ordem}, linha por linha:")
    for i in range(ordem):
        while True:
            try:
                entrada = input(f"Linha {i + 1}: ").split()
                linha = [int(x) for x in entrada]
                if len(linha) != ordem:
                    print(f"Insira exatamente {ordem} numeros.")
                    continue
                matriz.append(linha)
                break
            except ValueError:
                print("Insira apenas numeros inteiros separados por espaco.")
    return matriz


def imprimir_matriz(matriz: list[list[int]]) -> None:
    print("\nMatriz:")
    for linha in matriz:
        print("  ".join(f"{valor:4d}" for valor in linha))


def imprimir_historico(titulo: str, historico: list[str], limite: int = 8) -> None:
    print(f"\n--- {titulo} ---")
    if len(historico) <= limite:
        for etapa in historico:
            print(etapa)
            print("-" * 40)
    else:
        for etapa in historico[:3]:
            print(etapa)
            print("-" * 40)
        print(f"... ({len(historico) - 5} etapas omitidas) ...")
        for etapa in historico[-2:]:
            print(etapa)
            print("-" * 40)


def modo_matriz_manual() -> None:
    print("\n=== Modo 1: Matriz manual ===")
    ordem = ler_ordem()
    matriz = ler_matriz(ordem)
    imprimir_matriz(matriz)

    print("\nCalculando determinantes pelos dois metodos...")
    comparacao = comparar_metodos_matriz(matriz)

    print("\n=== Resultados ===")
    print(f"Determinante (cofatores):        {comparacao['determinante_cofatores']}")
    print(f"Determinante (op. elementares):  {comparacao['determinante_operacoes']:.0f}")
    print(f"Resultados coincidem:            {'Sim' if comparacao['coincidem'] else 'Nao'}")
    print(f"Tempo cofatores:                 {comparacao['tempo_cofatores']:.6f} s")
    print(f"Tempo op. elementares:           {comparacao['tempo_operacoes']:.6f} s")
    print(f"Operacoes cofatores:             {comparacao['operacoes_cofatores']}")
    print(f"Operacoes elementares:           {comparacao['operacoes_elementares']}")
    print(f"Chamadas recursivas:             {comparacao['chamadas_recursivas']}")
    print(f"Trocas de linhas:                {comparacao['trocas_linhas']}")

    imprimir_historico("Historico - Cofatores", comparacao["historico_cofatores"])
    imprimir_historico("Historico - Operacoes elementares", comparacao["historico_operacoes"])

    print("\nAbrindo painel visual...")
    exibir_analise_matriz(matriz, comparacao)


def modo_benchmark() -> None:
    print("\n=== Modo 2: Benchmark aleatorio (ordens 2 a 6) ===")
    print("Gerando matrizes aleatorias e medindo tempos...")

    resultado = executar_benchmark(
        ordem_minima=2,
        ordem_maxima=6,
        matrizes_por_ordem=5,
        repeticoes_tempo=5,
    )

    print("\n=== Resultados do benchmark ===")
    for det in resultado.detalhes:
        status = "OK" if det.resultados_coincidem else "DIFERENTE"
        print(
            f"n={det.ordem}: "
            f"cofatores={det.tempo_cofatores:.6f}s ({det.operacoes_cofatores:.0f} ops) | "
            f"op.elem.={det.tempo_operacoes:.6f}s ({det.operacoes_elementares:.0f} ops) | "
            f"{status}"
        )

    ordem_perceptivel = next(
        (
            det.ordem
            for det in resultado.detalhes
            if det.tempo_cofatores > det.tempo_operacoes * 2
        ),
        None,
    )
    if ordem_perceptivel:
        print(
            f"\nA diferenca de desempenho fica perceptivel a partir da ordem {ordem_perceptivel}."
        )
    else:
        print("\nA diferenca ainda e pequena nas ordens testadas, mas o crescimento e visivel nos graficos.")

    print("\nAbrindo painel de graficos...")
    exibir_painel_benchmark(resultado)


def modo_matriz_aleatoria() -> None:
    print("\n=== Modo 3: Matriz aleatoria (analise completa) ===")
    ordem = ler_ordem()
    matriz = gerar_matriz_aleatoria(ordem)
    print("\nMatriz gerada aleatoriamente:")
    imprimir_matriz(matriz)

    comparacao = comparar_metodos_matriz(matriz)
    print(f"\nDeterminante: {comparacao['determinante_cofatores']} (ambos os metodos)")
    exibir_analise_matriz(matriz, comparacao)


def exibir_menu() -> None:
    print("\n" + "=" * 52)
    print(" Trabalho 3 - Determinantes")
    print(" Cofatores vs Operacoes Elementares")
    print("=" * 52)
    print("1 - Informar matriz manualmente")
    print("2 - Executar benchmark (graficos por ordem)")
    print("3 - Gerar matriz aleatoria e analisar")
    print("0 - Sair")


def main() -> None:
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opcao: ").strip()

        if opcao == "1":
            modo_matriz_manual()
        elif opcao == "2":
            modo_benchmark()
        elif opcao == "3":
            modo_matriz_aleatoria()
        elif opcao == "0":
            print("Encerrando.")
            break
        else:
            print("Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
