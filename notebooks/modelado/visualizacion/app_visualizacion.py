import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Se realiza la lectura de los datos
df = pd.read_csv("c:/Users/aroap/Desktop/MASTER_VIU/13_METODOLOGIAS_GESTION_PROYECTOS_BIG_DATA/codigo/13MBID-OCT2324/data/final/datos_finales.csv", sep=";")

# Título del dashboard
st.write("# 13MBID - Visualización de datos")
st.write("## Panel de visualización generado sobre los datos de créditos y tarjetas emitidas a clientes de la entidad")
st.write("#### Persona/s: Aroa Palomo Vadillo")
st.write("----")

# Gráficos
st.write("### Caracterización de los créditos otorgados")

# Se tienen que agregar las definiciones de gráficos desde la libreta
creditos_x_objetivo = px.histogram(df, x='objetivo_credito', 
                                   title='Conteo de créditos por objetivo')
creditos_x_objetivo.update_layout(xaxis_title='Objetivo del crédito', yaxis_title='Cantidad')

# Se realiza la "impresión" del gráfico en el dashboard
st.plotly_chart(creditos_x_objetivo)


# Histograma de los importes de créditos otorgados
histograma_importes = px.histogram(df, x='importe_solicitado', nbins=10, title='Importes solicitados en créditos')
histograma_importes.update_layout(xaxis_title='Importe solicitado', yaxis_title='Cantidad')

st.plotly_chart(histograma_importes)


#Histogramas de los importes de crédito solicitados por objetivo y estado del crédito
chart_data = pd.concat([
    df['objetivo_credito'],
    df['importe_solicitado'],
    df['estado_credito'],
], axis=1)
chart_data = chart_data.query("""(`estado_credito` == 0) or (`estado_credito` == 1)""")
chart_data = chart_data.sort_values(['estado_credito', 'objetivo_credito'])
chart_data = chart_data.rename(columns={'objetivo_credito': 'x'})
chart_data_count = chart_data.groupby(['estado_credito','x'], dropna=False)[['importe_solicitado']].count()
chart_data_count.columns = ['importe_solicitado||count']
chart_data = chart_data_count.reset_index()
chart_data = chart_data.query("""`estado_credito` == 0""")

charts = []
charts.append(go.Bar(
    x=chart_data['x'],
    y=chart_data['importe_solicitado||count']
))
figure = go.Figure(data=charts, layout=go.Layout({
    'barmode': 'group',
    'legend': {'orientation': 'h', 'y': -0.3},
    'title': {'text': '(estado_credito: 0) - Count of importe_solicitado by objetivo_credito'},
    'xaxis': {'title': {'text': 'objetivo_credito'}},
    'yaxis': {'tickformat': '0:g', 'title': {'text': 'Count of importe_solicitado'}, 'type': 'linear'}
}))
figure.update_layout(title_text='Importe solicitado de crédito por objetivo y por estado del crédito = 0')

st.plotly_chart(figure)



# Filtros

option = st.selectbox(
    'Qué tipo de crédito desea filtrar?',
     df['objetivo_credito'].unique())

df_filtrado = df[df['objetivo_credito'] == option]

st.write(f"Tipo de crédito seleccionado: {option}")

if st.checkbox('Mostrar créditos finalizados?', value=True):

    # Conteo de ocurrencias por estado
    estado_credito_counts = df_filtrado['estado_credito'].value_counts()

    # Gráfico de torta de estos valores
    fig = go.Figure(data=[go.Pie(labels=estado_credito_counts.index, values=estado_credito_counts)])
    fig.update_layout(title_text='Distribución de créditos por estado registrado')
else:
    df_filtrado = df_filtrado[df_filtrado['estado_credito'] == 'P']
    # Conteo de ocurrencias por caso
    falta_pago_counts = df_filtrado['falta_pago'].value_counts()

    # Create a Pie chart
    fig = go.Figure(data=[go.Pie(labels=falta_pago_counts.index, values=falta_pago_counts)])
    fig.update_layout(title_text='Distribución de créditos en función de registro de mora')

st.write(f"Cantidad de créditos con estas condiciones: {df_filtrado.shape[0]}")
st.plotly_chart(fig)