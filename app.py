import streamlit as st

# 1. CSS para arredondar os botões e ajustar o tamanho
st.markdown("""
    <style>
    div.stButton > button {
        border-radius: 50px;
        height: 65px;
        font-size: 24px;
        font-weight: bold;
    }
    /* Aumentar o tamanho do texto do visor */
    input {
        font-size: 40px !important;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Criando a "memória" para lembrar os números
if 'visor' not in st.session_state:
    st.session_state.visor = ""

# Visor da calculadora
st.text_input("", st.session_state.visor, disabled=True)

# 3. Lógica matemática de cada tecla
def apertar_tecla(tecla):
    if tecla == "C":
        st.session_state.visor = ""
    elif tecla == "⌫": # Apaga apenas o último caracter
        st.session_state.visor = st.session_state.visor[:-1]
    elif tecla == "=":
        try:
            # O Python calcula com pontos e asteriscos, por isso traduzimos os símbolos
            conta = st.session_state.visor.replace(",", ".").replace("×", "*").replace("÷", "/").replace("%", "/100")
            resultado = str(eval(conta))
            # Devolve a vírgula para o visor
            st.session_state.visor = resultado.replace(".", ",")
        except:
            st.session_state.visor = "Erro"
    elif tecla == "( )":
        # Conta se precisa de abrir ou fechar o parênteses
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
