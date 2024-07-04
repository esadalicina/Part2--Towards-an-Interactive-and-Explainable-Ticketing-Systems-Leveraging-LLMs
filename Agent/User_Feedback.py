import streamlit as st
import sys
import os

from matplotlib import pyplot as plt
from streamlit_autorefresh import st_autorefresh

# Add the directory containing the Resources module to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import Resources.data_access
from Resources.data_access import load_tickets


def user_feedback_page(ticket_support):

    st.header("User Feedback")
    # Load the tickets data
    chart_data = load_tickets()
    chart_data = chart_data.loc[chart_data['Assigned_to'] == ticket_support]
    chart_data = chart_data.loc[chart_data['Status'] == 'Closed']
    if not chart_data.empty:
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
            st.dataframe(chart_data[['id', "Ticket Title", "Description", 'Priority', "Feedback Smiley", "Feedback Text"]])
        else:
            s = chart_data[chart_data["Feedback Smiley"] == select]
            st.dataframe(s[['id', "Ticket Title", "Description", 'Priority', "Feedback Smiley","Feedback Text"]])


    else:
        st.write("No feedback found.")

    st_autorefresh(interval=5000, key="chatrefresh")





