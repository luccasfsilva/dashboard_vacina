import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings

warnings.filterwarnings('ignore')

# =========================
# CONFIGURAÇÃO
# =========================
st.set_page_config(
    page_title="VaciAnalytics",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# CSS - VISUAL EXATO
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', system-ui, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #e0e7ff 0%, #d1d5ff 30%, #c7b8ff 60%, #a5b4fc 100%);
    }
    
    .block-container {
        padding: 1rem 2rem 3rem 2rem;
        max-width: 100%;
    }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.5);
        min-width: 220px !important;
        max-width: 220px !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    
    .main-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 
            0 4px 20px rgba(139, 92, 246, 0.08),
            0 1px 3px rgba(0,0,0,0.05),
            inset 0 1px 0 rgba(255,255,255,0.6);
        border: 1px solid rgba(255,255,255,0.6);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .main-card:hover {
        transform: translateY(-2px);
        box-shadow: 
            0 8px 30px rgba(139, 92, 246, 0.15),
            0 2px 5px rgba(0,0,0,0.08),
            inset 0 1px 0 rgba(255,255,255,0.8);
    }
    
    .header-bar {
        background: rgba(255, 255, 255, 0.9);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 1rem 2rem;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(255,255,255,0.6);
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .app-title {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #7c3aed, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    
    .nav-item {
        display: flex;
        align-items: center;
        gap: 0.8rem;
        padding: 0.9rem 1rem;
        border-radius: 16px;
        margin-bottom: 0.3rem;
        cursor: pointer;
        transition: all 0.3s ease;
        color: #6b7280;
        font-weight: 500;
        font-size: 0.9rem;
    }
    
    .nav-item:hover {
        background: rgba(124, 58, 237, 0.08);
        color: #7c3aed;
    }
    
    .nav-item.active {
        background: linear-gradient(135deg, #8b5cf6, #7c3aed);
        color: white;
        box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);
    }
    
    .nav-icon {
        font-size: 1.3rem;
        width: 28px;
        text-align: center;
    }
    
    .card-title {
        font-size: 0.85rem;
        font-weight: 600;
        color: #6b7280;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
    }
    
    .big-number {
        font-size: 2rem;
        font-weight: 800;
        color: #1f2937;
        line-height: 1;
    }
    
    .big-number.purple { color: #7c3aed; }
    .big-number.blue { color: #3b82f6; }
    .big-number.pink { color: #ec4899; }
    .big-number.cyan { color: #06b6d4; }
    
    .number-label {
        font-size: 0.8rem;
        color: #9ca3af;
        margin-top: 0.4rem;
        font-weight: 500;
    }
    
    .filter-pill {
        background: rgba(255,255,255,0.9);
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 0.5rem 1rem;
        font-size: 0.85rem;
        font-weight: 500;
        color: #6b7280;
    }
    
    .filter-pill.active {
        border-color: #8b5cf6;
        color: #7c3aed;
        background: rgba(139, 92, 246, 0.05);
    }
    
    #MainMenu, footer, header {
        visibility: hidden;
    }
    
    .metric-row {
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .metric-badge {
        width: 40px;
        height: 40px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
    }
    
    .badge-purple { background: linear-gradient(135deg, #c4b5fd, #a78bfa); }
    .badge-blue { background: linear-gradient(135deg, #93c5fd, #60a5fa); }
    .badge-pink { background: linear-gradient(135deg, #f9a8d4, #f472b6); }
    .badge-cyan { background: linear-gradient(135deg, #67e8f9, #22d3ee); }
    .badge-orange { background: linear-gradient(135deg, #fdba74, #fb923c); }
</style>
""", unsafe_allow_html=True)

# =========================
# CARREGAMENTO DE DADOS
# =========================
@st.cache_data(show_spinner=False)
def carregar_dados():
    # Substitua 'vacinados.csv' ou o caminho/URL correspondente da sua planilha
    try:
        df = pd.read_csv('vacinados.csv') # ou pd.read_excel('vacinados.xlsx')
    except Exception:
        # Fallback de dados para demonstração se não encontrar o arquivo
        df = pd.DataFrame({
            'cpf': ['***.481.424-**', '***.182.124-**', '***.380.000-**', '***.586.090-**'],
            'nome': ['GERALDA', 'UPINHA', 'AAKILLES', 'AALEXSAN'],
            'sexo': ['FEMININO', 'MASCULINO', 'MASCULINO', 'MASCULINO'],
            'grupo': ['PÚBLICO', 'PÚBLICO', 'CRIANÇA', 'IDOSOS'],
            'vacina': ['3 - COMIRNATY', '1 - CORONAVAC', '1 - CORONAVAC', '2 - CHADOX1'],
            'lote': ['FN9509', '210527', '210527', '21PVCD38'],
            'dose': [4, 2, 1, 3],
            'data_vacinacao': pd.to_datetime(['2022-01-15', '2022-02-10', '2022-02-12', '2022-03-01']),
            'local_vacinacao': ['DRIVE THRU GERALDÃO', 'UPINHA UR 04/05', 'CENTRO DE VACINAÇÃO UNICAP', 'SESAU - BUSCA ATIVA']
        })
    
    # Tratamento simples dos dados
    df['dose'] = pd.to_numeric(df['dose'], errors='coerce').fillna(1).astype(int)
    if 'data_vacinacao' in df.columns:
        df['data_vacinacao'] = pd.to_datetime(df['data_vacinacao'], errors='coerce')
        df['ano'] = df['data_vacinacao'].dt.year.fillna(2022).astype(int)
        df['mes'] = df['data_vacinacao'].dt.month.fillna(1).astype(int)
    else:
        df['ano'] = 2022
        df['mes'] = 1

    # Limpeza básica do nome da vacina (remover prefixos como "1 - ")
    df['vacina_nome'] = df['vacina'].astype(str).str.replace(r'^\d+\s*-\s*', '', regex=True)
    return df

df = carregar_dados()

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💉</div>
            <div style="font-weight: 800; font-size: 1.1rem; color: #1f2937;">VaciAnalytics</div>
            <div style="font-size: 0.75rem; color: #9ca3af; margin-top: 0.2rem;">Painel de Imunização</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="nav-item active">
            <span class="nav-icon">🏠</span>
            <span>Visão Geral</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">💉</span>
            <span>Doses</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">👥</span>
            <span>Grupos</span>
        </div>
        <div class="nav-item">
            <span class="nav-icon">📍</span>
            <span>Locais</span>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div style="font-size: 0.8rem; font-weight: 700; color: #6b7280; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">⚙️ Filtros</div>', unsafe_allow_html=True)
    
    # Filtro por Vacina
    vacinas_opt = ["Todas"] + list(df["vacina_nome"].unique())
    vacina_sel = st.selectbox("Vacina", vacinas_opt)
    
    # Filtro por Sexo
    sexo_opt = ["Todos"] + list(df["sexo"].dropna().unique())
    sexo_sel = st.selectbox("Gênero", sexo_opt)

    # Filtro por Grupo
    grupo_opt = ["Todos"] + list(df["grupo"].dropna().unique())
    grupo_sel = st.selectbox("Grupo Prioritário", grupo_opt)

# =========================
# FILTRAR DADOS
# =========================
df_f = df.copy()

if vacina_sel != "Todas":
    df_f = df_f[df_f["vacina_nome"] == vacina_sel]
if sexo_sel != "Todos":
    df_f = df_f[df_f["sexo"] == sexo_sel]
if grupo_sel != "Todos":
    df_f = df_f[df_f["grupo"] == grupo_sel]

if df_f.empty:
    st.error("Nenhum registro encontrado com os filtros selecionados.")
    st.stop()

# =========================
# HEADER
# =========================
st.markdown(f"""
    <div class="header-bar">
        <div>
            <div class="app-title">💉 VaciAnalytics Recife</div>
            <div style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.2rem;">{len(df_f):,} doses registradas na seleção</div>
        </div>
        <div style="display: flex; gap: 0.5rem;">
            <span class="filter-pill active">📊 Doses Total</span>
            <span class="filter-pill">🏥 Locais</span>
            <span class="filter-pill">💊 Vacinas</span>
        </div>
    </div>
""", unsafe_allow_html=True)

# =========================
# KPI ROW
# =========================
c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-purple">💉</div>
                <div>
                    <div class="big-number purple">{len(df_f):,}</div>
                    <div class="number-label">Total de Doses</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c2:
    pacientes_unicos = df_f['cpf'].nunique()
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-blue">👤</div>
                <div>
                    <div class="big-number blue">{pacientes_unicos:,}</div>
                    <div class="number-label">Pessoas Imunizadas</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    dose_reforco = len(df_f[df_f['dose'] >= 3])
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-pink">🔁</div>
                <div>
                    <div class="big-number pink">{dose_reforco:,}</div>
                    <div class="number-label">Doses de Reforço (3ª+)</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    locais_qtd = df_f['local_vacinacao'].nunique()
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-cyan">📍</div>
                <div>
                    <div class="big-number cyan">{locais_qtd}</div>
                    <div class="number-label">Locais Ativos</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c5:
    top_vacina = df_f['vacina_nome'].mode()[0] if not df_f.empty else "N/A"
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-orange">🧪</div>
                <div>
                    <div class="big-number" style="color: #f97316; font-size: 1.2rem;">{top_vacina}</div>
                    <div class="number-label">Vacina Mais Aplicada</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# =========================
# GRÁFICOS - TEMA CLARO
# =========================
def tema_claro(fig, h=320):
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#4b5563', family='Inter, sans-serif', size=11),
        title_font=dict(size=13, color='#1f2937', family='Inter, sans-serif'),
        margin=dict(l=40, r=30, t=50, b=40),
        height=h,
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1, bgcolor='rgba(0,0,0,0)'),
        hoverlabel=dict(bgcolor='white', bordercolor='#e5e7eb', font=dict(color='#1f2937'))
    )
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)', showline=False)
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(0,0,0,0.05)', showline=False)
    return fig

# --- Gráfico 1: Aplicações por Vacina/Fabricante ---
vac_counts = df_f['vacina_nome'].value_counts().reset_index()
vac_counts.columns = ['Vacina', 'Quantidade']
fig1 = px.bar(
    vac_counts, x='Vacina', y='Quantidade',
    color='Quantidade', color_continuous_scale=['#c4b5fd', '#8b5cf6', '#7c3aed']
)
fig1.update_layout(title='🧪 Total de Doses por Vacina/Fabricante', coloraxis_showscale=False, xaxis_title='', yaxis_title='')
fig1 = tema_claro(fig1)

# --- Gráfico 2: Top Locais de Vacinação ---
top_locais = df_f['local_vacinacao'].value_counts().head(8).reset_index()
top_locais.columns = ['Local', 'Quantidade']
fig2 = px.bar(
    top_locais, x='Quantidade', y='Local', orientation='h',
    color='Quantidade', color_continuous_scale=['#ddd6fe', '#a78bfa', '#7c3aed']
)
fig2.update_layout(title='🏆 Top Locais de Vacinação', yaxis=dict(categoryorder='total ascending'), coloraxis_showscale=False, xaxis_title='', yaxis_title='')
fig2 = tema_claro(fig2)

# --- Gráfico 3: Distribuição por Sexo (Pie) ---
sexo_df = df_f['sexo'].value_counts().reset_index()
sexo_df.columns = ['Sexo', 'Qtd']
fig3 = px.pie(
    sexo_df, values='Qtd', names='Sexo', hole=0.65,
    color_discrete_sequence=['#8b5cf6', '#f472b6', '#60a5fa']
)
fig3.update_traces(textposition='outside', textinfo='label+percent')
fig3.update_layout(title='👥 Distribuição por Gênero', showlegend=False)
fig3 = tema_claro(fig3)

# --- Gráfico 4: Distribuição das Doses (1ª, 2ª, 3ª, 4ª) ---
doses_df = df_f['dose'].astype(str).value_counts().reset_index()
doses_df.columns = ['Dose', 'Qtd']
fig4 = px.bar(
    doses_df, x='Dose', y='Qtd',
    color='Dose', color_discrete_sequence=['#60a5fa', '#34d399', '#fbbf24', '#f472b6']
)
fig4.update_layout(title='📌 Proporção por Número da Dose', showlegend=False, xaxis_title='Dose', yaxis_title='')
fig4 = tema_claro(fig4)

# --- Gráfico 5: Distribuição por Grupo Prioritário ---
grupo_df = df_f['grupo'].value_counts().head(8).reset_index()
grupo_df.columns = ['Grupo', 'Qtd']
fig5 = px.bar(
    grupo_df, x='Grupo', y='Qtd',
    color_discrete_sequence=['#8b5cf6']
)
fig5.update_layout(title='📊 Doses por Grupo Prioritário', xaxis_title='', yaxis_title='')
fig5 = tema_claro(fig5)

# --- Gráfico 6: Principais Lotes ---
lotes_df = df_f['lote'].value_counts().head(6).reset_index()
lotes_df.columns = ['Lote', 'Qtd']
fig6 = px.pie(
    lotes_df, values='Qtd', names='Lote', hole=0.5,
    color_discrete_sequence=['#22d3ee', '#8b5cf6', '#f472b6', '#a78bfa', '#60a5fa']
)
fig6.update_layout(title='📦 Top Lotes Utilizados', showlegend=True)
fig6 = tema_claro(fig6)

# =========================
# LAYOUT EM GRID
# =========================
r1c1, r1c2 = st.columns([1.3, 1])
with r1c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r1c2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

r2c1, r2c2, r2c3 = st.columns([1, 1, 1])
with r2c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r2c2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r2c3:
    # Card Destaque
    top_local_nome = top_locais.iloc[0]['Local'] if not top_locais.empty else "N/A"
    top_local_qtd = top_locais.iloc[0]['Quantidade'] if not top_locais.empty else 0
    st.markdown(f"""
        <div class="main-card" style="text-align: center; display: flex; flex-direction: column; justify-content: center; height: 100%; min-height: 320px;">
            <div style="font-size: 0.85rem; font-weight: 600; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 1rem;">🏥 Maior Centro de Aplicação</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: #1f2937; margin-bottom: 0.5rem; line-height: 1.3;">{top_local_nome}</div>
            <div style="font-size: 2rem; font-weight: 800; background: linear-gradient(135deg, #8b5cf6, #ec4899); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">{top_local_qtd:,} doses</div>
            <div style="margin-top: 1rem; padding-top: 1rem; border-top: 1px solid rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-around;">
                    <div>
                        <div style="font-size: 0.75rem; color: #9ca3af;">Status</div>
                        <div style="font-weight: 700; color: #10b981;">Ativo ✅</div>
                    </div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

r3c1, r3c2 = st.columns([1.2, 1])
with r3c1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with r3c2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABELA DE DADOS
# =========================
st.markdown('<div class="main-card" style="margin-top: 1rem;">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔍 Registros de Vacinação</div>', unsafe_allow_html=True)

colunas_visiveis = st.multiselect(
    "Selecionar Colunas",
    options=df_f.columns.tolist(),
    default=['cpf', 'nome', 'sexo', 'grupo', 'vacina', 'lote', 'dose', 'local_vacinacao']
)

st.dataframe(
    df_f[colunas_visiveis],
    use_container_width=True,
    height=400,
    hide_index=True
)
st.markdown('</div>', unsafe_allow_html=True)
