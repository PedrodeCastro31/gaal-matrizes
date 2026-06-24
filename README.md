# gaal-matrizes

Trabalho Computacional 3 — GAAL  
**Determinantes: Expansão por Cofatores vs Operações Elementares**

Programa em Python que calcula o determinante de matrizes quadradas (ordem 2 a 6) por dois métodos, compara resultados, registra etapas e mede desempenho.

## Como executar

```bash
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
pip install -r requirements.txt
python main.py
```

## Estrutura

| Arquivo | Função |
|---------|--------|
| `expansao_cofatores.py` | Determinante recursivo por cofatores |
| `operacoes_elementares.py` | Determinante por triangularização |
| `analise.py` | Benchmark, tempos e comparação |
| `visualizacao.py` | Gráficos matplotlib |
| `main.py` | Menu principal |
| `validar.py` | Testes de corretude |
| `graficos/` | PNGs gerados (`analise_matriz.png`, `benchmark.png`) |

## Lógica — Expansão por Cofatores

Implementada em `expansao_cofatores.py`, expande sempre pela **1ª linha** (Laplace):

```
det(A) = Σ (-1)^j · a[0][j] · det(menor[0][j])
```

1. Para cada coluna `j`, remove a linha 0 e a coluna `j` → `matriz_menor(matriz, 0, j)`.
2. Multiplica o elemento `a[0][j]` pelo sinal `(-1)^j` e pelo determinante da menor (recursão).
3. Soma todos os termos.

**Casos base:** matriz 1×1 retorna o único elemento; matriz 2×2 retorna `ad - bc`.

**Custo:** ~O(n!) — cada nível gera `n` subproblemas menores. O programa registra chamadas recursivas e operações.

## Lógica — Operações Elementares

Implementada em `operacoes_elementares.py`, triangulariza a matriz por **eliminação de Gauss com pivotamento parcial**:

1. Em cada coluna, escolhe o maior pivô (em módulo) e troca linhas se necessário.
2. Cada troca de linha inverte o sinal do determinante.
3. Zera os elementos abaixo do pivô: `L_i ← L_i - fator · L_pivô`.
4. Se a coluna do pivô for inteiramente nula → determinante = 0.
5. Ao final: `det = (±1) × ∏ diagonal` (sinal conforme trocas; resultado arredondado para inteiro).

**Custo:** ~O(n³) — adequado para matrizes maiores.

## Modos do programa

1. **Matriz manual** — digita a matriz, vê determinante, histórico, tempos e gráfico.
2. **Benchmark** — matrizes aleatórias (ordens 2 a 6), painel com tempos, operações e speedup.
3. **Matriz aleatória** — gera matriz da ordem escolhida e exibe análise completa.

## Saídas

- **Terminal:** determinantes, histórico de etapas, tempos, contagem de operações.
- **Gráficos:** salvos em `graficos/` — matriz inicial, triangular, comparação de tempo e benchmark por ordem.