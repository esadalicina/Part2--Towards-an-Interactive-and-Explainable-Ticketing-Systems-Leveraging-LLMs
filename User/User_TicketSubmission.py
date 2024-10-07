from Classify import predict_lr, plot_shap_values
from datetime import datetime
import pandas as pd
import base64
import streamlit as st
import time
from Title_Gen import generate_title
from Tag_Gen import tags
import sys
import os

# Add the directory containing the Resources module to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Resources.data_access
from Resources.data_access import load_tickets, add_ticket


def get_ticket_solutions(category, df):

    if category:
        # Filter solutions based on category
        filtered_df = df[df["Category"] == category]
        return filtered_df[["Category", "Title", "Description"]].values.tolist()
    else:
        # Fetch random solutions
        return df[["Category", "Title", "Description"]].sample(n=5).values.tolist()


def knowledge_base(df):
    # Solution suggestions
    st.sidebar.header("Solution Suggestions")
    search_query = st.sidebar.text_input("Search Solutions")

    # Retrieve ticket solutions from the dataset based on selected category and description
    solutions = get_ticket_solutions(st.session_state.selected_category, df)

    if solutions:
        for Category, Title, Description in solutions:
            if search_query.lower() in Description.lower() or search_query.lower() in Title.lower() or search_query.lower() in Category.lower():
                title_partial = f"**{Title[:50]}**..." if len(Title) > 50 else f"**{Title}**"
                description_partial = Description[:100] + "..." if len(Description) > 100 else Description
                expander_title = f"{title_partial}"
                description_encoded = base64.b64encode(Description.encode()).decode()
                full_description_link = f"<a href='data:text/html;base64,{description_encoded}' target='_blank'>View Full Description</a>"
                with st.sidebar.expander(expander_title, expanded=False):
                    st.write(description_partial)
                    st.markdown(full_description_link, unsafe_allow_html=True)


def update_subcategory():
    st.session_state.selected_subcategory = ""


def ticket_submission(df):

    # Ticket submission form
    st.header("Ticket Submission")

    # Define category descriptions
    category_descriptions = {
        "Bank Account or Service": "Unauthorized account access, issues with account statements, problems with ATM/online banking services, and unresolved customer service inquiries.",
        "Credit Cards and Prepaid Cards": "Unauthorized charges, billing errors, prepaid card activation/balance issues, and fraudulent transactions.",
        "Money Transfers and Financial Services": "Delays in money transfers, incorrect recipient information, hidden fees, and poor customer service.",
        "Credit Reporting and Debt Collection": "Errors in credit reports, unfair debt collection practices, disputes related to debt amounts, and harassment by debt collectors.",
        "Loans": "Misrepresentation of loan terms, high interest rates, difficulties with loan repayment, and unfair penalties/fees."
    }

    subcategories = {
        "Bank Account or Service": ["Checking or savings account", "Bank account or service"],
        "Loans": ["Consumer Loan", "Mortgage", "Payday loan, title loan, or personal loan", "Student loan", "Vehicle loan or lease"],
        "Credit Cards and Prepaid Cards": ["Credit card", "Credit card or prepaid card"],
        "Credit Reporting and Debt Collection": ["Credit reporting", "Credit reporting, credit repair services, or other personal consumer reports", "Debt collection"],
        "Money Transfers and Financial Services": ["Money transfer, virtual currency, or money service", "Money transfers", "Other financial service"]
    }

    # Initialize session state for selected_category
    if "selected_category" not in st.session_state:
        st.session_state.selected_category = None
    if "selected_subcategory" not in st.session_state:
        st.session_state.selected_subcategory = None
    if "description" not in st.session_state:
        st.session_state.description = None
    if "submission_successful" not in st.session_state:
        st.session_state.submission_successful = False
    if "show_success_message" not in st.session_state:
        st.session_state.show_success_message = False
    if "last_submission_time" not in st.session_state:
        st.session_state.last_submission_time = 0
    if "title" not in st.session_state:
        st.session_state.title = None
    if "tags" not in st.session_state:
        st.session_state.tags = None


    st.session_state.description = st.text_area("Provide a detailed description of your complaint and what you already have done to solve it!", value=st.session_state.description, height=200,
                                                placeholder="e.x 'I am having trouble logging into my bank account. I have tried multiple times and "
                                                            "I have received no response. I tried resetting my password, but that did not seem to work either. "
                                                            "I am concerned that there may be an issue with my account security or that someone "
                                                            "has accessed my account without my permission.")

    priority = st.selectbox("Priority", ["Low", "Medium", "High"])

    explainable = False
    if st.session_state.description is not None:
        if len(st.session_state.description) < 50 and st.session_state.description != "":
            sss = st.warning(f"🚨 The description is too short. Minimum length is 50 characters.")
            time.sleep(3)
            sss.empty()

        elif len(st.session_state.description) > 50:
            st.session_state.title = generate_title(st.session_state.description)
            option = " "
            predicted_category = ""
            if st.session_state.description:
                st.header("Predicted Category")
                predicted_category, label, prob = predict_lr([st.session_state.description])
                st.write(f"Your Ticket is classified in the following category: **{predicted_category}**")
                explainable = st.radio("Do you want to check the explanation of the systems decision?", options=["No", "Yes"])

                if explainable == "Yes":
                    st.write("Tha diagram shows which words from your description had a positive impact on the decision.")
                    plot_shap_values([st.session_state.description], class_index=label)

                option = st.radio("Do you trust our system or do you want to change the category?", options=[predicted_category, "Others"])

            if option == predicted_category:
                update_subcategory()
                st.session_state.selected_category = predicted_category
                # Display subcategories based on selected category
                if st.session_state.selected_category:
                    st.session_state.selected_subcategory = st.selectbox(
                        "Subcategory", [""] + subcategories.get(st.session_state.selected_category, []),
                        index=subcategories.get(st.session_state.selected_category, []).index(
                            st.session_state.selected_subcategory) + 1 if st.session_state.selected_subcategory else 0
                    )

            if option == "Others":
                st.session_state.selected_category = ""
                st.session_state.selected_subcategory = ""
                # Display category descriptions when hovering over category
                st.session_state.selected_category = st.selectbox("Category", [""] + list(category_descriptions.keys()),
                                                                  index=list(category_descriptions.keys()).index(
                                                                      st.session_state.selected_category) + 1 if st.session_state.selected_category else 0,
                                                                  on_change=update_subcategory()
                                                                  )

                # Display category description based on selected category
                category_description = category_descriptions.get(st.session_state.selected_category, "")
                st.write(f"<small>{category_description}</small>", unsafe_allow_html=True)

                # Display subcategories based on selected category
                if st.session_state.selected_category:
                    st.session_state.selected_subcategory = st.selectbox(
                        "Subcategory", [""] + subcategories.get(st.session_state.selected_category, []),
                        index=subcategories.get(st.session_state.selected_category, []).index(
                            st.session_state.selected_subcategory) + 1 if st.session_state.selected_subcategory else 0
                    )


    # Conditionally set CSS style to disable the submit button
    button_disabled = not (st.session_state.selected_category and st.session_state.description and st.session_state.selected_subcategory)

    if button_disabled:
        st.button("Submit", key="submit1", disabled=True)
    else:
        if st.button("Submit", key="submit2"):
            st.session_state.tags = tags(st.session_state.description)
            new_ticket = {
                "id": len(load_tickets()) + 1,
                "Username": st.session_state.username,
                "Email": st.session_state.email,
                "Category": st.session_state.selected_category,
                "Subcategory": st.session_state.selected_subcategory,
                "Ticket Title": st.session_state.title,
                "Description": st.session_state.description,
                "Priority": priority,
                "Status": "Submitted",
                "Submission Time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Assigned_to": "",
                "Feedback Smiley": "",
                "Feedback Text": "",
                "Tags": st.session_state.tags
            }

            new_ticket_df = pd.DataFrame([new_ticket])
            if 'tickets' not in st.session_state:
                st.session_state.tickets = new_ticket_df
            else:
                st.session_state.tickets = pd.concat([st.session_state.tickets, new_ticket_df], ignore_index=True)

            add_ticket(new_ticket)
            st.session_state.selected_category = ""
            st.session_state.selected_subcategory = ""
            st.session_state.description = ""
            st.session_state.submission_successful = True
            st.session_state.last_submission_time = time.time()
            st.session_state.show_success_message = True
            st.rerun()


    # Show knowledge base
    knowledge_base(df)


    # Display success message and reset form after delay
    if st.session_state.show_success_message:
        suc = st.success("Ticket submitted successfully!", icon="✅")
        time.sleep(3)
        st.session_state.show_success_message = False
        suc.empty()
        st.rerun()


