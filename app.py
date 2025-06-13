import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from src.plots import plot_barh, plot_barv, plot_pizza

st.set_page_config(layout="wide")
st.title("📦 Dashboard UniGift")

def render(func, *args, **kwargs):
    plt.clf()
    func(*args, **kwargs)
    st.pyplot(plt.gcf())
    st.markdown("---")

# Dados
transacoes = pd.read_csv("data/dashboards/transacoes.csv")
media_preco = pd.read_csv("data/dashboards/media_preco.csv")
top_vendas_pais = pd.read_csv("data/dashboards/top_vendas_pais.csv")
margem_lucro = pd.read_csv("data/dashboards/margem_lucro.csv")
preferencias = pd.read_csv("data/dashboards/preferencias.csv")
proporcao_rfv = pd.read_csv("data/dashboards/proporcao_rfv.csv")
faturamento_rfv = pd.read_csv("data/dashboards/faturamento_rfv.csv")
migracoes_rfv = pd.read_csv("data/dashboards/migracoes_rfv.csv")
retencao_rfv = pd.read_csv("data/dashboards/retencao_rfv.csv")

if "grafico_ativo" not in st.session_state:
    st.session_state.grafico_ativo = None

graficos = {
    "Média de produtos por transação": lambda: (
        render(
            plot_barh, transacoes,
            col_categoria="Country", col_valor="Media",
            titulo="Média de produtos por transação"
        ),
        st.markdown("""
### Com base nos dados analisados, podemos extrair alguns insights valiosos sobre o comportamento de compra internacional dos clientes da UniGift.

### 1. **Mercados com transações altamente concentradas**

Países como **Estados Unidos (32 produtos/transação)**, **Singapura (30,2)**, **Japão (27,5)**, **Portugal (27,4)** e **Brasil (25)** apresentam médias de produtos por pedido significativamente acima da média geral. Isso indica que nesses mercados, mesmo com menor volume absoluto de compras, os pedidos realizados são mais robustos e concentrados — sinalizando uma estratégia deliberada por parte dos consumidores: comprar mais em menos pedidos.

Esse comportamento pode ser atribuído a **fatores logísticos**, como fretes internacionais mais caros, impostos de importação e prazos de entrega mais longos. Dessa forma, os consumidores optam por pedidos mais completos, compensando o custo e tempo envolvidos na operação.

---

### 2. **Reino Unido: volume elevado, mas dispersão nas transações**

O Reino Unido apresenta média de 20,1 produtos por transação — abaixo de mercados mais distantes — mas domina amplamente em **volume total** (305.129 itens vendidos) e em número de pedidos (15.144 clientes únicos). Isso sugere:

- Uma **frequência maior de compras** com volume menor por pedido
- **Fácil acesso logístico**, já que é o país-sede da UniGift
- Maior penetração da marca e fidelização local

Logo, apesar de a média por transação ser inferior, a combinação de frequência e acesso torna o Reino Unido o maior gerador de receita e volume geral.

---

### 3. **Oportunidades de internacionalização segmentada**

Vários mercados apresentam altas médias com **baixa base de clientes**, como:

- **Japão**: média de 27,5, com apenas 4 clientes
- **Brasil**: média de 25, com 1 cliente
- **Islândia**: média de 23,7, com 7 clientes
- **Malta** e **Emirados Árabes**: médias acima de 22

Esses países podem representar **nichos de oportunidade** para expansão controlada. Mesmo com base pequena, o perfil de compra já se mostra promissor em termos de valor por pedido.

---

### 4. **Cautela com distorções estatísticas**

Apesar das médias elevadas, é importante considerar que países com **poucas transações** têm valores suscetíveis a distorção. Por exemplo, um único cliente no Brasil fez uma compra com 25 itens — o que define toda a métrica do país. Por isso, análises mais profundas devem cruzar esse dado com recorrência, ticket médio e receita agregada.

---

### 5. **Insight estratégico**

A **média de produtos por transação** revela padrões ocultos de comportamento. Altas médias não significam necessariamente mercados consolidados, mas apontam **intenção de compra relevante**. Estratégias promocionais como frete grátis acima de determinado valor, kits personalizados ou campanhas “leve mais, pague menos” podem impulsionar ainda mais esse comportamento, especialmente em mercados onde o custo logístico é uma barreira.
""")
    ),

    "Média de preços por país": lambda: (
        render(
            plot_barh, media_preco,
            col_categoria="Country", col_valor="UnitPrice",
            simbolo="£", titulo="Média de preços por país"
        ),
        st.markdown("""
            Com base nos dados de preço médio por país da UniGift, observa-se que o **Brasil** apresenta a **maior média de preços unitários**, com **£3,29 por produto**, seguido de perto por **Líbano (£3,28)** e **Bahrein (£3,08)**. Estes valores estão consideravelmente acima da média de mercados mais consolidados, como o **Reino Unido**, onde o preço médio é **£2,19**.

Essa discrepância de preços revela padrões de mercado, operacionais e estratégicos que merecem atenção. Abaixo, uma análise detalhada com insights:

---

### 1. **Países com maiores médias de preço concentram-se em mercados distantes e pouco frequentes**

Os países com os preços médios mais altos — como Brasil, Líbano, Bahrein e Lituânia — possuem, em geral, **menor volume de vendas** e **número reduzido de transações**. Isso indica que nesses mercados a UniGift ainda opera de forma pontual, com uma oferta limitada e, possivelmente, baseada em produtos de ticket mais alto.

**Insight:** países com baixa recorrência de pedidos tendem a apresentar maior variabilidade de preço, sendo mais suscetíveis à composição do mix de produtos comercializados (itens premium, personalizados ou de baixa rotatividade).

---

### 2. **Influência logística sobre o preço final**

O Brasil e outros países do topo da lista estão geograficamente distantes da sede da UniGift. Isso sugere que fatores como **custo de envio, taxas de importação e barreiras alfandegárias** impactam diretamente o preço de comercialização. Além disso, esses mercados podem estar sujeitos a impostos diferenciados por país de destino, repassados integralmente ao consumidor final.

**Insight:** estratégias logísticas otimizadas (como centros de distribuição regionais ou parcerias locais) podem reduzir esses valores e tornar a marca mais competitiva em mercados em desenvolvimento.

---

### 3. **Descompasso entre preço e presença de marca**

No Reino Unido — país sede da empresa — o preço médio é relativamente mais baixo, mesmo com ampla presença da marca e grande volume de vendas. Isso sugere um **efeito de escala e maturidade comercial**: clientes locais têm maior acesso a promoções, canais alternativos de venda e menor custo de entrega.

Em contrapartida, os países com preços médios mais altos também são, em geral, mercados com **baixa penetração da marca**, indicando que o canal de venda pode ainda estar restrito a poucos itens ou aquisições pontuais.

---

### 4. **Oportunidades comerciais com base no perfil de consumo**

A alta disposição a pagar em mercados como Brasil, Singapura e Austrália pode representar **potencial de margem elevada** por unidade vendida. Mesmo com menor volume, o valor agregado por transação é mais expressivo. Isso pode justificar ações de marketing de nicho, produtos exclusivos ou coleções limitadas voltadas a esses perfis.

**Insight:** a UniGift pode explorar esse comportamento com estratégias de diferenciação em mercados distantes, oferecendo produtos premium e condições logísticas mais atrativas.

---

### Conclusão

A variação do preço médio por país vai além da simples precificação: ela reflete o grau de presença da marca, eficiência logística, carga tributária local e percepção de valor do consumidor em cada região. Países como Brasil e Líbano, embora ainda com baixo volume, demonstram **alto valor médio por item** — o que pode servir como indicativo estratégico de onde investir em expansão com maior retorno unitário.
""")
    ),

    "Produto mais vendido em cada país": lambda: (
        render(
            plot_barh, top_vendas_pais,
            col_categoria="Country", col_valor="Quantity",
            col_rotulo="Description", decimais=False,
            titulo="Produto mais vendido em cada país"
        ),
        st.markdown("""
        A análise do produto mais vendido em cada país revela padrões significativos de preferência regional, popularidade de determinadas linhas e pistas sobre a penetração da UniGift em diferentes mercados. A seguir, sintetizo os principais achados com base no gráfico de barras e no conjunto de dados fornecido:

---

### **Principais observações sobre os produtos mais vendidos por país**

1. **Predominância da linha “ZINC”**
   - Produtos como **ZINC WILLIE WINKIE CANDLE STICK**, **ZINC T-LIGHT HOLDER STARS SMALL**, **ZINC WIRE SWEETHEART LETTER TRAY** e **ZINC FOLKART SLEIGH BELLS** são os mais vendidos em diversos países europeus (Alemanha, Suécia, Noruega, Itália, Suíça, Irlanda, etc.).
   - Isso sugere que a linha “ZINC” tem **forte aceitação estética e funcional** nesses mercados, possivelmente por alinhar-se ao estilo decorativo europeu — rústico, prático e de apelo artesanal.

2. **Países com produtos únicos como líderes**
   - Em regiões como o **Brasil** (*SPACEBOY LUNCH BOX*), **Japão** (*WORLD WAR 2 GLIDERS ASSTD DESIGNS*), **Singapura** (*WOODEN UNION JACK BUNTING*) e **Líbano** (*WOODEN PICTURE FRAME WHITE FINISH*), o item mais vendido é distinto e não pertence à linha dominante nos demais países.
   - Isso indica **variações culturais ou preferências locais específicas**, bem como um portfólio adaptado ou limitado a determinados itens em mercados com menos diversidade de produtos oferecidos.

3. **Consistência nos volumes máximos**
   - A quantidade “25” aparece como valor modal para quase todos os países. O **Reino Unido**, por ser mercado doméstico, tem **27 unidades** do item mais vendido, enquanto **África do Sul (RSA)** e **Arábia Saudita** possuem apenas **12 unidades**.
   - Essa uniformidade pode ser resultado de pacotes promocionais padronizados, limites de estoque ou estratégias logísticas específicas. Já os menores valores refletem **baixa penetração comercial ou demanda residual**.

4. **Produtos com apelo universal**
   - Alguns itens se destacam pela **repetição em múltiplos países**, como:
     - *ZINC T-LIGHT HOLDER STARS SMALL* → França, Finlândia, Espanha, Países Baixos
     - *ZINC WILLIE WINKIE CANDLE STICK* → Alemanha, Áustria, Polônia, Noruega, Suécia
   - Esses produtos podem ser considerados **candidatos para campanhas globais**, pois seu sucesso é replicável em diferentes mercados.

---

### **Insights estratégicos com base na distribuição dos produtos mais vendidos**

- **Diversificação de portfólio por região**: Mercados como Japão, Brasil e República Tcheca indicam abertura a itens lúdicos, infantis ou com temática nostálgica. A UniGift pode explorar essa tendência com curadoria regional de produtos.

- **Adoção de produtos líderes como entrada comercial**: A linha “ZINC”, por sua ampla aceitação, pode ser utilizada como **porta de entrada para novos mercados**, consolidando uma base de consumidores fidelizados antes da introdução de novos itens.

- **Atenção aos mercados com baixa expressão volumétrica**: Países como RSA e Arábia Saudita, apesar de terem registrado vendas, apresentam baixo volume no item mais popular. Isso pode indicar presença marginal da marca, ou desafios logísticos ou culturais que merecem investigação.

- **Análise de sazonalidade e funcionalidade dos produtos líderes**: Alguns itens (ex. *WRAP CHRISTMAS VILLAGE* em Malta ou *ZINC FOLKART SLEIGH BELLS* em Portugal) têm potencial sazonal. A UniGift pode ativar **campanhas promocionais específicas por estação** e adaptar o ciclo de estoque conforme essas tendências.
        """)
    ),

    "Produtos com maior margem de lucro por país": lambda: (
        render(
            plot_barh, margem_lucro,
            col_categoria="Country", col_valor="UnitPrice",
            col_rotulo="Description", simbolo="£",
            titulo="Produtos com maior margem de lucro por país"
        ),
        st.markdown("""
        A análise dos produtos com maior valor unitário por país sugere padrões de preferência local, estrutura de portfólio e possíveis diferenças operacionais na oferta da UniGift. Como o gráfico evidencia os itens mais caros registrados por país, é razoável tratá-los como **representantes de maior margem de lucro potencial**, assumindo que o custo de aquisição seja uniforme entre mercados.

---

### **Principais observações sobre os produtos com maior preço por país**

1. **Produto recorrente entre países europeus: _PARISIENNE CURIO CABINET_**
   - Aparece como item mais caro em Bélgica, Alemanha, Espanha, Itália, Irlanda, Noruega, Channel Islands e Israel.
   - Seu preço de £7.50, o máximo observado, sugere que é um dos produtos premium do catálogo UniGift.
   - Essa recorrência indica forte aceitação da peça na Europa continental, reforçando seu apelo em mercados com estética mais clássica ou vintage.

2. **Presença do item _PACKING CHARGE_ com valor máximo em alguns países**
   - Irlanda (EIRE) e França registram “PACKING CHARGE” como produto de maior preço unitário, o que pode apontar para:
     - Erro de categorização ou ausência de vendas relevantes para o país, levando o sistema a computar taxas como produto.
     - Transações residuais ou não representativas.
   - Como esse “produto” não representa bem o portfólio da empresa, ele deve ser tratado como **outlier** na análise.

3. **Produtos únicos por país sugerem perfil de mercado diferenciado**
   - Exemplos incluem:
     - **Singapore** e **UK**: *BULL DOG BOTTLE TOP WALL CLOCK*
     - **Netherlands**: *GREEN METAL BOX ARMY SUPPLIES*
     - **Australia**: *70'S ALPHABET WALL ART*
     - **Canada**: *GRASS HOPPER WOODEN WALL CLOCK*
   - Esses itens são estilizados, com apelo visual ou temático, possivelmente direcionados a públicos mais jovens, urbanos ou que valorizam decoração com personalidade.

4. **Valor unitário como indicador de sofisticação ou limitação de mix**
   - Alguns países com menor presença da marca, como **Bahrein** ou **Czech Republic**, têm produtos de valor relativamente modesto (entre £4.95 e £5.45) como os mais caros. Isso pode ocorrer por:
     - Oferta restrita do mix UniGift nesses mercados.
     - Preferência local por itens de menor valor agregado.
     - Estratégia comercial ainda em fase inicial.

5. **Mercado doméstico alinhado com o portfólio internacional**
   - O Reino Unido apresenta como item de maior valor o mesmo que Singapura: *BULL DOG BOTTLE TOP WALL CLOCK*, também cotado a £7.50.
   - Isso sinaliza consistência no posicionamento da linha premium mesmo em mercados distintos, o que pode beneficiar campanhas globais com personalização mínima.

---

### **Insights estratégicos com base nessa visualização**

- **Produtos como _PARISIENNE CURIO CABINET_ e _BULL DOG WALL CLOCK_ devem ser priorizados em ações comerciais para mercados europeus**, pois são aceitos como itens de alto valor em diversas geografias.

- **A diversificação de produtos premium entre países com menor volume sugere a necessidade de ajustar o portfólio local.** Oferecer itens com estética similar à linha ZINC ou CURIO pode aumentar o ticket médio por transação.

- **A presença de “PACKING CHARGE” no topo em alguns mercados levanta questões sobre a operação local ou completude da base de dados.** Pode ser necessário revisar os registros de vendas para garantir a qualidade da análise.

- **Mercados como Brasil, Líbano, Arábia Saudita e República Tcheca possuem itens mais baratos como "maior margem"** — sinal de potencial não explorado na oferta de produtos de valor mais alto. Investir em ampliar o mix nesses locais pode desbloquear ganhos marginais.

- **Produtos visualmente expressivos e com personalidade (relógios, quadros, buquês decorativos) demonstram apelo em mercados diversos**, e podem ser usados como itens de entrada para promover o catálogo completo.
        """)
    ),

    "Produtos mais comprados por clientes VIP": lambda: (
        render(
            plot_barh, preferencias.head(50),
            col_categoria="Description", col_valor="Quantity",
            decimais=False, titulo="Produtos mais comprados por clientes VIP"
        ),
        st.markdown("""
        A análise dos produtos mais comprados por clientes VIP revela preferências nítidas por itens que combinam apelo visual, funcionalidade no cotidiano e forte identidade estética. Esses padrões são relevantes para compreender o comportamento de compra de consumidores de maior valor para a UniGift.

---

### **1. Padrões visuais e lifestyle decorativo**

Os itens mais comprados concentram-se em categorias como:

- **Decoração com temática retrô ou afetiva**:  
  Ex: *CHILLI LIGHTS* (875 unidades), *DISCO BALL CHRISTMAS DECORATION*, *PARTY BUNTING*, *WOODEN HEART DECORATIONS*  
  → Esses produtos são populares em celebrações e ambientações afetivas, sugerindo que clientes VIP valorizam a estética festiva, vintage ou romântica.

- **Louça de porcelana e chá**:  
  *ROSES REGENCY TEACUP AND SAUCER*, *PINK REGENCY TEACUP AND SAUCER*, *GREEN REGENCY TEACUP AND SAUCER*, *REGENCY TEA PLATE ROSES*  
  → Forte associação com o universo britânico de tradição e elegância, reforçando o apelo do produto à identidade da marca (UniGift é sediada no Reino Unido).

---

### **2. Alta rotatividade de embalagens de confeitaria e cozinha**

- Diversos tipos de *cake cases* aparecem no top 15:  
  *PACK OF 72 RETROSPOT CAKE CASES*, *DINOSAUR CAKE CASES*, *FAIRY CAKE CASES*, *PINK PAISLEY CAKE CASES*, *VINTAGE LEAF CAKE CASES*  
  → Isso indica que clientes VIP compram itens que serão usados em eventos, culinária ou apresentações cuidadosas — um perfil que valoriza **detalhes e acabamento visual**.

- Outros itens de utilidade doméstica decorativa:  
  *DRAWER KNOBS*, *TEAPOTS*, *BOWLS*, *BUNTING*, *BAG CHARMS*

**Insight**: O mix de produtos mais comprados sugere uso pessoal com alto envolvimento estético — trata-se de uma clientela que valoriza a experiência de produto, e não apenas a função.

---

### **3. Fortíssima presença de bolsas e embalagens para presente**

- *LUNCH BAGS* aparecem em diversas variações e ocupam 9 posições no top 50.  
  Modelos: *RED RETROSPOT*, *WOODLAND*, *APPLE DESIGN*, *PINK POLKADOT*, *BLACK SKULL*, *SPACEBOY*, *CARS BLUE*, entre outros.

- Além das bolsas, há embalagens como *JUMBO BAG RED RETROSPOT* e papéis de presente (*WRAP ENGLISH ROSE*, *SKULLS AND CROSSBONES WRAP*).

**Insight**: Esses produtos indicam um perfil consumidor que compra para presentear ou compor kits, sugerindo um padrão de compra voltado a uso social e eventos. Incentivar esse comportamento com **bundles e kits temáticos** pode ser lucrativo.

---

### **4. Forte presença de edições sazonais e temáticas**

- Artigos como *DISCO BALL CHRISTMAS DECORATION*, *WOODEN STAR CHRISTMAS*, *CHILLI LIGHTS* e *FAIRY CAKE CASES* possuem apelo sazonal.  
  Há também elementos de kits para festa, como *COCKTAIL PARASOLS*, *PARTY BUNTING*, *PLACE SETTINGS*.

**Insight**: Clientes VIP demonstram preferência por itens voltados a datas especiais e ocasiões comemorativas. A UniGift pode se beneficiar ao lançar **coleções limitadas associadas ao calendário comercial**, como Natal, primavera ou dia das mães.

---

### **5. Conclusão estratégica**

Os produtos mais comprados por clientes VIP se concentram em quatro eixos:

- Estética retrô-romântica com apelo britânico
- Itens utilitários com valor emocional ou decorativo
- Artigos de cozinha/festa com foco em apresentação
- Kits, bolsas e embalagens para presente

**Recomendações:**

- Criar campanhas segmentadas com foco nesses temas, sobretudo para públicos com alto ticket médio
- Estimular recompra oferecendo variações sazonais ou coleções renováveis (ex: novas cores de lunch bag ou padrões de cake cases)
- Explorar kits temáticos personalizados como “gift boxes” para compradores VIP — combinando itens do top 50
        """)
    ),

    "Distribuição de clientes por perfil RFV": lambda: (
        render(
            plot_pizza, proporcao_rfv,
            col_categoria="Profile", col_valor="Proportion",
            exibir_percentual=True,
            titulo="Distribuição de clientes por perfil RFV"
        ),
        st.markdown("""
        
        A distribuição de clientes por perfil RFV (Recência, Frequência e Valor) revela características centrais da base de clientes da UniGift. Considerando os dados:

- **Clientes Emergentes**: 41,29%  
- **Clientes Churn** (perdidos/inativos): 35,80%  
- **Clientes VIP**: 22,90%

Essa composição revela padrões estratégicos importantes, tanto em termos de fidelização quanto de risco de evasão. A seguir, uma análise detalhada.

---

### 1. **Alta proporção de Clientes Emergentes: potencial em movimento**

Com 41,29% da base, esse é o maior grupo. Clientes Emergentes são aqueles com comportamento promissor: fazem pedidos recentes, com frequência crescente ou valor médio relevante, mas ainda não atingiram o patamar VIP.

**Oportunidade**: este grupo é o *trampolim natural* para construir mais clientes VIP. Com estímulos certos — como campanhas de recompra, programas de fidelidade ou ofertas personalizadas — é possível acelerar essa jornada.

**Insight**: esse grupo deve ser o foco central de estratégias de ativação e conversão. Monitorar sua progressão de RFV ao longo do tempo permite ações altamente segmentadas e eficazes.

---

### 2. **Clientes Churn representam um risco latente**

Clientes classificados como “Churn” ainda representam **35,80% da base total**. Isso indica que uma parcela significativa deixou de comprar recentemente ou perdeu seu padrão anterior de consumo.

**Desafio**: essa porcentagem elevada sugere ausência de mecanismos sistemáticos de retenção ou que as ações reativas estão chegando tarde.

**Insight**: é essencial entender *por que* esse grupo se afastou — seja por preço, experiência, mudança de mix ou canais. Estratégias como campanhas de reativação, cupons específicos ou mensagens personalizadas podem recuperar parte dessa base a um baixo custo de aquisição.

---

### 3. **Clientes VIP: grupo valioso, porém restrito**

Apenas 22,90% dos clientes estão classificados como VIP. Embora esse percentual seja relevante em termos de valor, ele indica que **a maior parte da receita tende a vir de uma parcela pequena da base**.

**Cuidado**: esses clientes devem ser tratados como ativos-chave. Perder um cliente VIP tende a gerar impacto proporcionalmente maior do que perder outros perfis.

**Insight**: investir em programas de relacionamento de alto valor — com atendimento personalizado, pré-venda, brindes ou eventos exclusivos — pode elevar o tempo de vida desses clientes e criar efeito de comunidade.

---

### **Recomendações gerais com base no gráfico**

- **Criar automações de transição RFV**: como muitos clientes estão em movimento entre os perfis, é estratégico construir ações automáticas que se ajustem ao avanço ou regressão do cliente no modelo RFV.

- **Priorizar conversão dos Emergentes em VIP**: campanhas escalonadas de “boas-vindas”, ofertas progressivas ou acesso antecipado a lançamentos são boas formas de desenvolver esse relacionamento.

- **Criar planos de resgate para Churn**: especialmente os que já foram VIPs ou Emergentes. Ofertas de tempo limitado, produtos nostálgicos ou reengajamento via e-mail marketing podem reativar esse público.

- **Investir na cultura de reconhecimento**: clientes VIP que são tratados com atenção especial não apenas compram mais, como influenciam outros consumidores a buscar esse status.

---

Essa distribuição de perfis reforça que o crescimento sustentável da UniGift virá menos da aquisição em massa e mais da **evolução interna da base de clientes atual**.
        
        """)
    ),

    "Faturamento Total Gerado por Perfil RFV": lambda: (
        render(
            plot_pizza, faturamento_rfv,
            col_categoria="Profile", col_valor="Value",
            simbolo="£", milhar=True, exibir_percentual=False,
            titulo="Faturamento Total Gerado por Perfil RFV"
        ),
        st.markdown("""
        A análise do faturamento total gerado por perfil RFV revela como os diferentes grupos de clientes da UniGift contribuem financeiramente para o negócio. Mesmo com apenas três categorias (VIP, Emergentes e Churn), os dados apontam para dinâmicas comerciais distintas que ajudam a entender melhor onde estão os maiores valores e os maiores riscos.

---

### **Distribuição do faturamento por perfil**

- **Clientes VIP**: £2.774.922 (56,2% do total)  
- **Clientes Emergentes**: £1.217.250 (24,6%)  
- **Clientes Churn**: £324.524 (6,6%)

---

### **1. O peso expressivo dos Clientes VIP**

Com apenas cerca de 23% da base (ver análise anterior), os Clientes VIP respondem por **mais da metade do faturamento da UniGift**. Isso comprova o princípio do Pareto, no qual uma minoria de clientes gera a maior parte da receita.

**Insights**:

- Cada cliente VIP tem, em média, um **Lifetime Value (LTV) muito superior**.
- É crucial manter um esforço constante de fidelização e retenção para esse grupo.
- Perder um único VIP tem impacto direto sobre o faturamento, o que justifica iniciativas de relacionamento personalizado e ações exclusivas.

---

### **2. Emergentes: segmento com forte potencial de crescimento**

Com 41% da base e gerando cerca de 25% da receita, os Clientes Emergentes possuem alto volume e faturamento relevante, embora ainda distante do perfil VIP.

**Oportunidades**:

- A taxa de conversão desses clientes para VIP representa uma das maiores alavancas de crescimento sustentável da UniGift.
- Estratégias de educação, nurturing (comunicação progressiva) e recompensas por frequência podem acelerar essa transição.
- Estímulos baseados em comportamento (ex: valor mínimo de compra para entrar no clube VIP) podem tornar esse funil previsível.

---

### **3. Churn: receita residual de um grupo em declínio**

Apesar de 35% dos clientes estarem classificados como Churn, sua participação no faturamento total é baixa (6,6%). Esse descompasso mostra que esses clientes **já estavam em regressão no consumo antes de inativarem**.

**Reflexões**:

- Nem todo cliente perdido representa perda de grande valor. Mas aqueles que já foram VIPs exigem atenção.
- Estratégias de reativação devem priorizar churns com histórico forte de consumo.
- Ferramentas preditivas podem identificar quando um Emergente começa a se comportar como pré-Churn para intervir rapidamente.

---

### **Conclusão e ações recomendadas**

- A segmentação RFV permite compreender o valor real de cada grupo e definir prioridades com base em impacto financeiro.
- Consolidar um programa de fidelidade para Emergentes e fortalecer laços com os VIPs deve estar no centro da estratégia comercial.
- As ações de reativação devem ser seletivas: o foco deve estar nos churns de alto valor e não na massa inativa como um todo.
        """)
    ),

    "Evolução mensal de migração de clientes Emergentes para VIP": lambda: (
        render(
            plot_barv, migracoes_rfv,
            col_categoria="Month", col_valor="NumMigrations",
            usar_cores=False, decimais=False, log=True,
            ordenar_por_valor=False,
            titulo="Evolução mensal de migração de clientes Emergentes para VIP"
        ),
        st.markdown("""
        A análise da evolução mensal de migração de clientes Emergentes para VIP em 2011 revela tendências sazonais claras e padrões de engajamento que podem informar decisões estratégicas de fidelização. O volume total de migrações no ano foi de 456 clientes, e a variação entre os meses aponta para momentos-chave de conversão ao longo do tempo.

---

### **Evolução mensal: tendências e marcos**

| Mês        | Migrações para VIP |
|------------|--------------------|
| Jan        | 15                 |
| Fev        | 20                 |
| Mar        | 19                 |
| Abr        | 30                 |
| Mai        | 38                 |
| Jun        | 43                 |
| Jul        | 34                 |
| Ago        | 34                 |
| Set        | 37                 |
| Out        | 50                 |
| **Nov**    | **88**             |
| Dez        | 18                 |

---

### **1. Crescimento consistente no 1º semestre**

Entre janeiro e junho, o número de migrações cresceu de forma progressiva, partindo de 15 para 43. Esse padrão indica um ciclo de **engajamento crescente e maturação da base** — com novos clientes Emergentes convertendo-se em VIPs à medida que avançam em frequência ou valor de compras.

**Insight**: ações de relacionamento e acompanhamento pós-primeira compra parecem ter impacto direto na conversão em até 6 meses após aquisição. O tempo médio de transição pode servir de métrica para avaliar a eficácia de programas de fidelidade.

---

### **2. Pico expressivo em novembro**

O mês de **novembro apresentou o dobro de migrações em relação ao mês anterior (88 vs. 50)**. Isso pode ser reflexo de:

- Campanhas promocionais de fim de ano (Black Friday, Natal)
- Aumento natural de consumo no trimestre Q4
- Estratégias específicas de incentivo aplicadas na reta final do ano

**Recomendação**: reforçar iniciativas de ativação e upgrade de clientes emergentes no último trimestre, quando o potencial de conversão é mais alto. Isso pode incluir campanhas escalonadas, conteúdos especiais e bônus acumulativos por faixas de gasto.

---

### **3. Queda significativa em dezembro**

Após o pico, há uma queda acentuada para apenas 18 migrações — valor comparável a fevereiro ou março. Esse recuo pode ser explicado por:

- Fechamento do ciclo de compras no mês anterior
- Saturação de campanhas promocionais
- Limitações logísticas ou de operação em fim de ano

**Reflexão**: dezembro parece menos efetivo para ações de transição de perfil, devendo ser focado em **entregas, atendimento e manutenção da experiência VIP**, mais do que em aquisições.

---

### **4. Comportamento semelhante nos meses de julho a setembro**

Durante o terceiro trimestre (julho a setembro), as migrações mantêm um patamar estável (34–37). Isso pode indicar um **período de manutenção**, em que não há crescimento expressivo, mas também não há queda.

**Sugestão**: inserir estímulos específicos nesse período intermediário do ano pode romper a estabilidade e gerar novo avanço — como pré-lançamentos para clientes emergentes ou planos de upgrade com metas de curto prazo.

---

### **Conclusão estratégica**

A curva de evolução da migração Emergente → VIP é fortemente afetada por **sazonalidade comercial** e **ciclos de engajamento natural**. Ela sugere que:

- Há uma janela média de maturação de até 6 meses entre primeira compra e upgrade de perfil.
- O quarto trimestre oferece o melhor momento para conversão, especialmente novembro.
- É possível manter um ritmo constante de conversão com pequenas alavancas nos períodos de estabilidade.
        """)
    ),

    "Retenção mensal de Clientes Churn": lambda: (
        render(
            plot_barv, retencao_rfv,
            col_categoria="Month", col_valor="Clientes Churn",
            exibir_percentual=True, ordenar_por_valor=False,
            usar_cores=False,
            titulo="Retenção mensal de Clientes Churn"
        ),
        st.markdown("""
        A análise da retenção mensal de clientes do perfil **Churn** — ou seja, clientes que deixaram de comprar ou reduziram drasticamente seu envolvimento com a UniGift — revela tendências que podem indicar riscos de evasão, bem como oportunidades de recuperação ou prevenção.

---

### **1. Variação mensal do percentual de clientes Churn**

| Mês        | Proporção de Churn |
|------------|--------------------|
| 2010-12    | 18,8%              |
| 2011-01    | 15,2%              |
| 2011-02    | 14,4%              |
| 2011-03    | 19,8%              |
| 2011-04    | 15,8%              |
| 2011-05    | 19,0%              |
| 2011-06    | 18,9%              |
| 2011-07    | 17,0%              |
| 2011-08    | 15,8%              |
| 2011-09    | 21,8%              |
| 2011-10    | 27,7%              |
| 2011-11    | **33,9%**          |
| 2011-12    | **10,4%**          |

---

### **2. Tendência geral e marcos críticos**

- **Estabilidade moderada** entre janeiro e agosto, com a proporção de churn oscilando entre 14% e 19%.
- **Aumento acentuado** a partir de setembro, culminando em **novembro com o maior valor do ano (33,9%)**.
- **Queda brusca em dezembro**, com a menor taxa de todo o período (10,4%).

---

### **3. Interpretações possíveis**

- O **pico em novembro** ocorre justamente durante o mês de maior migração de clientes Emergentes para VIP (conforme sua outra análise). Isso sugere um comportamento bifurcado da base: enquanto parte é ativada com sucesso e se torna mais valiosa, outra parte se desengaja.

- A **redução em dezembro** pode refletir:
  - Um recorte de clientes ativos com perfil mais engajado (ex: fim de campanhas promocionais que atraíam clientes menos fiéis).
  - Um efeito estatístico da concentração de vendas entre VIPs e Emergentes que reduz a proporção relativa de churn.

---

### **4. Relação com os demais perfis (VIP e Emergentes)**

- Nos meses de alta em Churn (setembro a novembro), os **Clientes Emergentes também aumentam** — indicando que parte da base está transitando positivamente, mas outra parte, não estimulada, está abandonando.

- A **elevação simultânea de VIPs e Churn em novembro** mostra que o crescimento de valor (receita) pode estar sendo obtido **à custa de uma base mais volátil**. Isso alerta para a necessidade de estratégias balanceadas entre crescimento e retenção.

---

### **5. Estratégias sugeridas**

- **Monitoramento preventivo**: identificar clientes com recência e frequência em queda já em julho-agosto pode evitar o pico de evasão observado no fim do ano.

- **Campanhas de resgate direcionadas**: especialmente entre setembro e outubro, oferecendo recompra facilitada, condições exclusivas ou lembretes personalizados.

- **Reativação pós-natal**: dezembro é o melhor momento para ações de reconexão com churns — com mensagens de agradecimento, pesquisas de feedback ou convites para campanhas de início de ano.

- **Segmentação cruzada com valor histórico**: não tratar todos os churns da mesma forma. Clientes que já foram VIP ou Emergentes ativos merecem plano especial de reengajamento.

---

### **Conclusão**

Embora o comportamento de churn tenha se mantido razoavelmente controlado no primeiro semestre, o último trimestre apresenta um risco claro de evasão em massa. Identificar antecipadamente perfis de risco, cruzar dados de recência com ticket médio e aplicar estratégias automatizadas de contenção pode preservar uma fatia valiosa da base e melhorar o custo de retenção por cliente.
        """)
    ),

    "Retenção mensal de Clientes Emergentes": lambda: (
        render(
            plot_barv, retencao_rfv,
            col_categoria="Month", col_valor="Clientes Emergentes",
            exibir_percentual=True, ordenar_por_valor=False,
            usar_cores=False,
            titulo="Retenção mensal de Clientes Emergentes"
        ),
        st.markdown("""
        A análise da retenção mensal de **Clientes Emergentes** ao longo de 2011 evidencia a dinâmica de crescimento e transformação dessa base estratégica. Esses clientes representam um estágio intermediário no modelo RFV — entre perfis inativos e o status de Cliente VIP — e seu comportamento é um indicador importante de vitalidade comercial.

---

### **Evolução do percentual de Clientes Emergentes (RFV)**

| Mês        | Proporção de Emergentes |
|------------|--------------------------|
| 2010-12    | 19,2%                    |
| 2011-01    | 16,5%                    |
| 2011-02    | 17,1%                    |
| 2011-03    | 22,4%                    |
| 2011-04    | 20,4%                    |
| 2011-05    | 25,9%                    |
| 2011-06    | 23,6%                    |
| 2011-07    | 23,5%                    |
| 2011-08    | 23,2%                    |
| 2011-09    | 31,8%                    |
| 2011-10    | 33,0%                    |
| 2011-11    | **39,9%**                |
| 2011-12    | 15,3%                    |

---

### **1. Crescimento consistente de março a novembro**

Após um leve recuo em janeiro e fevereiro, a proporção de Emergentes inicia uma **trajetória ascendente entre março e novembro**, atingindo o pico de **39,9%** — o valor mais alto do ano.

**Interpretação**:

- A empresa foi bem-sucedida em estimular novos clientes ou reativar perfis que passaram a exibir comportamento recente e engajado.
- Isso reflete uma **captação ativa e estratégias eficazes de ativação** ao longo do segundo e terceiro trimestres.

---

### **2. Queda abrupta em dezembro**

Em dezembro, a proporção de Clientes Emergentes cai drasticamente para **15,3%**, voltando aos níveis observados no início do ano.

**Possíveis causas**:

- **Migração massiva de Emergentes para VIPs** em novembro, resultando na redução desse grupo.
- **Desaceleração nas primeiras compras** ou nos padrões de engajamento característicos do perfil Emergente.
- **Efetivação de campanhas de migração**, que drenam a base intermediária em direção aos extremos (VIP ou Churn).

---

### **3. Relação com os demais perfis: transição acelerada**

Acompanhar os dados dos perfis VIP e Churn ao longo do mesmo período revela:

- O crescimento dos Emergentes está acompanhado de **incremento paralelo nos Clientes VIP** — evidência de que parte deles conclui o ciclo de evolução RFV.
- O aumento de Churn no fim do ano reforça que outra parte dos Emergentes **não é convertida a tempo e acaba abandonando** o relacionamento.

---

### **4. Recomendações estratégicas**

- **Campanhas de ativação antecipadas**: identificar sinais de comportamento Emergente logo após a primeira compra pode ampliar o tempo útil nesse estágio e aumentar a taxa de conversão para VIP.

- **Acompanhamento de ciclo de vida**: considerando que Emergentes tendem a evoluir ou decair rapidamente, é crucial definir **janelas de transição** (ex: 3–4 meses) para aplicar incentivos personalizados.

- **Evitar o “vazio de dezembro”**: após o pico de novembro, a queda do perfil Emergente pode ser amenizada com estratégias de retenção específicas para o fim de ano, como cupons de recompra ou kits de Natal.

- **Mapear gatilhos de migração**: monitorar quais ações, produtos ou campanhas aumentam a chance de um Emergente se tornar VIP pode ajudar a projetar caminhos otimizados de fidelização.

---

### **Conclusão**

A proporção de Clientes Emergentes serve como termômetro da **capacidade de renovação e crescimento do ciclo de valor** da UniGift. Seu fortalecimento entre março e novembro reflete um desempenho saudável, mas a queda acentuada em dezembro alerta para o risco de perdas se não houver acompanhamento contínuo. Entender como esses clientes se comportam e quais estímulos os movem ao longo da jornada é essencial para transformar um público promissor em fonte de receita recorrente e sustentável.
        """)
    ),

    "Retenção mensal de Clientes VIP": lambda: (
        render(
            plot_barv, retencao_rfv,
            col_categoria="Month", col_valor="Clientes VIP",
            exibir_percentual=True, ordenar_por_valor=False,
            usar_cores=False,
            titulo="Retenção mensal de Clientes VIP"
        ),
        st.markdown("""
        A análise da retenção mensal de **Clientes VIP** ao longo de 2011 destaca flutuações relevantes em seu peso relativo na base de clientes da UniGift. Como esse perfil representa os consumidores com maior valor agregado — tanto em frequência quanto em valor de compra — monitorar sua estabilidade e evolução é essencial para sustentar o desempenho financeiro da empresa.

---

### **Evolução mensal do percentual de Clientes VIP**

| Mês        | % VIP |
|------------|--------|
| Dez/2010   | 67,6%  |
| Jan/2011   | 56,8%  |
| Fev        | 58,1%  |
| Mar        | 55,4%  |
| Abr        | 55,4%  |
| Mai        | 62,2%  |
| Jun        | 59,5%  |
| Jul        | 55,4%  |
| Ago        | 58,1%  |
| Set        | 67,6%  |
| Out        | 64,9%  |
| Nov        | **75,7%** ← pico
| Dez        | **51,4%** ← menor nível

---

### **1. Retração no primeiro semestre e estabilização**

- Após um ponto alto em dezembro de 2010 (67,6%), há uma **queda acentuada entre janeiro e março**, com o percentual de VIPs se mantendo ao redor de 55%.
- Entre abril e agosto, observa-se uma **estabilidade moderada** entre 55% e 59%.

**Interpretação**: o início do ano pode representar um momento de recomposição do consumo pós-natal, com menor ritmo de recompra mesmo entre os melhores clientes. Ainda assim, manter mais da metade da base ativa como VIP ao longo de vários meses demonstra uma **estrutura de fidelização sólida**.

---

### **2. Fortalecimento no 3º trimestre e ápice em novembro**

- A partir de setembro, a base VIP cresce novamente, retomando 67,6% e alcançando o **pico histórico de 75,7% em novembro**.
- Esse aumento acompanha o momento de maior migração de Emergentes para VIP (confirmado em análise anterior).

**Insight**: novembro é um ponto-chave de conversão e fidelização. Aparentemente, campanhas sazonais (como Black Friday, kits de fim de ano ou incentivos por volume) foram eficazes para elevar o status da base.

---

### **3. Queda significativa em dezembro**

- Dezembro apresenta um **recuo para 51,4%**, o menor percentual de VIPs no ano.

**Hipóteses**:
- Parte dos VIPs pode ter cessado compras naquele mês por já terem realizado transações em novembro (efeito de antecipação).
- Clientes que compraram esporadicamente em dezembro não atingiram critérios RFV para permanecer no status VIP.
- Alto volume de novos clientes (Emergentes) pode ter reduzido a proporção relativa do grupo VIP, mesmo com sua base em números absolutos mantendo-se estável.

---

### **4. Estratégias recomendadas**

- **Aproveitar novembro como o principal gatilho de migração e reconhecimento VIP**, com campanhas de upgrade, lançamentos exclusivos e selos de fidelidade.
- **Mitigar a perda de engajamento em janeiro**, por meio de ações de reativação pós-festas, previews de coleções e bônus por recompra antecipada.
- **Garantir continuidade de compra após o upgrade**: VIPs que não voltam a comprar no trimestre seguinte tendem a regressar na classificação RFV.
- **Monitorar queda de VIPs em dezembro para entender se é recuo natural ou falha de retenção** — especialmente após período de forte crescimento.

---

### **Conclusão**

A base de Clientes VIP da UniGift se mostra robusta e responsiva a campanhas sazonais, atingindo seu melhor desempenho no trimestre final de 2011. Contudo, a oscilação após novembro reforça a importância de manter ativa a experiência VIP — não basta conquistar esse cliente, é essencial nutri-lo com estímulos personalizados, valor percebido e recompensas cíclicas para garantir sua permanência no topo da pirâmide de valor.
        """)
    )
}

# Sidebar
st.sidebar.markdown("### 🧭 Navegação")
for nome in graficos:
    if st.sidebar.button(nome):
        st.session_state.grafico_ativo = nome

# Exibição
if st.session_state.grafico_ativo:
    resultado = graficos[st.session_state.grafico_ativo]
    if isinstance(resultado, tuple):
        for etapa in resultado:
            if callable(etapa):
                etapa()
    else:
        resultado()
