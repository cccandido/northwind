
# 📊 Análise de Clientes e Risco de Churn - Northwind (Projeto RFM + Streamlit)

Este projeto é parte do meu portfólio como Cientista de Dados em formação. O objetivo foi realizar uma análise completa de clientes da empresa fictícia **Northwind**, utilizando o modelo **RFM (Recência, Frequência, Monetário)** e apresentar os resultados em um dashboard interativo com **Streamlit**.

## 🎯 Objetivos do Projeto

- Analisar o comportamento dos clientes
- Identificar clientes em risco de churn (cancelamento/inatividade)
- Criar segmentações com base no modelo RFM
- Visualizar métricas-chave e insights de negócio
- Praticar extração de dados via SQL, manipulação com Python (Pandas) e visualização com Streamlit

## 📚 Fonte dos Dados

- Base Northwind, originalmente em PostgreSQL.
- Principais tabelas utilizadas: `customers`, `orders`, `order_details`.
- Os dados foram extraídos via SQL e tratados em Python.

## 🛠️ Tecnologias Utilizadas

- Python
- Pandas
- Matplotlib
- Seaborn
- SQL (PostgreSQL)
- Streamlit
- SQLAlchemy

## 📈 Principais Análises Realizadas

- KPIs gerais da base de clientes
- Segmentação RFM (Ativo, Risco de Churn, Inativo)
- Comparativo de métricas por status
- Análise Exploratória de Dados (Histogramas, Boxplots, Heatmap, Scatterplot)
- Insights de negócio sobre risco de perda de clientes

## 💻 Como Executar o Projeto Localmente

1. Clone este repositório.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Garanta que você tenha acesso ao banco local PostgreSQL **ou** utilize os CSVs exportados (disponíveis na pasta `/data`).
4. Execute o Streamlit:

```bash
streamlit run app.py
```

## 🚀 Próximos Passos

- Adaptar o projeto para leitura via CSV ou Supabase, visando facilitar o deploy online.
- Evoluir o dashboard com filtros e interatividade.
- Implementar um modelo de Machine Learning para previsão de churn.

## 📌 Observação Final

Este projeto foi desenvolvido com foco em aprendizado, boas práticas de análise de dados e storytelling de negócio.

### Desenvolvido por: [Seu Nome Aqui]
