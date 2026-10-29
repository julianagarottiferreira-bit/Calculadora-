import re

import streamlit as st

st.set_page_config(page_title="Calculadora", page_icon="🧮", layout="centered")

# ---------------------------------------------------------------
# PALETA
# ---------------------------------------------------------------
CLARO = dict(
    FUNDO="#e4e3de", TECLA_1="#ebe5d8", TECLA_2="#dcd8c9", TEXTO="#2f2f2f",
    AZUL="#4b5a94", AZUL_BG="#4b5a94", VERMELHO="#d1401f",
    CARD="#ecebe6", HIST_TXT="#555555", SUTIL="#8a8a82",
    LINHA="rgba(0, 0, 0, 0.06)", SOMBRA_IGUAL="rgba(75, 90, 148, 0.35)",
)
ESCURO = dict(
    FUNDO="#1c1c1e", TECLA_1="#3b3b40", TECLA_2="#2e2e33", TEXTO="#f2f2f2",
    AZUL="#9db0ff", AZUL_BG="#5b6dc0", VERMELHO="#ff6b4a",
    CARD="#26262a", HIST_TXT="#c8c8cc", SUTIL="#8e8e93",
    LINHA="rgba(255, 255, 255, 0.08)", SOMBRA_IGUAL="rgba(91, 109, 192, 0.45)",
)

# Tema inicial: tenta seguir o tema do Streamlit/celular; depois a chave "Tema escuro" manda
if "tema_escuro" not in st.session_state:
    try:
        st.session_state.tema_escuro = st.context.theme.type == "dark"
    except Exception:
        st.session_state.tema_escuro = False

P = ESCURO if st.session_state.tema_escuro else CLARO
FUNDO = P["FUNDO"]
TECLA_1 = P["TECLA_1"]
TECLA_2 = P["TECLA_2"]
TEXTO = P["TEXTO"]
AZUL = P["AZUL"]
AZUL_BG = P["AZUL_BG"]
VERMELHO = P["VERMELHO"]
CARD = P["CARD"]
HIST_TXT = P["HIST_TXT"]
SUTIL = P["SUTIL"]
LINHA = P["LINHA"]
SOMBRA_IGUAL = P["SOMBRA_IGUAL"]

# ---------------------------------------------------------------
# 1. VISUAL (CSS)
# ---------------------------------------------------------------
st.markdown(
    f"""
<style>
/* Fundo geral (força tema claro mesmo com celular no modo escuro) */
.stApp, [data-testid="stAppViewContainer"] {{
    background: {FUNDO} !important;
}}
header[data-testid="stHeader"] {{ background: transparent !important; color: {TEXTO} !important; }}

/* Largura de celular, centralizado */
.block-container {{
    max-width: 420px !important;
    padding: 3.2rem 16px 2.5rem 16px !important;
    margin: 0 auto !important;
}}
div[data-testid="stVerticalBlock"] {{ gap: 0.75rem !important; }}

/* 4 colunas lado a lado, sempre */
div[data-testid="stHorizontalBlock"] {{
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 12px !important;
}}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {{
    width: auto !important;
    flex: 1 1 0 !important;
    min-width: 0 !important;
}}

/* Faz o botão ocupar a coluna inteira (era isso que deixava as bolinhas pequenas) */
div[data-testid="stColumn"] div[data-testid="stElementContainer"],
div.stButton {{
    width: 100% !important;
}}

/* Visor */
.visor {{
    min-height: 150px;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    text-align: right;
    word-break: break-all;
    padding: 0 10px 10px 10px;
    color: {TEXTO};
    font-weight: 300;
    line-height: 1.1;
}}

/* Teclas redondas */
div.stButton > button {{
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    aspect-ratio: 1 / 1;
    border-radius: 50% !important;
    border: none !important;
    padding: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: linear-gradient(145deg, {TECLA_1}, {TECLA_2}) !important;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.10) !important;
}}
div.stButton > button p {{
    font-size: 30px !important;
    font-weight: 400 !important;
    margin: 0 !important;
    color: {TEXTO} !important;
}}
div.stButton > button:hover,
div.stButton > button:focus,
div.stButton > button:focus:not(:active) {{
    border: none !important;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.14) !important;
}}
div.stButton > button:active {{
    transform: scale(0.94);
}}

/* Histórico */
.hist-card {{
    background: {CARD};
    border-radius: 24px;
    padding: 14px 20px 8px 20px;
    box-shadow: inset 0 2px 8px rgba(0, 0, 0, 0.07);
}}
.hist-titulo {{
    font-size: 12px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: {SUTIL};
    margin-bottom: 6px;
}}
.hist-item {{
    text-align: right;
    color: {HIST_TXT};
    font-size: 19px;
    padding: 8px 0;
    border-bottom: 1px solid {LINHA};
}}
.hist-item:last-child {{ border-bottom: none; }}
.hist-item b {{ color: {AZUL}; font-weight: 500; }}
.hist-vazio {{ color: {SUTIL}; text-align: center; padding: 14px 0; font-size: 15px; }}

/* Chave do "mostrar histórico" */
div[data-testid="stToggle"] p {{ color: {TEXTO} !important; font-size: 16px; }}
</style>
""",
    unsafe_allow_html=True,
)


# Cores por tecla (seletores mais "fortes" que a regra geral, senão não pegam)
def alvo(chaves, parte):
    return ", ".join(f"div.st-key-btn_{k} div.stButton > {parte}" for k in chaves)


OPERADORES = ["pct", "div", "mul", "sub", "add", "del"]
OPERADORES_GRANDES = ["div", "mul", "sub", "add"]

st.markdown(
    f"""
<style>
{alvo(OPERADORES, "button p")} {{ color: {AZUL} !important; }}
{alvo(OPERADORES_GRANDES, "button p")} {{ font-size: 38px !important; }}
{alvo(["c"], "button p")} {{ color: {VERMELHO} !important; }}

{alvo(["eq"], "button")} {{
    background: {AZUL_BG} !important;
    box-shadow: 0 8px 14px {SOMBRA_IGUAL} !important;
}}
{alvo(["eq"], "button p")} {{ color: #ffffff !important; font-size: 40px !important; }}

/* Botão "Limpar histórico": pequeno e retangular */
div.st-key-limpar div.stButton > button {{
    aspect-ratio: auto;
    border-radius: 16px !important;
    padding: 10px 8px !important;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.08) !important;
}}
div.st-key-limpar div.stButton > button p {{
    font-size: 15px !important;
    color: {TEXTO} !important;
}}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# 2. MEMÓRIA
# ---------------------------------------------------------------
if "visor" not in st.session_state:
    st.session_state.visor = ""
if "historico" not in st.session_state:
    st.session_state.historico = []


# ---------------------------------------------------------------
# 3. LÓGICA
# ---------------------------------------------------------------
def apertar_tecla(tecla):
    visor = st.session_state.visor

    if visor == "Erro":  # depois de um erro, recomeça do zero
        visor = ""

    if tecla == "C":
        visor = ""

    elif tecla == "⌫":
        visor = visor[:-1]

    elif tecla == "=":
        if visor:
            try:
                conta = (
                    visor.replace(",", ".")
                    .replace("×", "*")
                    .replace("÷", "/")
                    .replace("−", "-")
                    .replace("%", "/100")
                )
                conta = re.sub(r"(?<![\d.])0+(?=\d)", "", conta)  # 007 -> 7
                resultado = eval(conta, {"__builtins__": {}}, {})
                if resultado == int(resultado):
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 10)
                texto_resultado = str(resultado).replace(".", ",")
                st.session_state.historico.append((visor, texto_resultado))
                st.session_state.historico = st.session_state.historico[-30:]
                visor = texto_resultado
            except Exception:
                visor = "Erro"

    elif tecla == "( )":
        visor += "(" if visor.count("(") == visor.count(")") else ")"

    else:
        visor += tecla

    st.session_state.visor = visor


def limpar_historico():
    st.session_state.historico = []


def botao(texto, chave, **kwargs):
    """Botão que ocupa toda a coluna (compatível com versões novas e antigas)."""
    try:
        st.button(texto, key=chave, width="stretch", **kwargs)
    except TypeError:
        st.button(texto, key=chave, use_container_width=True, **kwargs)


# ---------------------------------------------------------------
# 4. TELA
# ---------------------------------------------------------------
texto = st.session_state.visor or "0"
n = len(texto)
tamanho = 72 if n <= 8 else 54 if n <= 12 else 40 if n <= 18 else 30
st.markdown(
    f'<div class="visor" style="font-size:{tamanho}px">{texto}</div>',
    unsafe_allow_html=True,
)

# (texto da tecla, nome interno usado no CSS)
teclado = [
    [("C", "c"), ("⌫", "del"), ("%", "pct"), ("÷", "div")],
    [("7", "n7"), ("8", "n8"), ("9", "n9"), ("×", "mul")],
    [("4", "n4"), ("5", "n5"), ("6", "n6"), ("−", "sub")],
    [("1", "n1"), ("2", "n2"), ("3", "n3"), ("+", "add")],
    [("( )", "par"), ("0", "n0"), (",", "comma"), ("=", "eq")],
]

for linha in teclado:
    colunas = st.columns(4)
    for coluna, (tecla, nome) in zip(colunas, linha):
        with coluna:
            botao(tecla, f"btn_{nome}", on_click=apertar_tecla, args=(tecla,))

# ---------------------------------------------------------------
# 5. HISTÓRICO (campo separado, pode ser ocultado)
# ---------------------------------------------------------------
st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
    mostrar = st.toggle("Histórico", value=True, key="mostrar_hist")
with c2:
    st.toggle("Tema escuro", key="tema_escuro")

if mostrar:
    if st.session_state.historico:
        itens = "".join(
            f'<div class="hist-item">{conta} <b>= {res}</b></div>'
            for conta, res in reversed(st.session_state.historico[-15:])
        )
    else:
        itens = '<div class="hist-vazio">Nenhuma operação ainda</div>'
    st.markdown(
        f'<div class="hist-card"><div class="hist-titulo">Histórico</div>{itens}</div>',
        unsafe_allow_html=True,
    )
    if st.session_state.historico:
        botao("Limpar histórico", "limpar", on_click=limpar_historico)
