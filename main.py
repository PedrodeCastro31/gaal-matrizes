from expansao_cofatores import determinante_expansao_cofatores


def main():
    print("Insira a ordem da matriz (2 a 6):")
    while True:
        try:
            ordem = int(input())
            if 2 <= ordem <= 6:
                break
            else:
                print("Por favor, digite um número entre 2 e 6:")
        except ValueError:
            print("Por favor, digite um número válido entre 2 e 6:")

    matriz = []
    print(f"Insira os elementos da matriz {ordem}x{ordem}, linha por linha (separados por espaço):")
    for i in range(ordem):
        while True:
            try:
                entrada = input(f"Linha {i+1}: ").split()
                linha = [int(x) for x in entrada]
                if len(linha) != ordem:
                    print(f"Por favor, insira exatamente {ordem} números.")
                    continue
                matriz.append(linha)
                break
            except ValueError:
                print("Por favor, insira apenas números inteiros separados por espaço.")

    print("Matriz inserida:")
    for linha in matriz:
        print(" ".join(str(x) for x in linha))

    determinante = determinante_expansao_cofatores(matriz)
    print(f"Determinante: {determinante}")

if __name__ == "__main__":
    main()