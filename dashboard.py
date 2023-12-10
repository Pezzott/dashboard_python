import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(layout="wide", page_title="Análise de dados", page_icon="📊")
st.title("Análise de dados")


df_lojas = pd.read_excel("LOJAS.xlsx")

# Criar uma nova coluna com ano e mês em formato textual
df_lojas['Mês/Ano'] = df_lojas['Data de Venda'].dt.strftime('%m/%Y')
df_lojas['Mês/Ano'] = pd.to_datetime(df_lojas['Mês/Ano'], format='%m/%Y').dt.to_period('M').dt.strftime('%B/%Y')

# Traduzir os nomes dos meses para português (opcional)
meses = {
    'January': 'Janeiro', 'February': 'Fevereiro', 'March': 'Março',
    'April': 'Abril', 'May': 'Maio', 'June': 'Junho',
    'July': 'Julho', 'August': 'Agosto', 'September': 'Setembro',
    'October': 'Outubro', 'November': 'Novembro', 'December': 'Dezembro'
}
df_lojas['Mês/Ano'] = df_lojas['Mês/Ano'].apply(lambda x: '/'.join([meses.get(item, item) for item in x.split('/')]))


opcoes_mes_ano = df_lojas['Mês/Ano'].sort_values().unique()


mes_ano_selecionado = st.sidebar.selectbox('Selecione o Mês/Ano:', opcoes_mes_ano)


df_filtrado = df_lojas[df_lojas['Mês/Ano'] == mes_ano_selecionado]





col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)



with col1:
    fig = px.bar(df_filtrado, x='Estado', y='Valor de Venda', color='Estado',
                 labels={'Valor de Venda':'Valor de Venda', 'Estado':'Estado'},
                 title='Valor de Venda por Estado')
    fig.update_layout(autosize=True)
    st.plotly_chart(fig, use_container_width=True)


with col2:
    fig_horiz = px.bar(df_filtrado, x='Valor de Venda', y='Nome do Produto', orientation='h',
                       labels={'Valor de Venda':'Valor de Venda', 'Nome do Produto':'Nome do Produto'},
                       title='Valor de Venda por Produto')
    st.plotly_chart(fig_horiz, use_container_width=True)

with col3:
  
    if df_filtrado['Data de Venda'].dtype != 'datetime64[ns]':
        df_filtrado['Data de Venda'] = pd.to_datetime(df_filtrado['Data de Venda'])

 
    fig_line = px.line(df_filtrado, x='Data de Venda', y='Valor de Venda',
                       title='Valor de Venda ao Longo do Tempo')

  
    st.plotly_chart(fig_line, use_container_width=True)

with col4:
  
    df_pizza = df_filtrado.groupby('Categoria do Produto (Roupa ou Calçado)')['Valor de Venda'].sum().reset_index()

 
    fig_pizza = px.pie(df_pizza, values='Valor de Venda', names='Categoria do Produto (Roupa ou Calçado)',
                       title='Distribuição do Valor de Venda por Categoria')

   
    st.plotly_chart(fig_pizza, use_container_width=True)

with col5:
 
    fig_histogram = px.histogram(df_filtrado, x='Nome do Vendedor', y='Valor de Venda',
                                 histfunc='sum', title='Valor de Venda por Vendedor')

  
    st.plotly_chart(fig_histogram, use_container_width=True)
