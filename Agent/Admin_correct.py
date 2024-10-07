import time
import pandas as pd
import streamlit as st
from matplotlib import pyplot as plt
from streamlit_autorefresh import st_autorefresh

subcategories = {
            "Bank Account or Service": ["Checking or savings account", "Bank account or service"],
            "Loans": ["Consumer Loan", "Mortgage", "Payday loan, title loan, or personal loan", "Student loan",
                      "Vehicle loan or lease"],
            "Credit Cards and Prepaid Cards": ["Credit card", "Credit card or prepaid card"],
            "Credit Reporting and Debt Collection": ["Credit reporting",
                                                     "Credit reporting, credit repair services, or other personal consumer reports",
                                                     "Debt collection"],
            "Money Transfers and Financial Services": ["Money transfer, virtual currency, or money service",
                                                       "Money transfers", "Other financial service"]
        }

def remove_support(st, update_subcategory, subcategories, users):
    st.subheader('Remove Member')

    st.session_state.selected_category = st.selectbox("Category ", [""] + list(subcategories.keys()),
                                                      on_change=update_subcategory())

    # Display subcategories based on selected category
    if st.session_state.selected_category:
        st.session_state.selected_subcategory = st.selectbox(
            "Subcategory ", [""] + subcategories.get(st.session_state.selected_category, []),
            index=subcategories.get(st.session_state.selected_category, []).index(
                st.session_state.selected_subcategory) + 1 if st.session_state.selected_subcategory else 0
        )

    if st.session_state.selected_subcategory and st.session_state.selected_category:
        members = users[users['team'] == st.session_state.selected_subcategory]
        member_to_remove = st.selectbox('Select Member to Remove', members['name'])

    elif st.session_state.selected_category:
        members = users[users['category'] == st.session_state.selected_category]
        member_to_remove = st.selectbox('Select Member to Remove', members['name'])
    else:
        member_to_remove = st.selectbox('Select Member to Remove', [""] + list(users['name']))

    if member_to_remove:
        if st.button('Remove Member'):
            sc = st.success('Member removed successfully!', icon="✅")
            users = users[users['name'] != member_to_remove]
            users.to_csv('data/users.csv', index=False)

            st.session_state.selected_category = " "
            st.session_state.selected_subcategory = " "
            time.sleep(1)
            sc.empty()
            st.rerun()


def add_support(st, update_subcategory, subcategories, users):
    st.subheader('Add New Member')

    st.session_state.new_member_name = st.text_input('Name')

    if st.session_state.new_member_name:
        st.session_state.new_member_password = st.text_input('Password ', type='password')
        st.session_state.sele_category = st.selectbox("Choose Category", [""] + list(subcategories.keys()),
                                                      on_change=update_subcategory())
        if st.session_state.sele_category:
            st.session_state.sele_subcategory = st.selectbox(
                "Choose Subcategory", [""] + subcategories.get(st.session_state.sele_category, []),
                index=subcategories.get(st.session_state.sele_category, []).index(
                    st.session_state.sele_subcategory) + 1 if st.session_state.sele_subcategory else 0)

    if st.session_state.new_member_password and st.session_state.sele_subcategory:
        if st.button('Add Member'):
            # s = st.success('New member added successfully!', icon="✅")
            new_member_role = 'support'
            new_member_data = pd.DataFrame({
                "id": len(users["name"]) + 1,
                'name': [st.session_state.new_member_name],
                'password': [st.session_state.new_member_password],
                'category': [st.session_state.sele_category],
                'team': [st.session_state.sele_subcategory],
                'role': [new_member_role]
            })
            users = pd.concat([users, new_member_data], ignore_index=True)
            users.to_csv('data/users.csv', index=False)

            st.session_state.sele_subcategory = ""

            st.success('New member added successfully!', icon="✅")
            time.sleep(1)
            st.rerun()




def support_info(st, subcategories, update_subcategory, users):
    st.session_state.selected_category = st.selectbox("Category", [""] + list(subcategories.keys()),
                                                      on_change=update_subcategory())

    # Display subcategories based on selected category
    if st.session_state.selected_category:
        st.session_state.selected_subcategory = st.selectbox(
            "Subcategory", [""] + subcategories.get(st.session_state.selected_category, []),
            index=subcategories.get(st.session_state.selected_category, []).index(
                st.session_state.selected_subcategory) + 1 if st.session_state.selected_subcategory else 0
        )

    if st.session_state.selected_subcategory and st.session_state.selected_category:
        members = users[users['team'] == st.session_state.selected_subcategory]
        st.dataframe(members[["id", "name", "team", "category", "role"]], use_container_width=True)
    elif st.session_state.selected_category:
        members = users[users['category'] == st.session_state.selected_category]
        st.dataframe(members[["id", "name", "team", "category", "role"]], use_container_width=True)
    else:
        st.dataframe(users[["id", "name", "team", "category", "role"]], use_container_width=True)


def reclassify(st, subcategories, update_subcategory, tickets, reclassify_ticket, load_tickets):
    st.subheader('Reclassify Tickets')
    wrong_tickets = tickets[tickets['Status'] == 'Wrong Classification']
    st.dataframe(wrong_tickets[['id', 'Category', 'Subcategory','Tags','Ticket Title' ,'Description','Priority', 'Status']], use_container_width=True)

    ticket_id_to_reclassify = st.selectbox('Enter Ticket ID to Reclassify', wrong_tickets['id'])

    st.session_state.selected_category = ""
    st.session_state.selected_subcategory = ""

    if ticket_id_to_reclassify:
        st.session_state.selected_category = st.selectbox("Category  ", list(subcategories.keys()),
                                                          on_change=update_subcategory())

        # Display subcategories based on selected category
        if st.session_state.selected_category:
            st.session_state.selected_subcategory = st.selectbox(
                "Team  ", subcategories.get(st.session_state.selected_category, []),
                index=subcategories.get(st.session_state.selected_category, []).index(
                    st.session_state.selected_subcategory) + 1 if st.session_state.selected_subcategory else 0
            )

        if st.button('Reclassify Ticket'):
            reclassify_ticket(ticket_id_to_reclassify, st.session_state.selected_category,
                              st.session_state.selected_subcategory)
            load_tickets()
            ses = st.success(f'Ticket {ticket_id_to_reclassify} reclassified.', icon="✅")
            time.sleep(1)
            ses.empty()
            st.rerun()


def get_info(st, tickets):
    priority_filter = st.selectbox('Filter by priority', ['All', 'Low', 'Medium', 'High'])
    if priority_filter != 'All':
        team_tickets = tickets[tickets['Priority'] == priority_filter]

        solved_tickets = team_tickets[team_tickets['Status'] == 'Closed']
        unsolved_tickets = team_tickets[team_tickets['Status'] != 'Closed']

        st.subheader('Solved Tickets')
        st.dataframe(solved_tickets[['id', 'Category', 'Subcategory', 'Priority', 'Status', 'Assigned_to']],
                     use_container_width=True)

        st.subheader('Unsolved Tickets')
        st.dataframe(unsolved_tickets[['id', 'Category', 'Subcategory', 'Priority', 'Status', 'Assigned_to']],
                     use_container_width=True)
    else:
        solved_tickets = tickets[tickets['Status'] == 'Closed']
        unsolved_tickets = tickets[tickets['Status'] != 'Closed']

        st.subheader('Solved Tickets')
        st.dataframe(solved_tickets[['id', 'Category', 'Subcategory', 'Priority', 'Status', 'Assigned_to']],
                     use_container_width=True)

        st.subheader('Unsolved Tickets')
        st.dataframe(unsolved_tickets[['id', 'Category', 'Subcategory', 'Priority', 'Status', 'Assigned_to']],
                     use_container_width=True)


def conversation(st, save_message, users):
    st.header('Conversation with Team Members')
    member_to_message = st.selectbox('Select Member to Message', users['name'])
    message = st.text_area('Enter your message')
    if st.button('Send Message'):
        save_message(st.session_state.user, member_to_message, message)
        st.success(f'Message sent to {member_to_message}.')

def feedback_page(users, tickets):
    st.write("Client & Support Relation")

    user = st.selectbox("Select a Support Agent", [""]+list(users['name']))

    if user == "":
        chart_data = tickets
    else:
        # Load the tickets data
        chart_data = tickets.loc[tickets['Assigned_to'] == user]

    # Aggregate feedback data
    feedback_counts = chart_data['Feedback Smiley'].value_counts().reset_index()
    feedback_counts.columns = ['Feedback Smiley', 'Count']

    # Pie chart
    fig, ax = plt.subplots()
    colors = ['#ff9999', '#66b3ff', '#99ff99', '#ffcc99', '#c2c2f0']
    ax.pie(feedback_counts['Count'], labels=feedback_counts['Feedback Smiley'], autopct='%1.1f%%', colors=colors,
           startangle=90)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig)

    st.write(feedback_counts.set_index('Feedback Smiley'))

    select = st.selectbox("Select a Feedback Smiley", [" ", "😀", "🙂", "😐", "🙁", "😞"])
    if select == " ":
        st.dataframe(chart_data[['id', "Username", "Email", "Ticket Title", "Description", 'Priority', "Feedback Smiley", "Feedback Text"]], use_container_width=True)
    else:
        s = chart_data[chart_data["Feedback Smiley"] == select]
        st.dataframe(s[['id', "Ticket Title", "Description", 'Priority', "Feedback Smiley", "Feedback Text"]], use_container_width=True)
    st_autorefresh(interval=5000, key="chatrefresh")

