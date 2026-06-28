
# Relatório de Verificação Formal — Problema 9: Máximo Divisor Comum (Algoritmo de Euclides)

## 1. Especificação e Proposta Inédita

Para expandir a bateria de testes práticos da disciplina, propomos a instrumentação do Algoritmo de Euclides para o cálculo do Máximo Divisor Comum (MDC). Este problema é ideal para a aplicação da Lógica de Hoare, pois baseia-se em uma propriedade fundamental da Teoria dos Números e exige uma transição de estado atômica.

| Item | Definição |
| :--- | :--- |
| Pré-condição | $a > 0 \land b \ge 0$ |
| Pós-condição | $res = \text{mdc}(a_0, b_0)$ |
| Invariante de loop | $\text{mdc}(a, b) == \text{mdc}(a_0, b_0)$ |
| Função variante | $V(state) = b$ (estritamente decrescente em $\mathbb{N}_0$) |
| Complexidade | $O(\log(\min(a, b)))$ iterações (Teorema de Lamé) |

---

## 2. Modelagem do Erro Proposital (State Overwrite)

Para atender à **Diretriz 6** do roteiro, modelamos um erro semântico comum em implementações imperativas: a destruição do estado anterior antes de concluir o passo indutivo. 

Na matemática discreta, o passo de Euclides dita que os próximos estados $(a', b')$ devem ser simultaneamente derivados dos estados atuais $(a, b)$ através da relação $a' = b$ e $b' = a \pmod b$. 

A função `mdc_euclides_INCORRETA_SOBRESCRITA` (presente em `mdc euclides.py`) realiza as atualizações de forma sequencial sem variável temporária:
1. `a = b` (o estado original de $a$ é sobrescrito e perdido).
2. `b = a % b` (como $a$ agora é igual a $b$, a instrução computa $b \pmod b$, resultando sempre em $0$).

Ao testar com o Data Set $a=48$ e $b=18$, a execução da asserção de manutenção no final do corpo do laço acusa o colapso:
> Erro: Invariante aniquilado por sobrescrita! mdc(novo_a=18, novo_b=0) = 18, esperado 6

Este erro comprova que a validade do invariante depende da **atomicidade da transição de estado** no espaço de memória da máquina.

---

## 3. Implementação Verificada

Na função `mdc_euclides_verified` (dentro de `mdc euclides.py`), o reparo estrutural foi realizado garantindo a transição atômica via desempacotamento de tuplas nativo do Python: `a, b = b, a % b`. Isso garante que o lado direito da expressão seja completamente avaliado utilizando o estado antigo antes de qualquer reatribuição.

Tabela de rastreio lógico ($a=48$, $b=18$):

| Instante Lógico | $a$ | $b$ | $\text{mdc}(a, b)$ | Status |
| :--- | :---: | :---: | :---: | :---: |
| Inicialização | 48 | 18 | 6 | ✅ |
| Fim da 1ª iteração | 18 | 12 | 6 | ✅ |
| Fim da 2ª iteração | 12 | 6 | 6 | ✅ |
| Fim da 3ª iteração | 6 | 0 | 6 | ✅ |
| Terminação | 6 | 0 | $res = 6$ | ✅ |

---

## 4. Prova de Correção Total

**Manutenção (passo indutivo):** Pelo Lema da Divisão de Euclides, para quaisquer inteiros $a, b$ com $b > 0$, o conjunto dos divisores comuns de $a$ e $b$ é idêntico ao conjunto dos divisores comuns de $b$ e $a \pmod b$. O invariante é matematicamente blindado durante a transição $a', b' = b, a \pmod b$.

**Terminação:** A função variante é $V(state) = b$. A cada passo, $b' = a \pmod b$. Pela definição do operador módulo, $0 \le a \pmod b < b$. O novo estado de $b$ é estritamente menor que o anterior, decrescendo monotonicamente no conjunto bem-ordenado $\mathbb{N}_0$, o que prova a terminação absoluta do laço.

**Dedução final ($I \land \lnot B \Rightarrow Q$):** Na saída do loop, a guarda $B \equiv (b > 0)$ é falsa, implicando $b = 0$. Substituindo no invariante:
$$\text{mdc}(a, 0) == \text{mdc}(a_0, b_0)$$
O maior divisor comum entre qualquer inteiro positivo $a$ e $0$ é trivialmente $a$. Portanto, $a = \text{mdc}(a_0, b_0)$, satisfazendo a pós-condição $Q$.

---

## 5. Conclusão e Testes

A prova de correção parcial aliada à prova de terminação no conjunto dos naturais garante a **Correção Total** do Algoritmo de Euclides. Os testes empíricos de fuzzing aplicados no script `mdc euclides.py` não relataram divergências contra $10.000$ amostras, atestando a robustez da instrumentação lógica proposta neste relatório.
