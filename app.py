import streamlit as st

st.title("Calculadora")

# 1. Criando a "memória" para lembrar os números digitados no visor
if 'visor' not in st.session_state:
    st.session_state.visor = ""

# 2. Desenhando a tela do visor
st.text_input("", st.session_state.visor, disabled=True)

# Função que decide o que acontece ao apertar cada tecla
def apertar_tecla(tecla):
    if tecla == "C":
        st.session_state.visor = ""
    elif tecla == "=":
        try:
            # O comando eval faz a conta matemática do texto (ex: "2+2" vira 4)
            st.session_state.visor = str(eval(st.session_state.visor))
        except:
            st.session_state.visor = "Erro"
    else:
        st.session_state.visor += str(tecla)

# 3. Construindo as fileiras de botões (4 colunas para manter o layout alinhado)
linha1 = st.columns(4)
linha1[0].button("7", use_container_width=True, on_click=apertar_tecla, args=("7",))
linha1[1].button("8", use_container_width=True, on_click=apertar_tecla, args=("8",))
linha1[2].button("9", use_container_width=True, on_click=apertar_tecla, args=("9",))
linha1[3].button("/", use_container_width=True, on_click=apertar_tecla, args=("/",))

linha2 = st.columns(4)
linha2[0].button("4", use_container_width=True, on_click=apertar_tecla, args=("4",))
linha2[1].button("5", use_container_width=True, on_click=apertar_tecla, args=("5",))
linha2[2].button("6", use_container_width=True, on_click=apertar_tecla, args=("6",))
linha2[3].button("*", use_container_width=True, on_click=apertar_tecla, args=("*",))

linha3 = st.columns(4)
linha3[0].button("1", use_container_width=True, on_click=apertar_tecla, args=("1",))
linha3[1].button("2", use_container_width=True, on_click=apertar_tecla, args=("2",))
linha3[2].button("3", use_container_width=True, on_click=apertar_tecla, args=("3",))
linha3[3].button("-", use_container_width=True, on_click=apertar_tecla, args=("-",))

linha4 = st.columns(4)
linha4[0].button("C", use_container_width=True, on_click=apertar_tecla, args=("C",))
linha4[1].button("0", use_container_width=True, on_click=apertar_tecla, args=("0",))
linha4[2].button("=", use_container_width=True, on_click=apertar_tecla, args=("=",))
linha4[3].button("+", use_container_width=True, on_click=apertar_tecla, args=("+",))
