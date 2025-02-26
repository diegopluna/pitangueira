import streamlit as st
import paid_transactions
import home


def main():
    st.set_page_config(
        page_title="Sistema de Gerenciamento de Transações",
        page_icon="💰",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.sidebar.title("Navegação")
    page = st.sidebar.radio(
        "Selecione uma página:",
        ["Início", "Transações Pagas"],  # Add the new page option
        index=0
    )

    if page == "Transações Pagas":
        paid_transactions.show()
    elif page == "Início":
        home.show()
    else:
        st.error("Página não encontrada")


if __name__ == "__main__":
    main()
