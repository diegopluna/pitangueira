import streamlit as st
import pandas as pd
import plotly.express as px
from db import query_database_to_dataframe


def filter_and_clean_dataframe():
    try:
        transactions_df, _ = query_database_to_dataframe()
        if transactions_df is None:
            return None
        filtered_transactions_df = transactions_df[
            (transactions_df["type"] == "COIN_PURCHASE")
            & (transactions_df["transaction_status"].isin(["PAID", "DELIVERED"]))
        ]

        # Drop specified columns
        columns_to_drop = [
            "customer_name",
            "customer_cpf",
            "payment_link",
            "order_code",
            "document_id",
            "total_value",
            "updated_by_id",
        ]
        filtered_transactions_df = filtered_transactions_df.drop(
            columns=columns_to_drop, errors="ignore"
        )



        return filtered_transactions_df
    except KeyError as e:
        print(f"Error: Column not found in DataFrame: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def show():
    transactions_df = filter_and_clean_dataframe()

    if transactions_df is None:
        st.error("An unexpected error occurred. Please check the logs.")
        return

    transactions_df["created_at"] = pd.to_datetime(transactions_df["created_at"])
    transactions_df["date"] = transactions_df["created_at"].dt.date

    st.title("Transaction Data Dashboard")

    date_range = st.sidebar.date_input(
        "Select Date Range", [transactions_df["date"].min(), transactions_df["date"].max()]
    )
    # filtered_df = transactions_df[
    #     (transactions_df["date"] >=  date_range[0]) & (transactions_df["date"] <=  date_range[1])
    # ]

    daily_quantity = (
        transactions_df.groupby("date")["quantity_coin"].sum().reset_index()
    )

    st.subheader("Total Quantity Coin per Day")
    fig = px.bar(
        daily_quantity,
        x="date",
        y="quantity_coin",
        title="Total Quantity Coin per Day",
        labels={"date": "Date", "quantity_coin": "Total Quantity Coin"},
        color_discrete_sequence=["#636EFA"],
        hover_data={"quantity_coin": True, "date": False},
    )
    fig.update_layout(
        xaxis_tickangle=-45,
        xaxis_title=None,
        yaxis_title="Total Quantity Coin",
    )
    fig.update_xaxes(tickangle=-45, tickmode="linear", dtick="D")
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Additional Insights")

    st.subheader("Transaction Status Distribution")
    status_counts = (
        transactions_df["transaction_status"].value_counts().reset_index()
    )
    status_counts.columns = ["transaction_status", "count"]
    fig_pie = px.pie(
        status_counts,
        names="transaction_status",
        values="count",
        title="Transaction Status Breakdown",
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    daily_quantity["cumulative_quantity"] = daily_quantity[
        "quantity_coin"
    ].cumsum()
    st.subheader("Cumulative Quantity Coin Over Time")
    fig_line = px.line(
        daily_quantity,
        x="date",
        y="cumulative_quantity",
        title="Cumulative Quantity Coin Over Time",
        labels={
            "date": "Date",
            "cumulative_quantity": "Cumulative Quantity Coin",
        },
    )
    st.plotly_chart(fig_line, use_container_width=True)

    st.subheader("Filtered Transactions")
    st.dataframe(
        transactions_df.style.format({"created_at": "{: %Y-%m-%d %H:%M:%S}"})
    )
