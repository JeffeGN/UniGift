# UniGift - Segmentação de Clientes via Análise RFV

Análise de comportamento de clientes baseada no modelo **RFV (Recência, Frequência e Valor)**, com foco em estratégias de retenção, personalização de campanhas e apoio à gestão de estoque.

Este repositório consolida pipeline de dados, funções analíticas reutilizáveis, testes automatizados e um **dashboard interativo (deploy via Streamlit Community Cloud)** com visualizações e análises interpretativas embutidas — diretamente abaixo de cada gráfico.

---

## 🧭 Contexto

**UniGift** é um e-commerce especializado em presentes personalizados para ocasiões diversas no mercado britânico. Atende tanto o público B2C quanto atacadistas, lidando com desafios como:

- Entender os perfis de clientes mais valiosos
- Reduzir churn e reativar compradores inativos
- Otimizar campanhas promocionais com base em comportamento real de compra
- Ajustar portfólio de produtos com base na demanda por segmento

---

## 🔍 Problemas abordados

- Como **identificar automaticamente os clientes com maior impacto financeiro**?
- Quais **sinais indicam queda de engajamento** e risco de churn?
- Como segmentar os clientes para personalizar **estratégias de marketing**?
- Como as compras estão distribuídas entre novos e recorrentes?
- Quais métricas orientam a **tomada de decisão de pricing e estoque**?

---

## 🎯 Solução técnica

- Limpeza e padronização dos dados de transações
- Cálculo dos indicadores de **Recência**, **Frequência** e **Valor**
- Modelagem RFV via quantis e scores compostos
- Segmentação visual com gráficos de barras e pizza
- Análises descritivas integradas no app (abaixo de cada visualização)
- Testes com `pytest`, incluindo **parametrização de casos de borda**
- Medição de **cobertura de testes com `pytest-cov`**
- Modularização com funções reutilizáveis (`src/plots.py`, `format_milhar`)
- Backend compatível com ambientes headless (uso de `Agg`)
- Arquivo `.bat` com execução automatizada e geração de relatório HTML

---

## 📊 Exemplos de visualização

- `plot_barh()`, `plot_barv()` e `plot_pizza()` com formatação monetária inteligente
- Sufixos compactos (`k`, `kk`) configuráveis
- Rótulos com controle de casas decimais e símbolo (`R$`, `£`, `$`, etc.)
- Suporte a escala logarítmica, ordenação flexível e agrupamento visual por cor
- **Textos analíticos posicionados diretamente após cada gráfico (Streamlit)**

---

## ✅ Testes e qualidade

- Testes automatizados com `pytest`
- Cobertura monitorada com `pytest-cov`  
- Casos extremos como `999`, `999_999`, `1_000_000` tratados com precisão decimal  
- Separação de lógica de cálculo e formatação textual

---

## 🚀 Deploy

O dashboard foi publicado em:

🔗 [Streamlit Community Cloud](https://jeffegn-unigift-app-20w8ar.streamlit.app/)  

---

## 📁 Organização

📦 UniGift/  
├── app.py               # App Streamlit com navegação e análises integradas  
├── app.bat              # Atalho para executar o app.py sem abrir o terminal  
├── tests.bat            # Atalho para rodar os testes com pytest + cobertura  
├── requirements.txt     # Dependências necessárias para execução e deploy  
├── src/                 # Módulo de visualizações, formatação e pré-processamento  
│   ├── plots.py  
│   ├── formatador.py  
│   └── preprocessamento.py  
├── data/  
│   ├── raw/             # Base de dados original (OnlineRetail.csv)  
│   │   └── OnlineRetail.csv  
│   ├── clean/           # Base tratada (df.csv) com dados limpos  
│   │   └── df.csv  
│   └── dashboards/      # Arquivos segmentados para visualizações no app  
│       ├── transacoes.csv  
│       ├── media_preco.csv  
│       ├── top_vendas_pais.csv  
│       ├── margem_lucro.csv  
│       ├── preferencias.csv  
│       ├── rfv.csv  
│       ├── proporcao_rfv.csv  
│       ├── faturamento_rfv.csv  
│       ├── migracoes_rfv.csv  
│       └── retencao_rfv.csv  
├── tests/               # Testes automatizados com `pytest`  
├── htmlcov/             # Relatório de cobertura de testes (gerado com `pytest-cov`)  
├── UniGift.ipynb        # Notebook de limpeza, exploração e exportação de dados  
├── README.md            # Documentação principal do projeto  
└── LICENSE              # Termos de uso e licença  

---

Esse projeto tem foco em **clareza, modularidade e inteligência de negócio**, transformando dados brutos em insights aplicáveis — com tabelas e análises escritas dentro do app para cada visualização RFV.
