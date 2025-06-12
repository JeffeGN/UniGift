import pandas as pd
import numpy as np

########################################

def calc_transacoes(df):
    # Calcula a média de InvoiceNo por país individualmente
    transacoes_unicas = df.groupby("Country")["InvoiceNo"].nunique().sort_values(ascending=False)
    transacoes_unicas = pd.DataFrame(transacoes_unicas).reset_index().rename(columns={"InvoiceNo":"Unique"})
    transacoes_totais = df.groupby("Country")["InvoiceNo"].value_counts().sort_values(ascending=False)
    transacoes_totais = pd.DataFrame(transacoes_totais).reset_index().rename(columns={"count":"Total"})
    transacoes_totais = transacoes_totais.groupby("Country")["Total"].sum().reset_index().sort_values(by="Total", ascending=False).reset_index().drop(columns=["index"])
    transacoes = pd.DataFrame({"Country": transacoes_totais["Country"], "Unique": transacoes_unicas["Unique"], "Media": transacoes_totais["Total"] / transacoes_unicas["Unique"], "Total": transacoes_totais["Total"]})
    return transacoes

########################################

def criar_rfv(
    df,
    customer_col="CustomerID",
    date_col="InvoiceDate",
    invoice_col="InvoiceNo",
    quantity_col="Quantity",
    price_col="UnitPrice"
):
    """
    Calcula a análise RFV (Recency, Frequency, Value) para um DataFrame customizado.

    Parâmetros:
    - df: DataFrame com os dados de transações
    - customer_col: coluna de ID do cliente
    - date_col: coluna com a data da transação
    - invoice_col: coluna identificadora única de cada compra
    - quantity_col: coluna com a quantidade do item
    - price_col: coluna com o preço unitário do item

    Retorna:
    - DataFrame com métricas RFV, scores e perfis de cliente
    """

    # Calcula o valor total de cada linha (quantidade × preço)
    df["TotalPrice"] = df[quantity_col] * df[price_col]

    # Define a última data da base como referência para o cálculo da Recency
    data_ultima_transacao = df[date_col].max()

    # Agrupa por cliente e calcula as métricas RFV
    rfv = df.groupby(df[customer_col]).agg({
        date_col: lambda x: (data_ultima_transacao - x.max()).days,  # Recency
        invoice_col: "nunique",                                     # Frequency
        "TotalPrice": "sum"                                         # Value
    }).reset_index()

    # Renomeia as colunas
    rfv.columns = [customer_col, "Recency", "Frequency", "Value"]

    # Calcula os scores por tercis (ou regra personalizada)
    rfv["RScore"] = pd.qcut(rfv["Recency"], q=3, labels=[3, 2, 1]).astype(int)

    def get_fscore(f):
        if f > 5:
            return 3
        elif f >= 3:
            return 2
        else:
            return 1

    rfv["FScore"] = rfv["Frequency"].apply(get_fscore)
    rfv["VScore"] = pd.qcut(rfv["Value"], q=3, labels=[1, 2, 3]).astype(int)

    # Soma dos scores RFV
    rfv["RFV"] = rfv["RScore"] + rfv["FScore"] + rfv["VScore"]

    # Classificação final dos perfis
    def segmentar_cliente(score):
        if score >= 8:
            return "Clientes VIP"
        elif score >= 5:
            return "Clientes Emergentes"
        else:
            return "Clientes Churn"

    rfv["Profile"] = rfv["RFV"].apply(segmentar_cliente)

    return rfv

########################################

def calc_proporcao_rfv(rfv):
    rfv = rfv["Profile"].value_counts(normalize=True).reset_index().rename(columns={"proportion":"Proportion"})
    return rfv

########################################

def calc_migracoes_rfv(df):
    # 1. Extrai o mês da transação
    df["MonthReference"] = df["InvoiceDate"].dt.to_period("M")
    
    # 2. Cálculo mensal de RFV com classificação por perfil
    def calcular_rfv_mensal(df):
        resultados = []
    
        for mes in sorted(df["MonthReference"].unique()):
            df_mes = df[df["MonthReference"] == mes]
    
            rfm = (
                df_mes.groupby("CustomerID")
                .agg({
                    "InvoiceDate": lambda x: (df_mes["InvoiceDate"].max() - x.max()).days,
                    "InvoiceNo": "nunique",
                    "TotalPrice": "sum"
                })
                .reset_index()
            )
            rfm.columns = ["CustomerID", "Recency", "Frequency", "Monetary"]
    
            rfm["R_score"] = pd.qcut(rfm["Recency"], 3, labels=[3, 2, 1])
            rfm["F_score"] = pd.qcut(rfm["Frequency"].rank(method="first"), 3, labels=[1, 2, 3])
            rfm["M_score"] = pd.qcut(rfm["Monetary"], 3, labels=[1, 2, 3])
    
            rfm["RFV"] = rfm["R_score"].astype(str) + rfm["F_score"].astype(str) + rfm["M_score"].astype(str)
    
            def classificar(rfv):
                if rfv == "333":
                    return "Clientes VIP"
                elif rfv.startswith("3") or rfv.endswith("3"):
                    return "Clientes Emergentes"
                elif rfv.startswith("1") and rfv.endswith("1"):
                    return "Clientes Churn"
                else:
                    return "Clientes Regulares"
    
            rfm["Profile"] = rfm["RFV"].apply(classificar)
            rfm["MonthReference"] = mes
            resultados.append(rfm[["CustomerID", "MonthReference", "Profile"]])
    
        return pd.concat(resultados, ignore_index=True)
    
    # 3. Aplica o cálculo mensal de RFV
    rfv = calcular_rfv_mensal(df)
    
    # 4. Faz o merge para obter df_rfv com perfis mensais
    df_rfv = df.merge(rfv, on=["CustomerID", "MonthReference"], how="left")
    
    # 5. Prepara perfil mensal por cliente
    monthly_profiles = (
        df_rfv.groupby(["CustomerID", "MonthReference"])["Profile"]
        .first()
        .reset_index()
        .sort_values(by=["CustomerID", "MonthReference"])
    )
    
    # 6. Cria coluna de perfil anterior
    monthly_profiles["PreviousProfile"] = monthly_profiles.groupby("CustomerID")["Profile"].shift(1)
    
    # 7. Filtra migrações de Emergentes para VIP
    migrations = monthly_profiles[
        (monthly_profiles["PreviousProfile"] == "Clientes Emergentes") &
        (monthly_profiles["Profile"] == "Clientes VIP")
    ]
    
    # 8. Conta número de migrações por mês
    migrations_by_month = migrations.groupby("MonthReference")["CustomerID"].nunique().reset_index()
    migrations_by_month.columns = ["Month", "NumMigrations"]
    return migrations_by_month

########################################

def calc_retencao_rfv(df):
    """
    Calcula a matriz de retenção percentual média por perfil RFV ao longo dos meses.

    Retorna:
    - retencao_rfv: DataFrame com os meses como linhas e os perfis RFV como colunas
    """

    df["MonthReference"] = df["InvoiceDate"].dt.to_period("M")

    def calcular_rfv_mensal(df):
        resultados = []

        for mes in sorted(df["MonthReference"].unique()):
            df_mes = df[df["MonthReference"] == mes]

            rfv = (
                df_mes.groupby("CustomerID")
                .agg({
                    "InvoiceDate": lambda x: (df_mes["InvoiceDate"].max() - x.max()).days,
                    "InvoiceNo": "nunique",
                    "TotalPrice": "sum"
                })
                .reset_index()
            )
            rfv.columns = ["CustomerID", "Recency", "Frequency", "Value"]
            rfv["RScore"] = pd.qcut(rfv["Recency"], 3, labels=[3, 2, 1]).astype(int)

            def get_fscore(f):
                return 3 if f > 5 else 2 if f >= 3 else 1

            rfv["FScore"] = rfv["Frequency"].apply(get_fscore)
            rfv["VScore"] = pd.qcut(rfv["Value"], 3, labels=[1, 2, 3]).astype(int)
            rfv["RFV"] = rfv["RScore"] + rfv["FScore"] + rfv["VScore"]

            def segmentar(score):
                return "Clientes VIP" if score >= 8 else "Clientes Emergentes" if score >= 5 else "Clientes Churn"

            rfv["Profile"] = rfv["RFV"].apply(segmentar)
            rfv["MonthReference"] = mes
            resultados.append(rfv[["CustomerID", "MonthReference", "Profile"]])

        return pd.concat(resultados, ignore_index=True)

    rfv = calcular_rfv_mensal(df)
    df_rfv = df.merge(rfv, on=["CustomerID", "MonthReference"], how="left")

    presenca = (
        df_rfv.groupby(["CustomerID", "MonthReference"])["Profile"]
        .first()
        .reset_index()
    )

    clientes_mes = (
        presenca
        .assign(Presente=1)
        .pivot_table(index="CustomerID", columns="MonthReference", values="Presente", fill_value=0)
    )

    perfil_inicial = (
        presenca
        .sort_values(by="MonthReference")
        .groupby("CustomerID")["Profile"]
        .first()
        .reset_index()
    )

    clientes_mes = clientes_mes.merge(perfil_inicial, on="CustomerID", how="left")

    perfil = clientes_mes["Profile"]
    clientes_mes = clientes_mes.drop(columns="Profile")

    # ⚠️ Mantém somente colunas numéricas
    clientes_mes = clientes_mes.select_dtypes(include=["number"])

    retencao_rfv = clientes_mes.groupby(perfil).mean().T
    retencao_rfv.index.name = "Month"
    retencao_rfv.reset_index(inplace=True)

    return retencao_rfv
