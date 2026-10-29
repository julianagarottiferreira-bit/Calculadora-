# Esse comando chama o Streamlit (o "mestre de obras" que desenha a tela)
import streamlit as st

# Coloca um título no topo do seu aplicativo
st.title("Minha Primeira Calculadora")

# ENTRADA DE DADOS: Criando as caixas para o usuário digitar
numero1 = st.number_input("Digite o primeiro número:")
numero2 = st.number_input("Digite o segundo número:")

# MENU: Criando uma lista para escolher a operação matemática
operacao = st.selectbox("Escolha a operação:", ["Somar", "Subtrair", "Multiplicar", "Dividir"])

# PROCESSAMENTO: O botão que faz a mágica acontecer
if st.button("Calcular"):
    
    # A Lógica: "SE (if) a operação escolhida for Somar, faça isso..."
    if operacao == "Somar":
        resultado = numero1 + numero2
        
    elif operacao == "Subtrair":
        resultado = numero1 - numero2
        
    elif operacao == "Multiplicar":
        resultado = numero1 * numero2
        
    elif operacao == "Dividir":
        resultado = numero1 / numero2

    # SAÍDA: Mostrando o resultado final em uma caixa verde na tela
    st.success(f"O resultado é: {resultado}")
