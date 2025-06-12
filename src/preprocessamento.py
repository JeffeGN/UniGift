import pandas as pd
import numpy as np

def carregar_dados(caminho):
    df = pd.read_csv(caminho, encoding="ISO-8859-1", dtype=str, low_memory=False)
    return df


def remover_outliers_iqr(df, coluna, k=1.5):
    """
    Remove outliers de uma coluna numérica com base na regra do IQR (Intervalo Interquartil).

    Parâmetros:
        df (DataFrame): DataFrame original.
        coluna (str): Nome da coluna numérica a ser filtrada.
        k (float): Multiplicador do IQR para definir os limites (default=1.5).

    Retorna:
        DataFrame: DataFrame com os outliers da coluna removidos.
    """
    Q1 = df[coluna].quantile(0.25)
    Q3 = df[coluna].quantile(0.75)
    IQR = Q3 - Q1
    filtro = (df[coluna] >= Q1 - k * IQR) & (df[coluna] <= Q3 + k * IQR)
    return df[filtro]


def corrigir_tipos_e_datas(df):
    """
    Corrige tipos de dados e extrai data e hora da coluna InvoiceDate.

    Parâmetros:
        df (DataFrame): DataFrame original com colunas brutas.

    Retorna:
        DataFrame: DataFrame com tipos corrigidos e colunas InvoiceDate e InvoiceTime separadas.
    """
    df = df.copy()

    # Conversões de tipo
    df["InvoiceNo"] = df["InvoiceNo"].astype(str)
    df["StockCode"] = df["StockCode"].astype(str)
    df["Description"] = df["Description"].astype(str)
    df["Quantity"] = df["Quantity"].astype(np.int64)
    df["UnitPrice"] = df["UnitPrice"].astype(np.float64)
    df["CustomerID"] = df["CustomerID"].astype(str)
    df["Country"] = df["Country"].astype(str)

    # Conversão de data e extração de hora
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%d-%m-%Y %H:%M")
    df["InvoiceTime"] = df["InvoiceDate"].dt.time
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"], format="%d/%m/%Y %H:%M")



    # Reorganização das colunas
    colunas = [
        "InvoiceNo", "StockCode", "Description", "Quantity",
        "InvoiceDate", "InvoiceTime", "UnitPrice", "CustomerID", "Country"
    ]
    df = df[colunas]

    return df

def preparar_dados_para_graficos(caminho):
    df = carregar_dados(caminho)
    df = corrigir_tipos_e_datas(df)
    df["Valor"] = df["UnitPrice"].astype(float) * df["Quantity"].astype(float)

    # Calcula o preço médio ponderado por país
    df_filtrado = df[df["Quantity"] > 0].copy()
    df_filtrado["ValorTotal"] = df_filtrado["UnitPrice"] * df_filtrado["Quantity"]

    preco_medio_por_pais = (
        df_filtrado.groupby("Country", group_keys=False)
        .apply(lambda x: x["ValorTotal"].sum() / x["Quantity"].sum())
        .sort_values(ascending=False)
        .reset_index(name="PrecoUnitarioMedio")
    )

    df = df.merge(preco_medio_por_pais, on="Country", how="left")
    return df



