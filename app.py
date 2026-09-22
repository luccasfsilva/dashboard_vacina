import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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
# CSS - ESTILO VISUAL
# =========================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', system-ui, sans-serif; }
    .stApp { background: linear-gradient(135deg, #e0e7ff 0%, #d1d5ff 30%, #c7b8ff 60%, #a5b4fc 100%); }
    .block-container { padding: 1rem 2rem 3rem 2rem; max-width: 100%; }
    
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.5);
        min-width: 220px !important;
        max-width: 220px !important;
    }
    
    .main-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(20px);
        border-radius: 24px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(139, 92, 246, 0.08);
        border: 1px solid rgba(255,255,255,0.6);
        margin-bottom: 1rem;
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
    }
    
    .big-number { font-size: 1.8rem; font-weight: 800; line-height: 1; }
    .big-number.purple { color: #7c3aed; }
    .big-number.blue { color: #3b82f6; }
    .big-number.pink { color: #ec4899; }
    .big-number.cyan { color: #06b6d4; }
    
    .number-label { font-size: 0.8rem; color: #9ca3af; margin-top: 0.4rem; font-weight: 500; }
    .metric-row { display: flex; gap: 1rem; align-items: center; }
    .metric-badge { width: 40px; height: 40px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }
    
    .badge-purple { background: linear-gradient(135deg, #c4b5fd, #a78bfa); }
    .badge-blue { background: linear-gradient(135deg, #93c5fd, #60a5fa); }
    .badge-pink { background: linear-gradient(135deg, #f9a8d4, #f472b6); }
    .badge-cyan { background: linear-gradient(135deg, #67e8f9, #22d3ee); }
    .badge-orange { background: linear-gradient(135deg, #fdba74, #fb923c); }
    
    #MainMenu, footer, header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# =========================
# CARREGAMENTO DOS DADOS (COM FALLBACK SE O ARQUIVO FALHAR)
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

    # Se não encontrar o arquivo no repositório, gera dados fictícios para a aplicação NÃO quebrar
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

    # Padronização de nomes das colunas
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
# SIDEBAR
# =========================
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; margin-bottom: 1.5rem;">
            <div style="font-size: 2.5rem;">💉</div>
            <div style="font-weight: 800; font-size: 1.1rem; color: #1f2937;">VaciAnalytics</div>
            <div style="font-size: 0.75rem; color: #9ca3af;">Painel de Imunização</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="font-size: 0.8rem; font-weight: 700; color: #6b7280; text-transform: uppercase; margin-bottom: 0.5rem;">⚙️ Filtros</div>', unsafe_allow_html=True)
    
    vacinas_opt = ["Todas"] + sorted(list(df["vacina_nome"].unique()))
    vacina_sel = st.selectbox("Vacina", vacinas_opt)
    
    sexo_col = 'sexo' if 'sexo' in df.columns else None
    if sexo_col:
        sexo_opt = ["Todos"] + sorted(list(df[sexo_col].dropna().unique()))
        sexo_sel = st.selectbox("Gênero", sexo_opt)
    else:
        sexo_sel = "Todos"

# =========================
# FILTRAGEM DOS DADOS
# =========================
df_f = df.copy()

if vacina_sel != "Todas":
    df_f = df_f[df_f["vacina_nome"] == vacina_sel]
if sexo_sel != "Todos" and sexo_col:
    df_f = df_f[df_f[sexo_col] == sexo_sel]

# =========================
# HEADER
# =========================
st.markdown(f"""
    <div class="header-bar">
        <div>
            <div class="app-title">💉 Dashboard de Vacinação</div>
            <div style="font-size: 0.8rem; color: #9ca3af; margin-top: 0.2rem;">{len(df_f):,} registros encontrados</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# =========================
# CARDS DE MÉTRICAS (KPIs)
# =========================
c1, c2, c3, c4 = st.columns(4)

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
    cpf_col = 'cpf' if 'cpf' in df.columns else df_f.columns[0]
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-blue">👤</div>
                <div>
                    <div class="big-number blue">{df_f[cpf_col].nunique():,}</div>
                    <div class="number-label">Pessoas Atendidas</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c3:
    reforco_qtd = len(df_f[df_f['dose'] >= 3])
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-pink">🔁</div>
                <div>
                    <div class="big-number pink">{reforco_qtd:,}</div>
                    <div class="number-label">Doses de Reforço</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

with c4:
    local_col = 'local_vacinacao' if 'local_vacinacao' in df.columns else df_f.columns[-1]
    st.markdown(f"""
        <div class="main-card">
            <div class="metric-row">
                <div class="metric-badge badge-cyan">📍</div>
                <div>
                    <div class="big-number cyan">{df_f[local_col].nunique()}</div>
                    <div class="number-label">Pontos de Vacinação</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# =========================
# GRÁFICOS
# =========================
def tema_claro(fig):
    fig.update_layout(
        plot_bgcolor='rgba(255,255,255,0.3)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#4b5563', family='Inter, sans-serif', size=11),
        margin=dict(l=20, r=20, t=40, b=20),
        height=320
    )
    return fig

col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    vac_counts = df_f['vacina_nome'].value_counts().reset_index()
    vac_counts.columns = ['Vacina', 'Qtd']
    fig1 = px.bar(vac_counts, x='Vacina', y='Qtd', title="🧪 Aplicações por Vacina", color='Qtd', color_continuous_scale=['#c4b5fd', '#7c3aed'])
    fig1.update_layout(coloraxis_showscale=False)
    st.plotly_chart(tema_claro(fig1), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    loc_counts = df_f[local_col].value_counts().head(7).reset_index()
    loc_counts.columns = ['Local', 'Qtd']
    fig2 = px.bar(loc_counts, x='Qtd', y='Local', orientation='h', title="🏆 Top Locais de Vacinação", color='Qtd', color_continuous_scale=['#ddd6fe', '#7c3aed'])
    fig2.update_layout(coloraxis_showscale=False, yaxis=dict(categoryorder='total ascending'))
    st.plotly_chart(tema_claro(fig2), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# TABELA DE DADOS
# =========================
st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="card-title">🔍 Registros Detalhados</div>', unsafe_allow_html=True)
st.dataframe(df_f, use_container_width=True, height=350, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)
