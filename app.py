import streamlit as st

# 1. CSS com regras específicas para bloquear a proteção de telemóvel do Streamlit
st.markdown("""
    <style>
    /* Limita a largura total para imitar o formato do telemóvel e centraliza */
    .block-container {
        max-width: 400px !important;
        padding-top: 2rem !important;
        padding-left: 15px !important;
        padding-right: 15px !important;
        margin: 0 auto !important;
    }

    /* O SEGREDO: Desliga a quebra automática do Streamlit em ecrãs pequenos */
    @media (max-width: 768px) {
        div[data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            gap: 8px !important;
        }
        div[data-testid="column"] {
            width: 25% !important;
            flex: 1 1 25% !important;
            min-width: 0 !important;
        }
    }

    /* Visual das teclas arredondadas */
    div.stButton > button {
        border-radius: 50px !important;
        height: 70px !important;
        font-size: 24px !important;
        font-weight: 500 !important;
        width: 100% !important;
        padding: 0 !important;
        margin: 0 !important;
    }

    /* Ajuste do visor para caber os números na perfeição */
    input {
        font-size: 45px !important;
        text-align: right !important;
        border-radius: 20px !important;
        height: 80px !important;
    }
    div[data-baseweb="input"] {
        height: 80px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Criando a "memória" para lembrar os números
if 'visor' not in st.session_state:
    st.session_state.visor = ""

# Visor da calculadora
st.text_input("Visor", st.session_state.visor, disabled=True, label_visibility="collapsed")

# 3. Lógica matemática
def apertar_tecla(tecla):
    if tecla == "C":
        st.session_state.visor = ""
    elif tecla == "⌫": 
        st.session_state.visor = st.session_state.visor[:-1]
    elif tecla == "=":
        try:
            conta = st.session_state.visor.replace(",", ".").replace("×", "*").replace("÷", "/").replace("%", "/100")
            # Calcula e remove casas decimais desnecessárias (ex: 4.0 vira 4)
            resultado = eval(conta)
            if resultado == int(resultado):
                resultado = int(resultado)
            st.session_state.visor = str(resultado).replace(".", ",")
        except:
            st.session_state.visor = "Erro"
    elif tecla == "( )":
        abertos = st.session_state.visor.count("(")
        fechados = st.session_state.visor.count(")")
        if abertos == fechados:
            st.session_state.visor += "("
        else:
            st.session_state.visor += ")"
    else:
        st.session_state.visor += str(tecla)

# 4. Grelha de botões
botoes = [
    ["C", "⌫", "%", "÷"],
    ["7", "8", "9", "×"],
    ["4", "5", "6", "-"],
    ["1", "2", "3", "+"],
    ["( )", "0", ",", "="]
]

for linha in botoes:
    colunas = st.columns(4)
    for i, tecla in enumerate(linha):
        colunas[i].button(tecla, use_container_width=True, on_click=apertar_tecla, args=(tecla,))
