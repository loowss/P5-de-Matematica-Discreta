"""
Este script implementa uma proposta adicional aos 8 problemas originais, 
demonstrando a aplicação da Lógica de Hoare no Teorema de Euclides, com a 
modelagem de um erro intencional de "State Overwrite" (sobrescrita de estado).
"""

import math
import random
# PARTE 1: EXECUÇÃO DO CÓDIGO COM BUG PROPOSITADO (DIRETRIZ 6)
def mdc_euclides_INCORRETA_SOBRESCRITA(a: int, b: int) -> int:
    """
    Simula um erro imperativo clássico: as atualizações de estado dependentes 
    são feitas em sequência sem variável temporária, destruindo o valor 
    de 'a' prematuramente e colapsando o invariante matemático.
    """
    assert a > 0 and b >= 0, "Erro: Pre-condicoes violadas (a > 0 e b >= 0)!"
    
    original_a, original_b = a, b
    
    # Invariante inicial válido
    assert math.gcd(a, b) == math.gcd(original_a, original_b), "Erro de inicializacao"

    while b > 0:
        velha_variante = b
        
        # <<< O ERRO PROPOSITADO >>>
        a = b
        b = a % b # Como a == b agora, b será sempre 0 prematuramente
        
        # Checagem de Manutenção vai estourar imediatamente na 1ª iteração
        assert math.gcd(a, b) == math.gcd(original_a, original_b), (
            f"Erro: Invariante aniquilado por sobrescrita! "
            f"mdc(novo_a={a}, novo_b={b}) = {math.gcd(a, b)}, "
            f"esperado {math.gcd(original_a, original_b)}"
        )
        
        assert b < velha_variante, "Falta de progresso"

    return a

def demonstrar_falha_diretriz_6():
    print("=" * 72)
    print("DIRETRIZ 6 -- Diagnóstico de Falha Lógica (State Overwrite)")
    print("Data Set oficial: a=48, b=18 (MDC esperado = 6)")
    print("-" * 72)
    try:
        mdc_euclides_INCORRETA_SOBRESCRITA(48, 18)
    except AssertionError as e:
        print(f"-> AssertionError CAPTURADA com sucesso:\n   {e}")
        print("\nExplicação da Falha:")
        print("A ausência de simultaneidade na atribuição destruiu o estado de 'a'.")
        print("O valor passou a ser 18, forçando 'b' a calcular 18 % 18 = 0.")
        print("O invariante lógico foi irremediavelmente perdido.")
    print("=" * 72 + "\n")


# PARTE 2: IMPLEMENTAÇÃO VERIFICADA (CORREÇÃO TOTAL)
def mdc_euclides_verified(a: int, b: int) -> int:
    """
    Implementação rigorosa. Utiliza desempacotamento de tuplas do Python 
    para garantir transição de estado atômica.
    """
    # 1. ASSERÇÃO DE PRÉ-CONDIÇÃO
    assert a > 0 and b >= 0, "Erro: Pre-condicoes violadas (a > 0 e b >= 0)!"
    
    original_a, original_b = a, b

    # 2. ASSERÇÃO DE INICIALIZAÇÃO (CASO BASE)
    assert math.gcd(a, b) == math.gcd(original_a, original_b), \
        "Erro: Invariante falhou na inicializacao!"

    while b > 0:
        # Preparação para limite inferior e métrica de progresso
        velha_variante = b
        assert velha_variante >= 0, "Erro: Variante violou o limite inferior!"

        # Transição Atômica (O Lema de Euclides é garantido aritmeticamente)
        a, b = b, a % b

        # 3. ASSERÇÃO DE MANUTENÇÃO (PASSO INDUTIVO)
        assert math.gcd(a, b) == math.gcd(original_a, original_b), \
            "Erro: Invariante violado durante o laço!"
        
        # 4. ASSERÇÃO DE DECREMENTO (TERMINAÇÃO)
        assert b < velha_variante, \
            "Erro: Loop em execucao infinita (sem progresso monotonicamente decrescente)!"

    # 5. ASSERÇÃO DE PÓS-CONDIÇÃO (DEDUÇÃO FINAL)
    assert a == math.gcd(original_a, original_b), \
        "Erro: A pos-condicao falhou na deducao final!"
        
    return a


def testes_de_robustez():
    print("Executando Bateria de Testes Formal na Versão Verificada...")
    
    # Teste 1: Data set e casos clássicos
    casos = [(48, 18, 6), (101, 10, 1), (54, 24, 6), (7, 0, 7)]
    for a, b, esperado in casos:
        assert mdc_euclides_verified(a, b) == esperado
    print("-> Casos base e limites operacionais OK.")

    # Teste 2: Fuzzing extremo contra a biblioteca padrão do Python
    random.seed(42)
    for _ in range(10_000):
        a = random.randint(1, 2_000_000)
        b = random.randint(0, 2_000_000)
        assert mdc_euclides_verified(a, b) == math.gcd(a, b)
    print("-> Fuzzing (10.000 amostras aleatórias) concluído sem divergências.")
    print("-> Correção Total atestada.")


if __name__ == "__main__":
    demonstrar_falha_diretriz_6()
    testes_de_robustez()