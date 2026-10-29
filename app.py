# 1. CSS atualizado para bloquear o empilhamento no telemóvel
st.markdown("""
    <style>
    /* Força as colunas a ficarem lado a lado */
    div[data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 0 !important;
    }
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: nowrap !important;
        gap: 5px !important;
    }
    
    /* Visual dos botões arredondados */
    div.stButton > button {
        border-radius: 50px;
        height: 65px;
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Texto grande no visor */
    input {
        font-size: 40px !important;
        text-align: right;
    }
    </style>
""", unsafe_allow_html=True)
