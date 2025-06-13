# UniGift · Segmentação de Clientes via Análise RFV

Análise de comportamento de clientes baseada no modelo **RFV (Recência, Frequência e Valor)**, com foco em estratégias de retenção, personalização de campanhas e apoio à gestão de estoque.

Este repositório consolida pipeline de dados, funções analíticas reutilizáveis, testes automatizados e gráficos interativos para compreensão e visualização dos perfis mais relevantes para o negócio.

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
- Suporte a escala logarítmica e agrupamento visual por cor

---

## ✅ Testes e qualidade

- Testes automatizados com `pytest`
- Cobertura monitorada com `pytest-cov`  
- Casos extremos como `999`, `999_999`, `1_000_000` tratados com precisão decimal  
- Separação de lógica de cálculo e formatação textual

---

## 📁 Organização

```
📦 UniGift/
├── src/              # Funções de formatação e visualização
├── tests/            # Testes automatizados (unitários e parametrizados)
├── htmlcov/          # Relatório de cobertura (gerado após testes)
├── UniGift.ipynb     # Notebook de demonstração dos gráficos e resultados
└── README.md         # Este arquivo
```

---

Esse projeto tem foco em **clareza, modularidade e confiabilidade**, oferecendo uma base sólida para aplicar RFV em diversos contextos.