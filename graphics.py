import plotly.graph_objects as go

def graficar_actuarial_interactivo(age, reserve, funeral_aid, actuarial_valuation, af3):
    fig = go.Figure()

    # 1. RESERVA (Barras)
    fig.add_trace(go.Bar(
        x=age,
        y=reserve,
        name="Reserva",
        marker_color='rgba(70, 130, 180, 0.6)', # Steelblue con transparencia
        marker_line_color='rgba(70, 130, 180, 1)',
        marker_line_width=1.5,
        hovertemplate="<b>Reserva</b><br>Edad: %{x}<br>Valor: $%{y:,.2f}<extra></extra>"
    ))

    # 2. AUXILIO FUNERAL (Barras)
    fig.add_trace(go.Bar(
        x=age,
        y=funeral_aid,
        name="Auxilio Funeral",
        marker_color='rgba(255, 165, 0, 0.6)', # Naranja con transparencia
        marker_line_color='rgba(255, 165, 0, 1)',
        marker_line_width=1.5,
        hovertemplate="<b>Auxilio Funeral</b><br>Edad: %{x}<br>Valor: $%{y:,.2f}<extra></extra>"
    ))

    # 3. CÁLCULO ACTUARIAL (Línea con puntos pequeños)
    fig.add_trace(go.Scatter(
        x=age,
        y=actuarial_valuation,
        name="Cálculo Actuarial",
        mode='lines+markers',
        line=dict(color='green', width=2),
        marker=dict(size=4), # Punto pequeño como solicitaste
        hovertemplate="<b>Cálculo Actuarial</b><br>Edad: %{x}<br>Valor: $%{y:,.2f}<extra></extra>"
    ))

    # 4. AF3 (Línea discontinua con puntos pequeños - Eje secundario)
    fig.add_trace(go.Scatter(
        x=age,
        y=af3,
        name="AF3",
        mode='lines+markers',
        line=dict(color='red', width=2, dash='dash'),
        marker=dict(size=4),
        yaxis="y2",
        hovertemplate="<b>Factor AF3</b><br>Edad: %{x}<br>Porcentaje: %{y:.2%}<extra></extra>"
    ))

    # Configuración de los Ejes y Diseño
    fig.update_layout(
        title="Componentes Reserva Actuarial (Interactivo)",
        xaxis=dict(title="Edad Actual", tickmode='linear', tickangle=45),
        yaxis=dict(
            title="Valores en Pesos",
            tickformat=",.0f", # Formato con separador de miles
            side="left"
        ),
        yaxis2=dict(
            title="Factor Actuarial (FAC3)",
            tickformat=".1%", # Formato porcentaje
            overlaying="y",
            side="right",
            showgrid=False
        ),
        hovermode="x unified", # Muestra todos los valores al mismo tiempo al pasar por la edad
        template="plotly_white",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    fig.show()

# Nota: Asegúrate de tener instalado plotly: pip install plotly