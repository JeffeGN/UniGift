import matplotlib
matplotlib.use("Agg")

import pytest
import pandas as pd
import matplotlib.pyplot as plt

from src.plots import (
    plot_barv,
    plot_barh,
    plot_pizza
)

def test_plot_barv_executa_sem_erro():
    df = pd.DataFrame({
        "Perfil": ["A", "B", "C"],
        "Valor": [100, 200, 300]
    })
    plot_barv(df, col_valor="Valor", col_categoria="Perfil")
    plt.close()  # Fecha a figura

def test_plot_barh_executa_sem_erro():
    df = pd.DataFrame({
        "Segmento": ["X", "Y", "Z"],
        "Faturamento": [1000, 5000, 3000]
    })
    plot_barh(df, col_valor="Faturamento", col_categoria="Segmento")
    plt.close()

def test_plot_pizza_executa_sem_erro():
    df = pd.DataFrame({
        "Categoria": ["Eletrônicos", "Roupas", "Livros"],
        "Fatia": [0.4, 0.35, 0.25]
    })
    plot_pizza(df, col_valor="Fatia", col_categoria="Categoria", exibir_percentual=True)
    plt.close()
