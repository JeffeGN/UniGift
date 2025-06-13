import matplotlib.pyplot as plt
import pandas as pd
import pytest

# Importa a função a ser testada e ferramentas para arredondamento preciso
from src.plots import format_milhar
from decimal import Decimal, ROUND_DOWN

# Função que reduz valores numéricos e acrescenta sufixos ("k", "kk") para facilitar leitura
def format_milhar(valor, decimais=True, simbolo=""):
    # Define o sufixo com base no valor recebido
    if valor >= 1_000_000:
        sufixo = "kk"
        base = Decimal(valor) / Decimal(1_000_000)
    elif valor >= 1_000:
        sufixo = "k"
        base = Decimal(valor) / Decimal(1_000)
    else:
        sufixo = ""
        base = Decimal(valor)

    # Se for para exibir com casas decimais
    if decimais:
        # Limita a duas casas decimais sem arredondar pra cima
        base = base.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        return f"{simbolo}{base:,.2f}{sufixo}".replace(",", ".")  # Ajusta formatação para estilo com ponto
    else:
        # Arredonda normalmente e remove casas decimais
        return f"{simbolo}{int(round(base + Decimal("1e-6"))):,}{sufixo}".replace(",", ".")

# Testes automatizados cobrindo cenários de limite (bordas)
@pytest.mark.parametrize("valor, decimais, esperado", [
    (0, True, "0.00"),                      # valor zero
    (-500, True, "-500.00"),                # número negativo
    (999, True, "999.00"),                  # abaixo de 1k
    (1000, True, "1.00k"),                  # exatamente 1k
    (999_999, True, "999.99k"),             # abaixo de 1kk
    (1_000_000, True, "1.00kk"),            # exatamente 1kk
    (1_000_001, False, "1kk"),              # acima de 1kk sem decimais
    (1250.75, True, "1.25k"),               # valor quebrado com decimais
    (1250.75, False, "1k"),                 # valor quebrado arredondado (sem decimais)
])
def test_format_milhar_casos_de_borda(valor, decimais, esperado):
    # Compara o resultado da função com o resultado esperado em cada caso
    assert format_milhar(valor, decimais=decimais) == esperado
