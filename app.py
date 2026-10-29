import streamlit as st

# 1. CSS atualizado e otimizado para o ecrã do telemóvel
st.markdown("""
    <style>
    /* Esconde as margens laterais exageradas do Streamlit no telemóvel */
    .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        padding-top: 2rem !important;
        max-width: 100% !important;
    }

    /* Ajusta o bloco principal para não transbordar e manter as teclas na mesma linha */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 8px !important;
        width: 100% !important;
        padding: 0px !important;
    }
    
    /* Força exatamente as 4 colunas a caberem no ecrã (compensando os espaços) */
    div[data-testid="column"] {
        width: 22% !important;
        flex: 1 1 22% !important;
        min-width: 0 !important;
    }
    
    /* Visual dos botões redondos e perfeitamente centrados */
    div.stButton > button {
        border-radius: 50px;
        height: 70px;
        width: 100%;
        font-size: 24px;
        font-weight: bold;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Texto grande no visor */
    input {
        font-size: 45px !important;
        text-align: right;
        border-radius: 15px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Criando a "memória" para lembrar os números
if 'visor' not in st.session_state:
    st.session_state.visor = ""

# Visor da calculadora (com a etiqueta oculta para ficar mais limpo)
st.text_input("Visor", st.session_state.visor, disabled=True, label_visibility="collapsed")

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
