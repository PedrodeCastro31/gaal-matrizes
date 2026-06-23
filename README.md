# gaal-matrizes

Trabalho Computacional 3 - GAAL  
**Determinantes: Expansao por Cofatores vs Operacoes Elementares**

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python main.py
```

## Modos do programa

1. **Matriz manual** - digite uma matriz 2x2 ate 6x6, veja determinante, historico, tempos e graficos.
2. **Benchmark** - gera matrizes aleatorias para ordens 2 a 6 e abre painel com graficos comparativos.
3. **Matriz aleatoria** - gera uma matriz da ordem escolhida e mostra a analise completa.

## Estrutura

| Arquivo | Descricao |
|---------|-----------|
| `expansao_cofatores.py` | Determinante recursivo por cofatores |
| `operacoes_elementares.py` | Determinante por triangularizacao |
| `analise.py` | Benchmark, medicao de tempos e comparacao |
| `visualizacao.py` | Graficos matplotlib |
| `main.py` | Menu principal |

## Analise obrigatoria (respostas)

### 1. Os resultados coincidiram?

**Sim.** Para todas as matrizes testadas (ordens 2 a 6), os dois metodos produziram o mesmo determinante, com tolerancia para arredondamento de ponto flutuante no metodo das operacoes elementares.

### 2. Qual metodo foi mais eficiente?

**Operacoes elementares.** O benchmark mostra tempos consistentemente menores e crescimento muito mais lento (aproximadamente O(n³)) em relacao a expansao por cofatores.

### 3. Por que o metodo dos cofatores se torna inviavel para matrizes maiores?

Porque sua complexidade e aproximadamente **O(n!)**: cada nivel da recursao gera n subproblemas menores, e o numero de operacoes explode rapidamente. Nos graficos, isso aparece na curva de operacoes e no tempo (escala log).

### 4. Em quais situacoes o metodo dos cofatores ainda e pedagogicamente util?

- Matrizes pequenas (**2x2** e **3x3**), onde a recursao e facil de acompanhar passo a passo.
- Demonstracao da definicao de cofator e da estrutura do determinante como polinomio nas entradas.
- Exercicios teoricos e provas, onde a forma explicita da expansao e mais importante que a eficiencia.

## Validacao

Execute o script de validacao contra `numpy.linalg.det`:

```bash
python validar.py
```
