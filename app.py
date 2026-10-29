import streamlit as st

st.set_page_config(page_title="Calculadora", page_icon="🧮", layout="centered")

# ---------------------------------------------------------------
# 1. VISUAL (CSS)
# ---------------------------------------------------------------
st.markdown("""
<style>
/* Fundo geral (força o tema claro mesmo se o celular estiver no escuro) */
.stApp, [data-testid="stAppViewContainer"] {
    background: #e4e3de !important;
}
header[data-testid="stHeader"] { background: transparent !important; }

/* Largura de celular, centralizado */
.block-container {
    max-width: 420px !important;
    padding: 1.2rem 16px 2rem 16px !important;
    margin: 0 auto !important;
}

/* Espaço entre as linhas de botões */
div[data-testid="stVerticalBlock"] { gap: 0.7rem !important; }

/* Mantém as 4 colunas lado a lado no celular */
div[data-testid="stHorizontalBlock"] {
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    gap: 12px !important;
}
div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"],
div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
    width: auto !important;
    flex: 1 1 0 !important;
    min-width: 0 !important;
}

/* Visor */
.visor {
    min-height: 200px;
    display: flex;
    align-items: flex-end;
    justify-content: flex-end;
    text-align: right;
    word-break: break-all;
    padding: 0 8px 18px 8px;
    color: #2f2f2f;
    font-family: "Source Sans Pro", sans-serif;
    font-weight: 300;
    line-height: 1.1;
}

/* Teclas redondas */
div.stButton > button {
    width: 100% !important;
    height: auto !important;
    min-height: 0 !important;
    aspect-ratio: 1 / 1;
    border-radius: 50% !important;
    border: none !important;
    padding: 0 !important;
    background: linear-gradient(145deg, #ebe5d8, #dcd8c9) !important;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.10) !important;
    transition: transform 0.05s ease;
}
div.stButton > button p {
    font-size: 30px !important;
    font-weight: 400 !important;
    margin: 0 !important;
    color: #2f2f2f !important;
}
div.stButton > button:hover,
div.stButton > button:focus,
div.stButton > button:focus:not(:active) {
    border: none !important;
    box-shadow: 0 6px 10px rgba(0, 0, 0, 0.14) !important;
}
div.stButton > button:active {
    transform: scale(0.94);
    background: linear-gradient(145deg, #dcd8c9, #d2cdbc) !important;
}

/* Operadores em azul */
.st-key-btn_pct button p, .st-key-btn_div button p,
.st-key-btn_mul button p, .st-key-btn_sub button p,
.st-key-btn_add button p, .st-key-btn_del button p {
    color: #4b5a94 !important;
}
.st-key-btn_div button p, .st-key-btn_mul button p,
.st-key-btn_sub button p, .st-key-btn_add button p {
    font-size: 36px !important;
}

/* C em vermelho */
.st-key-btn_c button p { color: #d1401f !important; }

/* Igual: azul preenchido */
.st-key-btn_eq button {
    background: #4b5a94 !important;
    box-shadow: 0 8px 14px rgba(75, 90, 148, 0.35) !important;
}
.st-key-btn_eq button p {
    color: #ffffff !important;
    font-size: 40px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------
# 2. MEMÓRIA DO VISOR
# ---------------------------------------------------------------
if "visor" not in st.session_state:
    st.session_state.visor = ""


# ---------------------------------------------------------------
# 3. LÓGICA
# ---------------------------------------------------------------
def apertar_tecla(tecla):
    visor = st.session_state.visor

    # Depois de um erro, qualquer tecla começa do zero
    if visor == "Erro":
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
                # eval sem acesso a funções do Python (só aceita matemática)
                resultado = eval(conta, {"__builtins__": {}}, {})
                if resultado == int(resultado):
                    resultado = int(resultado)
                else:
                    resultado = round(resultado, 10)
                visor = str(resultado).replace(".", ",")
            except Exception:
                visor = "Erro"

    elif tecla == "( )":
        if visor.count("(") == visor.count(")"):
            visor += "("
        else:
            visor += ")"

    else:
        visor += tecla

    st.session_state.visor = visor


# ---------------------------------------------------------------
# 4. TELA
# ---------------------------------------------------------------
texto = st.session_state.visor or "0"
n = len(texto)
if n <= 8:
    tamanho = 72
elif n <= 12:
    tamanho = 54
elif n <= 18:
    tamanho = 40
else:
    tamanho = 30

st.markdown(
    f'<div class="visor" style="font-size:{tamanho}px">{texto}</div>',
    unsafe_allow_html=True,
)

# (texto da tecla, nome interno usado pelo CSS)
botoes = [
    [("C", "c"), ("⌫", "del"), ("%", "pct"), ("÷", "div")],
    [("7", "n7"), ("8", "n8"), ("9", "n9"), ("×", "mul")],
    [("4", "n4"), ("5", "n5"), ("6", "n6"), ("−", "sub")],
    [("1", "n1"), ("2", "n2"), ("3", "n3"), ("+", "add")],
    [("( )", "par"), ("0", "n0"), (",", "comma"), ("=", "eq")],
]

for linha in botoes:
    colunas = st.columns(4)
    for coluna, (tecla, nome) in zip(colunas, linha):
        with coluna:
            st.button(tecla, key=f"btn_{nome}", on_click=apertar_tecla, args=(tecla,))
