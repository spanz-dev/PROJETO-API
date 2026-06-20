import streamlit as st
import requests
from requests import post
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu

if "logado" not in st.session_state:
    st.session_state.logado = False

load_dotenv()

st.markdown('''

    <style>
    div.stButton > button {
    
    background-color: #41D0F2;
    
    </style>
    

''', unsafe_allow_html=True)

API_URL = os.getenv("API_URL" , "http://127.0.0.1:8000")

st.set_page_config(page_title="SpanzFlix" , layout="centered")
st.title("Filmes e Series - Spanzflix☁️")

with st.sidebar:
    choose = st.selectbox("Escolha: " , ["Login" , "Registro"])
    if choose == "Registro":
        st.title("Seja bem vindo,Faça seu cadastro ja!!!")
        nome = st.text_input("Insira seu nome completo: ")
        email = st.text_input("Insira seu E-mail: ")
        senha = st.text_input("Insira sua senha: " , type="password")
        if st.button("Cadastrar-se"):
                payload = {"nome": nome , "email": email , "senha": senha}
                res = requests.post(f"{API_URL}/registro" , json=payload)
                if res.status_code == 200:
                    st.success("Cadrastro Realizado!!")
                else:
                    st.error("nao foi possivel concluir o cadastro")
    else:
        st.title("Faça seu login ja!!!")
        email = st.text_input("Insira seu E-mail: ")
        senha = st.text_input("Insira sua senha: " , type="password")
        if st.button("Logar"):
            payload = {"email": email , "senha": senha}
            res = requests.post(f"{API_URL}/login" , json=payload)
            if res.status_code == 200:
                st.success("Voce logou em sua conta!")
                st.session_state.logado = True
                st.rerun()
            else:
                st.error("nao foi possivel concluir o login")


if st.session_state.logado:
    pagina = option_menu(
        menu_title=None,
        options=["Home", "Dashboard", "Usuários", "Configurações"],
        icons=["house", "bar-chart", "people", "gear"],
        orientation="horizontal",
    )

    if pagina == "Home":
        st.title("Home")

    elif pagina == "Dashboard":
        st.title("Dashboard")

    elif pagina == "Usuários":
        st.title("Usuários")

    elif pagina == "Configurações":
        st.title("Configurações")