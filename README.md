# 📊 Análise de Clientes e Risco de Churn - Northwind (Projeto RFM + Streamlit)

**👉 [Acesse o Dashboard Online Aqui](https://analytics-northwind.streamlit.app/)**

Este projeto faz parte do meu portfólio como **Cientista de Dados em formação**. O objetivo foi realizar uma análise completa de clientes da empresa fictícia **Northwind**, aplicando o modelo **RFM (Recência, Frequência, Monetário)** e apresentando os resultados em um **dashboard interativo** criado com **Streamlit**.

## 🎯 Objetivos do Projeto

- Analisar o comportamento dos clientes
- Identificar clientes em risco de churn (cancelamento/inatividade)
- Criar segmentações utilizando o modelo RFM
- Visualizar métricas-chave e insights de negócio
- Praticar extração de dados via SQL, manipulação com Python (Pandas) e visualização com Streamlit
- Realizar deploy do projeto para acesso online via Streamlit Cloud

## 📚 Fonte dos Dados

- Base Northwind, originalmente hospedada em PostgreSQL.
- Tabelas principais utilizadas: `customers`, `orders`, `order_details`.
- Exportação para CSV para viabilizar o deploy online.

## 📂 Scripts SQL

As consultas SQL utilizadas para gerar as tabelas de análise estão disponíveis na pasta `/SQL/` deste repositório.

Incluindo:

- Criação da **view de análise de clientes RFM**
- Contagem de clientes por status
- Outras consultas exploratórias utilizadas no projeto

> **Arquivo principal:** `queries_clientes_northwind.sql`

## 🛠️ Tecnologias e Ferramentas Utilizadas

- Python
- Pandas
- Matplotlib
- Seaborn
- SQL (PostgreSQL)
- SQLAlchemy
- Streamlit
- Git e GitHub

## 📈 Principais Análises Realizadas

- KPIs gerais da base de clientes
- Segmentação RFM (Ativo, Risco de Churn, Inativo)
- Comparativo de métricas por status
- Análise Exploratória de Dados (Histogramas, Boxplots, Heatmap, Scatterplot)
- Geração de insights estratégicos sobre o comportamento de compra e risco de churn

## 💻 Como Executar o Projeto Localmente

1. Clone este repositório:

```bash
git clone https://github.com/cccandido/northwind.git
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o projeto com Streamlit, utilizando os arquivos CSV disponíveis na pasta `/data/`:

```bash
streamlit run stream-csv.py
```

## 🚀 Deploy Online

Este projeto está disponível publicamente via **Streamlit Cloud**:

👉 [https://analytics-northwind.streamlit.app/](https://analytics-northwind.streamlit.app/)

## 📌 Próximos Passos

- Evoluir o dashboard com filtros interativos
- Implementar um modelo preditivo de churn utilizando Machine Learning
- Explorar deploys em outras plataformas como AWS ou Heroku

## 👩‍💻 Sobre mim

 **Analista de Dados** com objetivo e foco crescente em projetos de **Ciência de Dados aplicada a Negócios**.

Este projeto faz parte do meu portfólio prático, refletindo não apenas o aprendizado técnico, mas também minha capacidade de entender o problema de negócio, estruturar análises e entregar insights de valor.

**Acesse meu linkedin!**

[LinkedIn - Camila Candido](https://www.linkedin.com/in/camila-scandido/)
