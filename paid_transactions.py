import streamlit as st
from db import query_database_to_dataframe

def show():
    st.title("Compras não entregues")
    st.write("Esta página exibe todas as transações com status PAGO.")

    with st.spinner('Carregando dados...'):
        # Get data from database
        _, joined_data_df = query_database_to_dataframe()

    if joined_data_df is not None:
        paid_transactions = joined_data_df[joined_data_df["Status da Transação"] == "PAID"]
        st.subheader(f"Total de transações pagas: {len(paid_transactions)}")
        search_term = st.text_input("Pesquisar por nome, email ou telefone")

        if search_term:
            filtered_df = paid_transactions[
                paid_transactions["Nome Completo"].str.contains(search_term, case=False, na=False) |
                paid_transactions["Email"].str.contains(search_term, case=False, na=False) |
                paid_transactions["Telefone"].str.contains(search_term, case=False, na=False)
            ]
            st.dataframe(filtered_df, use_container_width=True)
        else:
            # Display the dataframe
            st.dataframe(paid_transactions, use_container_width=True)

        if not paid_transactions.empty:
            csv = paid_transactions.to_csv(index=False).encode('utf-8')
            st.download_button(
                "Exportar para CSV",
                csv,
                "transacoes_pagas.csv",
                "text/csv",
                key='download-csv'
            )

            # Show summary statistics
            # st.subheader("Resumo Financeiro")

            # total_frevos = paid_transactions["Quantidade de Frevos"].sum()
            # avg_transaction = paid_transactions["Quantidade de Frevos"].mean()

            # col1, col2 = st.columns(2)
            # with col1:
            #     st.metric("Total de Frevos Vendidos", f"{total_frevos:,.2f}")
            # with col2:
            #     st.metric("Média por Transação", f"{avg_transaction:,.2f}")
    else:
        st.error("Não foi possível carregar os dados. Por favor, verifique a conexão com o banco de dados.")
