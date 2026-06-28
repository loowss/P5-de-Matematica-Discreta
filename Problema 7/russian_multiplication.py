import random
import math

# PARTE 1: IMPLEMENTAÇÃO VERIFICADA (DIRETRIZES 1 A 5)
def russian_multiplication_verified(a: int, b: int) -> int:
    assert a >= 0 and b >= 0, "Erro: Pre-condicoes devem ser naturais!"
    res, original_a, original_b = 0, a, b
    
    assert res + (a * b) == (original_a * original_b), "Erro: Invariante na inicializacao!"

    while a > 0:
        velha_variante = a
        assert velha_variante >= 0, "Erro: Variante violou o limite inferior!"

        if a % 2 != 0:
            res += b

        a, b = a // 2, b * 2

        assert res + (a * b) == (original_a * original_b), "Erro: Invariante violado no corpo do loop!"
        assert a < velha_variante, "Erro: Loop em execucao infinita (sem progresso)!"

    assert res == (original_a * original_b), "Erro: A pos-condicao falhou na terminacao!"
    return res

# PARTE 2: ANÁLISE DE FALHA — DIRETRIZ 6 (ERRO SEMÂNTICO)
def demonstrar_falha_diretriz_6(a: int, b: int):
    """
    PONTO DE FALHA: Atualizacao precoce de b. O multiplicador e dobrado 
    ANTES da acumulacao condicional, alterando a aritmetica do algoritmo.
    """
    res, original_a, original_b = 0, a, b
    while a > 0:
        b = b * 2  # <<< ERRO SEMÂNTICO: Atualizacao precoce corrompe o invariante
        if a % 2 != 0:
            res += b
        a = a // 2
        
        # A assercao estoura porque a matematica foi corrompida.
        assert res + (a * b) == original_a * original_b, (
            f"Invariante violado por erro aritmetico! "
            f"res={res}, a={a}, b={b} -> "
            f"res + a*b = {res + a * b} != {original_a * original_b}"
        )
    return res

# PARTE 3: BATERIA DE TESTES DE ROBUSTEZ
def testes_de_robustez():
    for a, b, esperado in [(11, 3, 33), (0, 7, 0), (0, 0, 0), (1, 1, 1), (1023, 17, 17391), (50000, 0, 0)]:
        assert russian_multiplication_verified(a, b) == esperado
    
    random.seed(42)
    for _ in range(10_000):
        a, b = random.randint(0, 50_000), random.randint(0, 50_000)
        assert russian_multiplication_verified(a, b) == a * b

if __name__ == "__main__":
    print("Iniciando bateria de avaliacao formal...")
    
    try:
        demonstrar_falha_diretriz_6(11, 3)
    except AssertionError as e:
        print(f"-> [Diretriz 6 OK] Falha semantica capturada com sucesso: {e}")
        
    testes_de_robustez()
    print("-> [Diretrizes 1-5 OK] Todos os testes passaram com sucesso na versao verificada.")