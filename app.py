import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import warnings

warnings.filterwarnings('ignore')

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="Painel de Imunização - Recife",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ESTILIZAÇÃO CSS - DARK SLATE EXECUTIVE
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    
    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    
    div[data-testid="stMetricLabel"] {
        color: #94a3b8 !important;
        font-size: 0.85rem !important;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div[data-testid="stMetricValue"] {
        color: #38bdf8 !important;
        font-weight: 700;
    }
    
    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1e293b;
        padding: 6px;
        border-radius: 12px;
        border: 1px solid #334155;
    }

    .stTabs [data-baseweb="tab"] {
        height: 45px;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 600;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #0284c7 !important;
        color: #ffffff !important;
    }
    
    /* Custom Header Container */
    .header-container {
        background: linear-gradient(90deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
    }
    
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================
# LEITURA E TRATAMENTO DOS DADOS
# =========================
@st.cache_data(show_spinner=False)
def carregar_dados():
    caminhos = ['vacinados.csv', 'vacinas.csv', 'dados.csv']
    df = None
    
    for cam in caminhos:
        try:
            df = pd.read_csv(cam, encoding='utf-8')
            break
        except Exception:
            try:
                df = pd.read_csv(cam, encoding='latin1', sep=None, engine='python')
                break
            except Exception:
                continue

    # Fallback seguro para teste caso o CSV não esteja presente
    if df is None or df.empty:
        df = pd.DataFrame({
            'cpf': ['***.481.424-**', '***.182.124-**', '***.380.000-**', '***.586.090-**', '***.876.660-**'],
            'nome': ['GERALDA', 'UPINHA', 'AAKILLES', 'AALEXSAN', 'AANDRESSA'],
            'sexo': ['FEMININO', 'MASCULINO', 'MASCULINO', 'MASCULINO', 'FEMININO'],
            'grupo': ['PÚBLICO', 'PÚBLICO', 'CRIANÇA', 'IDOSOS', 'CRIANÇA'],
            'vacina': ['3 - COMIRNATY', '1 - CORONAVAC', '1 - CORONAVAC', '2 - CHADOX1', '5 - COMIRNATY'],
            'lote': ['FN9509', '210527', '210527', '21PVCD38', 'FP8290'],
            'dose': [4, 2, 1, 3, 1],
            'local_vacinacao': ['DRIVE THRU GERALDÃO', 'UPINHA UR 04/05', 'CENTRO DE VACINAÇÃO UNICAP', 'SESAU - BUSCA ATIVA', 'CENTRO DE VACINAÇÃO UNICAP']
        })

    df.columns = [c.lower().strip() for c in df.columns]
    
    if 'dose' in df.columns:
        df['dose'] = pd.to_numeric(df['dose'], errors='coerce').fillna(1).astype(int)
    else:
        df['dose'] = 1

    if 'vacina' in df.columns:
        df['vacina_nome'] = df['vacina'].astype(str).str.replace(r'^\d+\s*-\s*', '', regex=True)
    else:
        df['vacina_nome'] = 'Não Informada'

    return df

df = carregar_dados()

# =========================
# BARRA LATERAL (FILTROS)
# =========================
with st.sidebar:
    st.image("https://img.icons8.com/isometric-line/100/38bdf8/syringe.png", width=64)
    st.title("Filtros Globais")
    st.caption("Ajuste os parâmetros abaixo:")
    
    vacinas_opt = ["Todas"] + sorted(list(df["vacina_nome"].dropna().unique()))
    vacina_sel = st.selectbox("💉 Fabricante / Vacina", vacinas_opt)
    
    if 'sexo' in df.columns:
        sexo_opt = ["Todos"] + sorted(list(df['sexo'].dropna().unique()))
        sexo_sel = st.selectbox("👥 Gênero", sexo_opt)
    else:
        sexo_sel = "Todos"

    if 'grupo' in df.columns:
        grupo_opt = ["Todos"] + sorted(list(df['grupo'].dropna().unique()))
        grupo_sel = st.selectbox("🏷️ Grupo Prioritário", grupo_opt)
    else:
        grupo_sel = "Todos"

# Aplicação dos Filtros
df_f = df.copy()

if vacina_sel != "Todas":
    df_f = df_f[df_f["vacina_nome"] == vacina_sel]
if sexo_sel != "Todos" and 'sexo' in df_f.columns:
    df_f = df_f[df_f['sexo'] == sexo_sel]
if grupo_sel != "Todos" and 'grupo' in df_f.columns:
    df_f = df_f[df_f['grupo'] == grupo_sel]

# =========================
# CABEÇALHO PRINCIPAL
# =========================
st.markdown("""
<div class="header-container">
    <h1 style="margin:0; font-size: 1.8rem; font-weight:700; color:#f8fafc;">🛡️ Central de Imunização e Vacinação</h1>
    <p style="margin: 0.3rem 0 0 0; color:#94a3b8; font-size: 0.9rem;">
        Acompanhamento analítico de aplicação de doses, distribuição por locais e público-alvo.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================
# METRICAS (KPIs)
# =========================
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_doses = len(df_f)
cpf_col = 'cpf' if 'cpf' in df_f.columns else df_f.columns[0]
total_pessoas = df_f[cpf_col].nunique()
doses_reforco = len(df_f[df_f['dose'] >= 3])
local_col = 'local_vacinacao' if 'local_vacinacao' in df_f.columns else df_f.columns[-1]
total_locais = df_f[local_col].nunique()
top_vacina = df_f['vacina_nome'].mode()[0] if not df_f.empty else "N/A"

kpi1.metric("Total de Doses", f"{total_doses:,}")
kpi2.metric("Pessoas Únicas", f"{total_pessoas:,}")
kpi3.metric("Doses de Reforço", f"{doses_reforco:,}")
kpi4.metric("Locais Ativos", f"{total_locais}")
kpi5.metric("Vacina Mais Usada", top_vacina)

st.markdown("<br>", unsafe_allow_html=True)

# Função auxiliar de tema para os gráficos Plotly Dark
def aplicar_tema_dark(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#94a3b8", family="Inter, sans-serif"),
        margin=dict(l=20, r=20, t=40, b=20),
        height=360
    )
    fig.update_xaxes(showgrid=True, gridcolor="#334155")
    fig.update_yaxes(showgrid=True, gridcolor="#334155")
    return fig

# =========================
# NAVEGAÇÃO POR ABAS
# =========================
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Visão Geral", 
    "💉 Vacinas & Doses", 
    "📍 Locais & Grupos", 
    "📄 Tabela de Dados"
])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    col_a, col_b = st.columns([1.2, 1])
    
    with col_a:
        st.subheader("Distribuição das Doses Aplicadas")
        dose_df = df_f['dose'].value_counts().reset_index()
        dose_df.columns = ['Dose', 'Quantidade']
        dose_df['Dose'] = dose_df['Dose'].astype(str) + "ª Dose"
        
        # CORREÇÃO: Utilizando lista explícita de cores no tom Cyan/Teal
        fig_dose = px.bar(
            dose_df, x='Dose', y='Quantidade',
            color='Quantidade',
            color_continuous_scale=['#0284c7', '#38bdf8', '#7dd3fc']
        )
        fig_dose.update_layout(coloraxis_showscale=False)
        st.plotly_chart(aplicar_tema_dark(fig_dose), use_container_width=True)

    with col_b:
        st.subheader("Divisão por Gênero")
        if 'sexo' in df_f.columns:
            sexo_df = df_f['sexo'].value_counts().reset_index()
            sexo_df.columns = ['Gênero', 'Quantidade']
            fig_sexo = px.pie(
                sexo_df, values='Quantidade', names='Gênero', hole=0.6,
                color_discrete_sequence=['#0284c7', '#ec4899', '#38bdf8']
            )
            st.plotly_chart(aplicar_tema_dark(fig_sexo), use_container_width=True)
        else:
            st.info("Coluna 'sexo' não disponível nos dados.")

# --- ABA 2: VACINAS & DOSES ---
with tab2:
    st.subheader("Volume de Aplicações por Fabricante")
    vac_df = df_f['vacina_nome'].value_counts().reset_index()
    vac_df.columns = ['Vacina', 'Quantidade']
    
    # CORREÇÃO: Utilizando escala de cores segura
    fig_vac = px.bar(
        vac_df, x='Quantidade', y='Vacina', orientation='h',
        color='Quantidade', color_continuous_scale=['#0f766e', '#14b8a6', '#2dd4bf']
    )
    fig_vac.update_layout(coloraxis_showscale=False, yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(aplicar_tema_dark(fig_vac), use_container_width=True)

# --- ABA 3: LOCAIS & GRUPOS ---
with tab3:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Top 8 Locais com Maior Atendimento")
        loc_df = df_f[local_col].value_counts().head(8).reset_index()
        loc_df.columns = ['Local', 'Quantidade']
        
        fig_loc = px.bar(
            loc_df, x='Quantidade', y='Local', orientation='h',
            color_discrete_sequence=['#38bdf8']
        )
        fig_loc.update_layout(yaxis=dict(categoryorder='total ascending'))
        st.plotly_chart(aplicar_tema_dark(fig_loc), use_container_width=True)

    with c2:
        st.subheader("Atendimento por Grupo Prioritário")
        if 'grupo' in df_f.columns:
            grp_df = df_f['grupo'].value_counts().head(8).reset_index()
            grp_df.columns = ['Grupo', 'Quantidade']
            
            fig_grp = px.bar(
                grp_df, x='Grupo', y='Quantidade',
                color_discrete_sequence=['#4ade80']
            )
            st.plotly_chart(aplicar_tema_dark(fig_grp), use_container_width=True)
        else:
            st.info("Coluna 'grupo' não disponível.")

# --- ABA 4: TABELA DE DADOS ---
with tab4:
    st.subheader("Registros Detalhados")
    st.dataframe(
        df_f,
        use_container_width=True,
        height=450,
        hide_index=True
    )
