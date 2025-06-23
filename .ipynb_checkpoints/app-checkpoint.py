import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine

# 1. CONEXÃO AO BANCO DE DADOS
user = 'postgres'
password = 'postgres'
host = 'localhost'
port = '5432'
database = 'northwind'

# Conexão
engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
connection = engine.connect()

print("Conectado com sucesso!")

# 2. LEITURA DAS TABELAS PRINCIPAIS
customers = pd.read_sql('SELECT * FROM customers', connection)
orders = pd.read_sql('SELECT * FROM orders', connection)
order_details = pd.read_sql('SELECT * FROM order_details', connection)

# 3. CALCULO DO RFM (Recencia, Frequencia, Monetario)
reference_date = pd.to_datetime(orders['order_date']).max() + pd.Timedelta(days=1)
orders['order_date'] = pd.to_datetime(orders['order_date'])

rfm = orders.groupby('customer_id').agg({
    'order_date': lambda x: (reference_date - x.max()).days,
    'order_id': 'count'
}).rename(columns={
    'order_date': 'Recency',
    'order_id': 'Frequency'
}).reset_index()

# Calculo do Monetario
order_details['total'] = order_details['unit_price'] * order_details['quantity'] * (1 - order_details['discount'])
monetary = orders.merge(order_details, on='order_id') \
    .groupby('customer_id')['total'].sum().reset_index() \
    .rename(columns={'total': 'Monetary'})

rfm = rfm.merge(monetary, on='customer_id')

# 4. SEGMENTAÇÃO SIMPLES DE CHURN
rfm['Churn_Risco'] = np.where(rfm['Recency'] > 90, 'Alto Risco', 'Baixo Risco')

# 5. DASHBOARD STREAMLIT
st.title('📊 Análise de Clientes - Projeto Northwind')

st.markdown("""
Este dashboard apresenta uma análise de clientes baseada no modelo RFM (Recência, Frequência, Monetário).
""")

# Métricas principais
col1, col2, col3 = st.columns(3)
col1.metric('Clientes', rfm['customer_id'].nunique())
col2.metric('Faturamento Total', f"${rfm['Monetary'].sum():,.2f}")
col3.metric('Clientes em Alto Risco', rfm[rfm['Churn_Risco'] == 'Alto Risco'].shape[0])

# Filtros
risco = st.radio('Filtrar por risco de churn:', ['Todos', 'Alto Risco', 'Baixo Risco'])

if risco != 'Todos':
    rfm = rfm[rfm['Churn_Risco'] == risco]

# Gráfico de Dispersão RFM
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=rfm, x='Frequency', y='Monetary', hue='Churn_Risco', palette='Set1', s=100, ax=ax)
plt.title('Distribuição RFM por Risco de Churn')
st.pyplot(fig)

# Fechar conexão ao final
connection.close()
