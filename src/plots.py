import matplotlib.pyplot as plt

#######################################

def format_milhar(valor, decimais=True, simbolo=""):
    """
    Formata um valor numérico com notação abreviada:
    - 'k' para milhar (ex: 2.500 → 2,50k)
    - 'kk' para milhão (ex: 2.500.000 → 2,50kk)

    Parâmetros:
    - valor: número a ser formatado
    - decimais: se False, arredonda sem casas decimais
    - simbolo: string prefixada aos valores (ex: "R$", "$", etc.)

    Retorna:
    - string com o valor formatado no padrão 'simbolo + valor + sufixo'
    """

    # Proteção contra alterações acumuladas
    valor = valor.copy() 
    
    # Define a base e o sufixo com base na escala do valor
    if valor >= 1_000_000:
        sufixo = "kk"
        base = valor / 1_000_000
    elif valor >= 1_000:
        sufixo = "k"
        base = valor / 1_000
    else:
        sufixo = ""
        base = valor

    # Formata com ou sem casas decimais e aplica o símbolo e o sufixo
    if decimais:
        return f"{simbolo}{base:,.2f}{sufixo}".replace(",", ".")
    else:
        return f"{simbolo}{int(round(base)):,}{sufixo}".replace(",", ".")


######################################

def plot_barh(
    transacoes,
    col_valor,
    col_categoria,
    col_rotulo=None,
    titulo=None,
    log=True,
    cor="steelblue",
    exibir_percentual=False,
    ordenar_por_valor=True,
    contorno_barras=True,
    decimais=True,
    milhar=False,
    simbolo=""
):
    """
    Plota um gráfico de barras horizontais com:
    - rótulos personalizados ao lado das barras
    - opção de escala logarítmica
    - formato monetário com símbolo e abreviação visual (k, kk)

    Parâmetros:
    - transacoes: DataFrame com os dados
    - col_valor: coluna numérica
    - col_categoria: coluna das categorias no eixo Y
    - col_rotulo: coluna auxiliar para compor o rótulo (opcional)
    - titulo: título do gráfico (opcional)
    - log: se True, aplica escala logarítmica no eixo X
    - cor: cor das barras
    - exibir_percentual: se True, exibe proporções no lugar dos valores absolutos
    - ordenar_por_valor: se True, ordena do menor para o maior valor
    - contorno_barras: se True, adiciona contorno preto nas barras
    - decimais: se False, remove casas decimais dos rótulos
    - milhar: se True, formata os valores como k / kk
    - simbolo: string prefixada aos valores (ex: "R$")
    """

    # Proteção contra alterações acumuladas
    transacoes = transacoes.copy() 
    
    # Ordena os dados por valor ou categoria
    if ordenar_por_valor:
        transacoes = transacoes.sort_values(by=col_valor, ascending=True)
    else:
        transacoes = transacoes.sort_values(by=col_categoria, ascending=True)

    # Define a função de formatação para os valores exibidos nos rótulos
    if exibir_percentual:
        transacoes[col_valor] = transacoes[col_valor]
        format_valor = lambda v: f"{v:,.0%}" if not decimais else f"{v:,.2%}"
    else:
        format_valor = (
    lambda v: format_milhar(v, decimais=decimais, simbolo=simbolo)
    if milhar else (
        f"{simbolo}{v:,.0f}" if not decimais else f"{simbolo}{v:,.2f}"
        )
    )


    # Gera os rótulos compostos por nome da categoria e valor
    if col_rotulo:
        transacoes["label"] = transacoes.apply(
            lambda row: f"{row[col_rotulo]} ({row[col_categoria]} - {format_valor(row[col_valor])})", axis=1
        )
    else:
        transacoes["label"] = transacoes.apply(
            lambda row: f"{row[col_categoria]} ({format_valor(row[col_valor])})", axis=1
        )

    # Define a coluna de rótulo como índice do gráfico
    transacoes = transacoes.set_index("label")

    # Cria a figura e o gráfico de barras horizontais
    plt.figure(figsize=(10, 8))
    transacoes[col_valor].plot(
        kind="barh",
        color=cor,
        edgecolor="black" if contorno_barras else None
    )

    # Remove bordas externas do gráfico
    ax = plt.gca()
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Remove marcas dos eixos e limpa visualmente o gráfico
    ax.tick_params(axis='both', which='both',
                   bottom=False, top=False,
                   left=False, right=False,
                   labelbottom=False, labelleft=True)
    ax.xaxis.set_ticks([])
    ax.xaxis.set_tick_params(which='minor', bottom=False)

    # Aplica escala logarítmica no eixo X, se necessário
    if log:
        plt.xscale("log")

    # Usa título padrão se nenhum for fornecido
    if not titulo:
        titulo = f"{col_valor} por {col_categoria}"

    # Define título e finaliza layout
    plt.title(titulo, fontsize=14)
    plt.xlabel("")
    plt.ylabel("")
    plt.grid(False)
    plt.tight_layout()
    plt.show()



######################################

def plot_barv(
    transacoes,
    col_valor,
    col_categoria,
    col_rotulo=None,
    titulo=None,
    log=True,
    exibir_percentual=False,
    compacto=False,
    ordenar_por_valor=True,
    contorno_barras=True,
    usar_cores=True,
    decimais=True,
    milhar=False,
    simbolo=""
):
    """
    Plota um gráfico de barras verticais com:
    - rótulos personalizados acima das barras
    - suporte a múltiplas cores por categoria
    - formato monetário com símbolo e abreviação visual (k, kk)
    """

    # Garante que o DataFrame original não seja alterado
    transacoes = transacoes.copy()
   
    # Agrupa os dados por categoria ao exibir percentuais
    if exibir_percentual:
        agrupado = transacoes.groupby(col_categoria, as_index=False)[col_valor].sum()
        agrupado[col_valor] = agrupado[col_valor]
        agrupado["label"] = agrupado[col_categoria]
        transacoes = agrupado
        format_valor = lambda v: f"{v:,.0%}" if not decimais else f"{v:,.2%}"
    else:
        format_valor = lambda v: format_milhar(v, decimais=decimais, simbolo=simbolo) if milhar else (
            f"{simbolo}{v:,.0f}" if not decimais else f"{simbolo}{v:,.2f}"
        )

        # Cria coluna de rótulo se for informada uma coluna auxiliar
        if col_rotulo:
            transacoes["label"] = transacoes.apply(
                lambda row: f"{row[col_rotulo]} ({row[col_categoria]})", axis=1
            )
        else:
            transacoes["label"] = transacoes[col_categoria]

    # Ordena os dados conforme desejado
    if ordenar_por_valor:
        transacoes = transacoes.sort_values(by=col_valor, ascending=False)
    else:
        transacoes = transacoes.sort_values(by=col_categoria)

    # Define cores para as barras
    if usar_cores:
        categorias = transacoes[col_categoria].unique()
        cmap = plt.get_cmap("Set2")
        cores = {cat: cmap(i) for i, cat in enumerate(categorias)}
        cores_barras = transacoes[col_categoria].map(cores)
    else:
        cores_barras = "steelblue"

    # Usa coluna de rótulo como índice
    transacoes = transacoes.set_index("label")

    # Cria o gráfico
    plt.figure(figsize=(12, 6))
    ax = transacoes[col_valor].plot(
        kind="bar",
        color=cores_barras,
        edgecolor="black" if contorno_barras else None,
        width=0.8 if not compacto else 1.0
    )

    # Estética
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=0, ha="center")
    ax.tick_params(axis='y', which='both', left=False, labelleft=False)

    # Rótulos nas barras
    for i, v in enumerate(transacoes[col_valor]):
        ax.text(i, v, format_valor(v), ha="center", va="bottom", fontsize=10)

    # Legenda de cores, se usada
    if usar_cores:
        legendas = [
            plt.Line2D([0], [0], marker='s', color='none', label=cat, markerfacecolor=cor, markersize=10)
            for cat, cor in cores.items()
        ]
        ax.legend(handles=legendas, loc='upper right', title=col_categoria)

    # Título do gráfico
    if not titulo:
        titulo = f"{col_valor} por {col_categoria}"
    plt.title(titulo, fontsize=14)
    plt.xlabel("")
    plt.ylabel("")
    plt.tight_layout()
    plt.show()

######################################

def plot_pizza(
    transacoes,
    col_valor,
    col_categoria,
    titulo=None,
    exibir_percentual=True,
    usar_cores=True,
    decimais=True,
    ordenar_por_valor=True,
    milhar=False,
    simbolo=""
):
    """
    Plota um gráfico de pizza com:
    - rótulos personalizados
    - suporte a cores distintas ou cor única
    - formato monetário com símbolo e abreviação visual (k, kk)

    Parâmetros:
    - transacoes: DataFrame com os dados
    - col_valor: coluna numérica
    - col_categoria: coluna das categorias
    - titulo: título do gráfico (opcional)
    - exibir_percentual: se True, mostra porcentagem; senão, valores reais
    - usar_cores: se False, usa cor única
    - decimais: se False, remove casas decimais dos rótulos
    - ordenar_por_valor: se True, ordena do maior para o menor
    - milhar: se True, formata os valores como k / kk
    - simbolo: string prefixada aos valores (ex: "R$")
    """

     # Proteção contra alterações acumuladas
    transacoes = transacoes.copy() 
    
    
    # Ordena as categorias com base no valor ou no nome
    if ordenar_por_valor:
        transacoes = transacoes.sort_values(by=col_valor, ascending=False)
    else:
        transacoes = transacoes.sort_values(by=col_categoria)

    # Extrai os valores numéricos e os nomes das categorias
    valores = transacoes[col_valor].values
    categorias = transacoes[col_categoria].values

    # Define os rótulos a serem exibidos nas fatias
    if exibir_percentual:
        # Calcula proporções para exibição percentual
        proporcoes = valores
        format_valor = lambda v: f"{v:,.0%}" if not decimais else f"{v:,.2%}"
        labels = [f"{cat} ({format_valor(p)})" for cat, p in zip(categorias, proporcoes)]
    else:
        # Formata os valores com símbolo e notação k/kk se necessário
        labels = [f"{cat} ({format_milhar(v, decimais=decimais, simbolo=simbolo)})"
          if milhar else f"{cat} ({simbolo}{v:,.0f})" if not decimais
          else f"{cat} ({simbolo}{v:,.2f})"
          for cat, v in zip(categorias, valores)]


    # Define as cores da paleta se ativado
    if usar_cores:
        cmap = plt.get_cmap("Set2")
        cores = [cmap(i % cmap.N) for i in range(len(categorias))]
    else:
        cores = ["steelblue"] * len(categorias)

    # Cria a figura do gráfico
    plt.figure(figsize=(8, 8))

    # Plota o gráfico de pizza com os parâmetros visuais definidos
    plt.pie(
        valores,
        labels=labels,
        colors=cores,
        startangle=90,
        counterclock=False,
        wedgeprops={"edgecolor": "black"}  # contorno das fatias
    )

    # Define um título padrão se nenhum for informado
    if not titulo:
        titulo = f"{col_valor} por {col_categoria}"

    # Aplica o título e finaliza o layout
    plt.title(titulo, fontsize=14)
    plt.tight_layout()
    plt.show()
