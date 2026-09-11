import pandas as pd
import streamlit as st
import plotly.express as px
from pathlib import Path

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="SmartStock",
    page_icon="📦",
    layout="wide"
)

# =========================
# CARREGAMENTO DOS DADOS
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
ARQUIVO_DADOS = BASE_DIR / "database" / "materiais.csv"

df = pd.read_csv(ARQUIVO_DADOS)

# =========================
# REGRAS DE NEGÓCIO
# =========================

# Consumo médio diário
df["consumo_medio_diario"] = (
    df["consumo_medio_mensal"] / 30
)

# Estoque de segurança simples:
# 7 dias de consumo médio
df["estoque_seguranca"] = (
    df["consumo_medio_diario"] * 7
)

# Ponto de reposição
df["ponto_reposicao"] = (
    df["consumo_medio_diario"] * df["lead_time_dias"]
    + df["estoque_seguranca"]
)

# Status do material
df["status"] = df.apply(
    lambda linha: "Comprar"
    if linha["estoque_atual"] <= linha["ponto_reposicao"]
    else "OK",
    axis=1
)

# Cobertura de estoque em dias
df["cobertura_dias"] = (
    df["estoque_atual"] /
    df["consumo_medio_diario"]
)

# Identificação de possível excesso de estoque
df["estoque_excesso"] = (
    df["cobertura_dias"] > 180
)

df["quantidade_excedente"] = (
    df["estoque_atual"] -
    (df["consumo_medio_diario"] * 180)
).clip(lower=0)

df["capital_excedente"] = (
    df["quantidade_excedente"] *
    df["custo_unitario"]
)
# =========================
# CURVA ABC
# =========================

# Ordena os materiais do maior para o menor valor em estoque
df = df.sort_values(
    "valor_estoque",
    ascending=False
).reset_index(drop=True)

# Percentual que cada item representa no valor total do estoque
df["percentual_valor"] = (
    df["valor_estoque"] /
    df["valor_estoque"].sum()
)

# Percentual acumulado
df["percentual_acumulado"] = (
    df["percentual_valor"].cumsum()
)

# Classificação ABC
def classificar_abc(percentual):
    if percentual <= 0.80:
        return "A"
    elif percentual <= 0.95:
        return "B"
    else:
        return "C"

df["classe_abc"] = (
    df["percentual_acumulado"]
    .apply(classificar_abc)
)
# =========================
# CABEÇALHO
# =========================
st.title("📦 SmartStock")
st.subheader("Gestão Inteligente de Almoxarifado")

st.caption(
    "Projeto de portfólio para análise de estoque, "
    "monitoramento de indicadores e apoio à decisão de compras."
)

# =========================
# KPIs
# =========================
valor_total = df["valor_estoque"].sum()

itens_reposicao = (
    df["status"] == "Comprar"
).sum()

total_materiais = len(df)

estoque_critico = (
    df["cobertura_dias"] < 15
).sum()

col1, col2, col3, col4 = st.columns(4)

valor_formatado = (
    f"{valor_total:,.2f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

col1.metric(
    "💰 Valor em estoque",
    f"R$ {valor_formatado}"
)

col2.metric(
    "📦 Materiais",
    total_materiais
)

col3.metric(
    "⚠️ Reposição necessária",
    itens_reposicao
)

col4.metric(
    "🚨 Cobertura < 15 dias",
    estoque_critico
)

st.divider()

# =========================
# GRÁFICOS
# =========================
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:

    st.subheader("Valor de estoque por categoria")

    valor_categoria = (
        df.groupby("categoria", as_index=False)
        ["valor_estoque"]
        .sum()
    )

    fig_categoria = px.bar(
        valor_categoria,
        x="categoria",
        y="valor_estoque",
        labels={
            "categoria": "Categoria",
            "valor_estoque": "Valor em estoque"
        }
    )

    st.plotly_chart(
        fig_categoria,
        use_container_width=True
    )

with col_grafico2:

    st.subheader("Situação de reposição")

    status_contagem = (
        df["status"]
        .value_counts()
        .reset_index()
    )

    status_contagem.columns = [
        "status",
        "quantidade"
    ]

    fig_status = px.pie(
        status_contagem,
        names="status",
        values="quantidade"
    )

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

# =========================
# CURVA ABC
# =========================
st.divider()

st.subheader("📊 Curva ABC do Estoque")

resumo_abc = (
    df.groupby("classe_abc", as_index=False)
    .agg(
        quantidade_itens=("codigo", "count"),
        valor_estoque=("valor_estoque", "sum")
    )
)

fig_abc = px.bar(
    resumo_abc,
    x="classe_abc",
    y="valor_estoque",
    text="quantidade_itens",
    labels={
        "classe_abc": "Classe ABC",
        "valor_estoque": "Valor em estoque",
        "quantidade_itens": "Quantidade de itens"
    }
)

fig_abc.update_traces(
    texttemplate="%{text} itens",
    textposition="outside"
)

st.plotly_chart(
    fig_abc,
    use_container_width=True
)

st.caption(
    "Classe A: itens que concentram aproximadamente 80% do valor do estoque. "
    "Classe B: faixa seguinte até 95%. "
    "Classe C: itens que representam os 5% finais."
)

# =========================
# CAPITAL EM POSSÍVEL EXCESSO
# =========================
st.divider()

st.subheader("💤 Possível Excesso de Estoque")

capital_excedente_total = df["capital_excedente"].sum()

capital_excedente_formatado = (
    f"{capital_excedente_total:,.2f}"
    .replace(",", "X")
    .replace(".", ",")
    .replace("X", ".")
)

col_excesso1, col_excesso2 = st.columns(2)

col_excesso1.metric(
    "Capital potencialmente imobilizado",
    f"R$ {capital_excedente_formatado}"
)

col_excesso2.metric(
    "Materiais com cobertura > 180 dias",
    int(df["estoque_excesso"].sum())
)

excessos = (
    df[df["estoque_excesso"]]
    .sort_values("capital_excedente", ascending=False)
    [
        [
            "codigo",
            "descricao",
            "categoria",
            "estoque_atual",
            "cobertura_dias",
            "capital_excedente"
        ]
    ]
    .copy()
)

excessos["cobertura_dias"] = (
    excessos["cobertura_dias"].round(0)
)

excessos["capital_excedente"] = (
    excessos["capital_excedente"].round(2)
)

st.dataframe(
    excessos,
    use_container_width=True,
    hide_index=True
)

st.caption(
    "Critério demonstrativo: materiais com cobertura superior "
    "a 180 dias são sinalizados para análise gerencial."
)
# =========================
# RECOMENDAÇÕES
# =========================
st.divider()

st.subheader("🛒 Central de Recomendações")

itens_compra = df[
    df["status"] == "Comprar"
].copy()

itens_compra = itens_compra[
    [
        "codigo",
        "descricao",
        "categoria",
        "estoque_atual",
        "consumo_medio_mensal",
        "lead_time_dias",
        "ponto_reposicao",
        "cobertura_dias"
    ]
]

itens_compra["ponto_reposicao"] = (
    itens_compra["ponto_reposicao"]
    .round(0)
)

itens_compra["cobertura_dias"] = (
    itens_compra["cobertura_dias"]
    .round(1)
)

st.dataframe(
    itens_compra,
    use_container_width=True,
    hide_index=True
)

st.info(
    "Os alertas são calculados considerando consumo médio, "
    "lead time do fornecedor e estoque de segurança."
)

# =========================
# DADOS DO PROJETO
# =========================
with st.expander("Sobre o projeto"):
    st.write(
        """
        O SmartStock é um projeto autoral de gestão inteligente
        de almoxarifado.

        O objetivo é transformar dados de estoque em informações
        úteis para compras, planejamento e tomada de decisão.

        Todos os dados utilizados nesta demonstração são fictícios.
        """
    )