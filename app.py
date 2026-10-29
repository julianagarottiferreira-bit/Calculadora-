import streamlit as st

# 1. CSS agressivo para forçar a grelha de 4 colunas e corrigir o visor cortado
st.markdown("""
    <style>
    /* Remove margens gerais do ecrã */
    .block-container {
        padding: 1rem !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
    }

    /* Força as linhas a comportarem-se como uma grelha horizontal, sem empilhar */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2% !important; /* Espaçamento mínimo */
        width: 100% !important;
        padding: 0 !important;
    }
    
    /* Força as 4 colunas a dividirem o ecrã em partes exatamente iguais */
    div[data-testid="column"] {
        width: 23% !important;
        flex: 1 1 0px !important; 
        min-width: 0 !important;
        padding: 0 !important;
    }
    
    /* Ajusta os botões para ficarem proporcionais */
    div.stButton > button {
        border-radius: 15px !important; /* Ligeiramente arredondados */
        height: 70px !important;
        width: 100% !important;
        font-size: 22px !important;
        font-weight: bold !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Aumenta a altura da caixa do visor para os números não ficarem cortados */
    div[data-baseweb="input"] {
        height: 80px !important;
    }
    input {
        font-size: 40px !important;
        height: 80px !important;
        text-align: right !important;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Criando a "memória" para lembrar os números
if 'visor' not in st.session_state:
    st.session_state.visor = ""

# Visor da calculadora
st.text_input("Visor", st.session_state.visor, disabled=True, label_visibility="collapsed")

# 3. Lógica matemática de cada tecla
def apertar_tecla(tecla):
    if tecla == "C":
        st.session_state.visor = ""
    elif tecla == "⌫": 
        st.session_state.visor = st.session_state.visor[:-1]
    elif tecla == "=":
        try:
            conta = st.session_state.visor.replace(",", ".").replace("×", "*").replace("÷", "/").replace("%", "/100")
            resultado = str(eval(conta))
            st.session_state.visor = resultado.replace(".", ",")
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

# 4. Construindo a grelha exata de 5 linhas e 4 colunas
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
