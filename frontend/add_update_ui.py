import streamlit as st
from datetime import datetime
import requests

API_URL = "http://127.0.0.1:8000/"
response = requests.get(f"{API_URL}/expense/date")
data = response.json()
latest_expense_date = data[0]['last_expense_date']

def add_update_tab():
    # Use a placeholder date until the user selects one
    selected_date = st.date_input("Enter Date", latest_expense_date, label_visibility="collapsed")

    # Fetch expenses dynamically when the date changes
    if "selected_date" not in st.session_state or st.session_state.selected_date != selected_date:
        response = requests.get(f"{API_URL}/expenses/{selected_date}")
        if response.status_code == 200:
            st.session_state.expenses = response.json()
            st.session_state.selected_date = selected_date
        else:
            st.error("Failed to retrieve expenses")
            st.session_state.expenses = []

    categories = ["Rent", "Food", "Shopping", "Entertainment", "Other"]

    # Display message if no expenses are recorded for the selected date
    if not st.session_state.expenses:
        st.info(f"No expenses recorded for {selected_date}. Click on Add/Update Expense button to enter expense.")

    # Button to add a new empty expense row
    if st.button("Add/Update Expense"):
        st.session_state.expenses.append({'id': None, 'amount': 0.0, 'category': "Shopping", 'notes': ""})

    with st.form(key="expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.text("Amount")
        with col2:
            st.text("Category")
        with col3:
            st.text("Notes")

        updated_expenses = []
        for i, expense in enumerate(st.session_state.expenses):
            col1, col2, col3 = st.columns(3)
            with col1:
                amount_input = st.number_input(
                    label=f"Amount {i}",
                    min_value=0.0,
                    step=1.0,
                    value=expense.get('amount', 0.0),
                    key=f"amount_{i}",
                    label_visibility="collapsed"
                )
            with col2:
                category_input = st.selectbox(
                    label=f"Category {i}",
                    options=categories,
                    index=categories.index(expense.get('category', "Shopping")),
                    key=f"category_{i}",
                    label_visibility="collapsed"
                )
            with col3:
                notes_input = st.text_input(
                    label=f"Notes {i}",
                    value=expense.get('notes', ""),
                    key=f"notes_{i}",
                    label_visibility="collapsed"
                )

            updated_expenses.append({
                'id': expense.get('id'),  # Include ID for existing records
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })

        submit_button = st.form_submit_button("Submit")
        if submit_button:
            # Filter out rows with zero amount
            filtered_expenses = [expense for expense in updated_expenses if expense['amount'] > 0]

            post_response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if post_response.status_code == 200:
                st.success("Expenses updated successfully")
                # Refresh the expense list to reflect the updates
                refreshed_response = requests.get(f"{API_URL}/expenses/{selected_date}")
                if refreshed_response.status_code == 200:
                    st.session_state.expenses = refreshed_response.json()
                else:
                    st.error("Failed to refresh expenses.")
            else:
                st.error("Failed to update expenses.")


if __name__ == "__main__":
    add_update_tab()
