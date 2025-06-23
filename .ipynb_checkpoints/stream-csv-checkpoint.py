#bibliotecas
from sqlalchemy import create_engine
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import datetime as dt
import seaborn as sns

#------------------------------
# Acesso ao banco e leitura
# das principais colunas
#-----------------------------

#leitura das tabelas principais

customers = pd.read_csv('data/customers.csv')
orders = pd.read_csv('data/orders.csv')
order_details = pd.read_csv('data/order_details.csv')

# Convertendo a coluna de data
orders['order_date'] = pd.to_datetime(orders['order_date'])

#------------------------------------
#CONSTRUINDO AS MÉTRICAS DO RFM
#-----------------------------------

#Recência 

data_referencia = orders['order_date'].max()

def calcula_recencia(grupo):
    ultima_data = grupo['order_date'].max()
    return (data_referencia - ultima_data).days

recencia = orders.groupby('customer_id').apply(calcula_recencia).reset_index(name='recencia_dias')


#Frequencia 

frequencia = orders.groupby('customer_id').agg({
    'order_id':'count'
}).reset_index().rename(columns={'order_id':'frequencia_pedidos'})


#Monetario

#unindo tabela orders com tabela orders_details

pedidos_detalhes = orders.merge(order_details, on='order_id')


#criando uma coluna com o valor total de cada item comprado

pedidos_detalhes['valor_total'] = pedidos_detalhes['unit_price'] * pedidos_detalhes['quantity']

monetario = pedidos_detalhes.groupby('customer_id').agg({
    'valor_total':'sum'
}).reset_index().rename(columns={'valor_total':'valor_total_gasto'})


#unindo o RFM

rfm = recencia.merge(frequencia, on='customer_id').merge(monetario, on='customer_id')


# Calculando Ticket Médio
rfm['ticket_medio'] = rfm['valor_total_gasto'] / rfm['frequencia_pedidos']

#-----------------------------------
# EXPLORANDO O RFM 
# -----------------------------------
#Segmentação dos clientes com base na recencia

#0 30 dias - ativo
#31 a 90 dias - risco de churn
#>90 inativo

def segmenta_cliente (recencia):
    if recencia <= 30:
        return 'Cliente Ativo'
    elif recencia <= 90:
        return 'Risco de Churn'
    else: 
        return 'Inativo'
        

rfm['status_cliente'] = rfm['recencia_dias'].apply(segmenta_cliente)

# Contagem de clientes por status
count_status = rfm.groupby('status_cliente').agg({'customer_id':'nunique'}).reset_index().rename(columns={'customer_id':'qtd_clientes'})


# Cálculo geral de inativos e risco de churn
total_clientes = rfm['customer_id'].nunique()
clientes_inativos = count_status.loc[count_status['status_cliente'] == 'Inativo', 'qtd_clientes'].values[0]
clientes_risco = count_status.loc[count_status['status_cliente'] == 'Risco de Churn', 'qtd_clientes'].values[0]

percentual_inativos = (clientes_inativos / total_clientes) * 100
percentual_risco = (clientes_risco / total_clientes) * 100
percentutal_perda_total = ((clientes_inativos + clientes_risco) / total_clientes ) *100



# KPIs calculados
total_clientes = rfm['customer_id'].nunique()
total_vendas = rfm['valor_total_gasto'].sum()
total_pedidos = rfm['frequencia_pedidos'].sum()
ticket_medio_geral = total_vendas / total_pedidos


# --------------------------
# MONTANDO O STREAMLIT
# --------------------------
# Estrutura com Abas
# --------------------------

st.title("📊 Análise de Clientes e Risco de Churn - RFM com Northwind Database")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📌 Introdução",
    "📈 KPIs",
    "🧑‍🤝‍🧑 Segmentação",
    "📊 Comparativos por Status",
    "🔎 EDA",
    "📋 Conclusões"
])

# --------------------------
# Aba 1 - Introdução
# --------------------------
with tab1:
   

    st.markdown("""
    ### 🎯 Objetivo do Projeto:

    Realizar uma análise detalhada da base de clientes da empresa Northwind, utilizando a metodologia **RFM (Recência, Frequência e Monetário)**.

    O foco principal é **identificar padrões de comportamento dos clientes** e **avaliar o risco de churn (cancelamento/inatividade)**.  
    O projeto busca **classificar os clientes em diferentes segmentos estratégicos**, como:

    - **Clientes Ativos**
    - **Clientes em Risco de Churn**
    - **Clientes Inativos**

    Essa segmentação permitirá ao time de Marketing e Vendas **priorizar ações de retenção e reengajamento**.

    ---

    ### 🏢 Sobre a Base de Dados:

    O projeto utiliza o tradicional banco de dados **Northwind**, que simula as operações comerciais de uma distribuidora de alimentos.

    As principais tabelas utilizadas foram:

    - **Customers:** Dados cadastrais dos clientes.
    - **Orders:** Histórico de pedidos.
    - **Order Details:** Itens vendidos em cada pedido.

    ---

    ### 📈 Metodologia:

    Para atingir os objetivos, foram aplicadas as seguintes técnicas:

    - Manipulação de dados e extração de KPIs com **PostgrSQL e Python (Pandas)**
    - Construção das métricas **RFM** para análise de comportamento
    - **Segmentação de clientes por risco de churn**
    - **Análise exploratória de dados (EDA)** para identificação de padrões
    - Criação de um **Dashboard interativo com Streamlit**, permitindo visualização e interação com os dados
    """)


# --------------------------
# Aba 2 - KPIs Gerais
# --------------------------

# --------------------------
# Aba 2 - KPIs Gerais (Formato com Cards Personalizados)
# --------------------------
with tab2:
    st.header("📈 KPIs Gerais da Base de Clientes")


    col1, col2, col3, col4 = st.columns(4)

    # KPI 1 - Total de Clientes
    with col1:
        st.markdown("<h5 style='color:gray;'>Total de Clientes</h5>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#ffffff;'>{total_clientes:,}".replace(",", "."), unsafe_allow_html=True)

    # KPI 2 - Total de Vendas
    with col2:
        st.markdown("<h5 style='color:gray;'>Total de Vendas R$ </h5>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#ffffff;'>R$ {int(total_vendas):,}".replace(",", ".") + "</h3>", unsafe_allow_html=True)

    # KPI 3 - Total de Pedidos
    with col3:
        st.markdown("<h5 style='color:gray;'>Total de Pedidos</h5>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#ffffff;'>{total_pedidos:,}".replace(",", "."), unsafe_allow_html=True)

    # KPI 4 - Ticket Médio Geral
    with col4:
        st.markdown("<h5 style='color:gray;'>Ticket Médio Geral</h5>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#ffffff;'>R$ {ticket_medio_geral:,.2f}</h3>".replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

    st.markdown("""
    <p style='font-size:18px; color:#ffffff;'>
    Estes indicadores oferecem uma visão geral da base de clientes e do volume de vendas.
    O <strong>Ticket Médio Geral</strong> indica o valor médio de cada pedido realizado.
    </p>
    """, unsafe_allow_html=True)


# ----------------------------------
# Aba 3 - Segmentação de Clientes
# ----------------------------------

with tab3:
    st.header("🧑‍🤝‍🧑 Segmentação de Clientes - Status RFM")

    st.markdown("""
    A segmentação foi realizada com base na **Recência (R)** das compras de cada cliente.

    **Critérios de Segmentação:**

    - **Ativo:** Última compra nos últimos 30 dias
    - **Risco de Churn:** Última compra entre 31 e 90 dias
    - **Inativo:** Última compra há mais de 90 dias

    Essa classificação permite ao time comercial entender o nível de engajamento dos clientes e priorizar estratégias de retenção.
    """)


    # Opção para escolher tipo de gráfico
    tipo_grafico = st.radio("Escolha o tipo de gráfico para visualizar a distribuição:", ["Pizza", "Barras"])

    if tipo_grafico == "Pizza":
        fig, ax = plt.subplots()
        ax.pie(count_status['qtd_clientes'],
               labels=count_status['status_cliente'],
               autopct='%1.1f%%',
               startangle=140,
               colors=plt.cm.Paired.colors)
        ax.axis('equal')
        st.pyplot(fig)

    else:
        fig, ax = plt.subplots()
        ax.bar(count_status['status_cliente'], count_status['qtd_clientes'], color='skyblue')
        plt.xticks(rotation=45)
        plt.title('Quantidade de Clientes por Status')
        st.pyplot(fig)

    # Exibir tabela com os números
    st.dataframe(count_status)

    st.markdown(f"""
    <p style='font-size:18px; color:#ffffff;'>
    <strong>Insight:</strong> Atualmente, <strong>{percentual_inativos:.1f}%</strong> da base de clientes está inativa, e <strong>{percentual_risco:.1f}%</strong> corre risco de churn, totalizando <strong>{percentutal_perda_total:.1f}%</strong> de toda a base de clientes, representando um potencial impacto significativo de receita.
    </p>
    """, unsafe_allow_html=True)


# -------------------------------------------
# Aba 4 - Comparativos por Status
# -------------------------------------------

# --------------------------
# Aba 4 - Comparativos por Status
# --------------------------
with tab4:
    st.header("📊 Comparativos de Métricas por Status de Cliente")

    st.markdown("""
    Aqui comparamos as principais métricas **(Recência, Frequência, Valor Monetário e Ticket Médio)** entre os diferentes grupos de clientes.

    Essa análise permite entender como os grupos se comportam em relação ao volume de compras, ao gasto total e ao tempo desde a última interação.
    """)

    # Agrupamento por status
    comparativo_status = rfm.groupby('status_cliente').agg({
        'recencia_dias': 'mean',
        'frequencia_pedidos': 'mean',
        'valor_total_gasto': 'mean',
        'ticket_medio': 'mean'
    }).reset_index().rename(columns={
        'recencia_dias': 'Recência Média (dias)',
        'frequencia_pedidos': 'Frequência Média de Pedidos',
        'valor_total_gasto': 'Valor Médio Gasto (R$)',
        'ticket_medio': 'Ticket Médio (R$)'
    })

    # Exibir a tabela com formatação
    st.dataframe(comparativo_status.style.format({
        'Recência Média (dias)': '{:.1f}',
        'Frequência Média de Pedidos': '{:.1f}',
        'Valor Médio Gasto (R$)': 'R$ {:.2f}',
        'Ticket Médio (R$)': 'R$ {:.2f}'
    }))

    # Gráfico - Valor Médio Gasto por Status
    st.subheader("💰 Valor Médio Gasto por Status")
    fig, ax = plt.subplots()
    ax.bar(comparativo_status['status_cliente'], comparativo_status['Valor Médio Gasto (R$)'], color='salmon')
    plt.title('Valor Médio Gasto por Status')
    plt.ylabel('R$')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Gráfico - Frequência Média por Status
    st.subheader("📦 Frequência Média de Pedidos por Status")
    fig, ax = plt.subplots()
    ax.bar(comparativo_status['status_cliente'], comparativo_status['Frequência Média de Pedidos'], color='lightgreen')
    plt.title('Frequência Média de Pedidos por Status')
    plt.ylabel('Número de Pedidos')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # Gráfico - Ticket Médio por Status
    st.subheader("💳 Ticket Médio por Status")
    fig, ax = plt.subplots()
    ax.bar(comparativo_status['status_cliente'], comparativo_status['Ticket Médio (R$)'], color='orange')
    plt.title('Ticket Médio por Status')
    plt.ylabel('R$')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    st.markdown("""
    > **Insight:** Como esperado, os **Clientes Ativos** apresentam maior frequência de compras e maior gasto médio.
    
    > Já os clientes em **Risco de Churn** apresentam uma queda clara nas métricas de gasto e ticket médio.
    
    > Curiosamente, os **Inativos** ainda mantêm um gasto acumulado médio relativamente maior, um indicativo de que muitos desses clientes já foram bons compradores no passado, mas hoje estão inativos. """)


# --------------------------
# Aba 5 - Análise Exploratória de Dados (EDA)
# --------------------------
with tab5:
    st.header("🔎 Análise Exploratória das Variáveis RFM")

    st.markdown("""
    Nesta seção, exploramos a distribuição e o comportamento das principais variáveis da análise RFM:

    - **Recência (Dias desde a última compra)**
    - **Frequência (Número de Pedidos)**
    - **Valor Monetário (Total gasto por cliente)**
    - **Ticket Médio**
    """)

    # -----------------
    # Histograma da Recência
    # -----------------
    st.subheader("📅 Distribuição da Recência (Dias)")
    fig, ax = plt.subplots()
    ax.hist(rfm['recencia_dias'], bins=20, color='skyblue', edgecolor='black')
    plt.xlabel('Dias desde a última compra')
    plt.ylabel('Quantidade de Clientes')
    plt.title('Histograma da Recência')
    st.pyplot(fig)

    # -----------------
    # Boxplot - Ticket Médio por Status
    # -----------------
    st.subheader("💳 Distribuição do Ticket Médio por Status de Cliente")
    fig, ax = plt.subplots()
    sns.boxplot(x='status_cliente', y='ticket_medio', data=rfm, palette='Set3', ax=ax)
    plt.title('Boxplot do Ticket Médio por Status')
    plt.ylabel('Ticket Médio (R$)')
    plt.xlabel('Status do Cliente')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # -----------------
    # Heatmap de Correlação
    # -----------------
    st.subheader("📈 Correlação entre as Variáveis RFM")
    corr = rfm[['recencia_dias', 'frequencia_pedidos', 'valor_total_gasto', 'ticket_medio']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='Blues', fmt=".2f", ax=ax)
    plt.title('Matriz de Correlação entre RFM')
    st.pyplot(fig)

    # -----------------
    # Scatterplot - Frequência x Valor Monetário
    # -----------------
    st.subheader("📊 Relação entre Frequência de Pedidos e Valor Total Gasto")

    # Checando os valores únicos reais
    # print(rfm['status_cliente'].unique())
    
    # Definindo as cores corretas para cada grupo real
    cores_personalizadas = {
        'Cliente Ativo': 'green',
        'Risco de Churn': 'orange',
        'Inativo': 'red'
    }
    
    fig, ax = plt.subplots()
    sns.scatterplot(
        x='frequencia_pedidos',
        y='valor_total_gasto',
        hue='status_cliente',
        data=rfm,
        palette=cores_personalizadas,
        ax=ax
    )
    plt.title('Frequência vs Valor Total Gasto (colorido por Status)')
    plt.xlabel('Frequência de Pedidos')
    plt.ylabel('Valor Total Gasto (R$)')
    plt.legend(title='Status do Cliente')
    st.pyplot(fig)
      

    st.markdown("""
    > **Observações da Análise Exploratória:**
    
    - **Formação de Clusters Visuais:** Ao observar o scatterplot, é possível identificar **grupos naturais de clientes com comportamentos semelhantes** em relação à frequência de pedidos e ao valor gasto. Esses clusters reforçam a segmentação feita previamente (Ativos, Risco de Churn, Inativos).
    
    - **Presença de Outliers:** Durante a análise, foram identificados alguns clientes com **valores muito acima da média**, tanto em gasto quanto em frequência de pedidos.  
    Por se tratarem de comportamentos legítimos de clientes de alto valor, **optamos por não remover esses outliers**, preservando a representatividade dos dados reais.
    
    - **Correlação:** Não foi observada correlação forte entre as variáveis RFM, mas a dispersão visual ajuda a entender melhor os diferentes perfis de cliente.
    """, unsafe_allow_html=True)


# --------------------------
# Aba 6 - Conclusões e Próximos Passos
# --------------------------

with tab6:
    st.header("📋 Conclusões e Próximos Passos")

    st.markdown("""
    ### ✅ Principais Conclusões:

    - **Clientes Ativos** demonstram maior frequência de compra e maior valor de gasto médio por pedido.
    - **Clientes em Risco de Churn** já apresentam sinais claros de queda no engajamento, com menor frequência e menor ticket médio.
    - **Clientes Inativos** ainda mantêm um gasto acumulado relativamente alto, sugerindo que muitos deles já foram clientes valiosos no passado.
    - A análise exploratória identificou **clusters visuais distintos no comportamento dos clientes**, reforçando a segmentação feita.
    - Foram encontrados **outliers de clientes com gastos muito altos**, mas optamos por mantê-los na base para preservar a realidade dos dados.

    ---

    ### 🚀 Próximos Passos Recomendados:

    - **Implementar um Modelo Preditivo de Churn:**  
    Para antecipar o risco de perda de clientes, com base nas variáveis RFM e possíveis outras variáveis comportamentais.

    - **Desenvolver Campanhas de Retenção Personalizadas:**  
    Criar ações de reengajamento focadas nos clientes em risco e inativos, com base nos insights obtidos.

    - **Monitoramento Contínuo:**  
    Criar um processo automatizado de atualização da segmentação RFM e dos KPIs, para que a análise seja usada de forma recorrente pela área de negócios.

    - **Evoluir o Dashboard:**  
    Incorporar filtros interativos, análises temporais e outros indicadores avançados.

    ---

    ### 💡 Observação Final:

    Este projeto foi desenvolvido com foco em aplicar conceitos fundamentais de **Ciência de Dados aplicada a Negócios**, envolvendo **SQL**, **Python (Pandas, Matplotlib, Seaborn)** e **Streamlit**.

    Todo o código, documentação e storytelling estão disponíveis no repositório deste projeto.

    """)









