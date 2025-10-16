import streamlit as st
import mysql.connector
from datetime import datetime



def show():

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Abbivimi@7",
        database="user_management"
    )
    cursor = conn.cursor(dictionary=True)

    st.markdown(
        """
        <style>
             .block-container {
            max-width: 95% !important;
            padding-top: 2rem !important;     /* Reduce top padding */
            padding-bottom: 1rem !important;  /* Reduce bottom padding */
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
            
            .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .logout-btn {
                background-color: #FF4B4B;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
            }
            .logout-btn:hover {
                background-color: #e04343;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.title("Client Dashboard")

    col1, col2 = st.columns([8, 2])
    with col1:
        st.header("Queries")
    with col2:
        if st.button("Logout", key="logout_btn"):
            st.session_state.clear()
            st.success("Logged out successfully!")
            st.stop()

    if "show_form" not in st.session_state:
        st.session_state.show_form = False

    cursor.execute("SELECT * FROM client_queries ORDER BY query_created_time DESC")
    queries = cursor.fetchall()

    col_left, col_right = st.columns(2)

    with col_left:
        top_left, top_right = st.columns([6, 2])
        with top_left:
            st.markdown("#### Closed Queries")
        with top_right:
            if st.button("Create New Query", key="create_query"):
                st.session_state.show_form = not st.session_state.show_form

        if st.session_state.show_form:
            st.subheader("Submit New Query")
            with st.form("new_query_form"):
                email = st.text_input("Email ID")
                mobile = st.text_input("Mobile Number")
                heading = st.text_input("Query Heading")
                description = st.text_area("Query Description")
                submitted = st.form_submit_button("Submit Query")

                if submitted:
                    cursor.execute(
                        """
                        INSERT INTO client_queries 
                        (mail_id, mobile_number, query_heading, query_description, status, query_created_time, query_closed_time) 
                        VALUES (%s, %s, %s, %s, 'Open', %s, NULL)
                        """,
                        (email, mobile, heading, description, datetime.now())
                    )
                    conn.commit()
                    st.success(" Query submitted successfully!")
                    st.session_state.show_form = False

        closed_queries = [q for q in queries if q["status"] == "Closed"]
        if not closed_queries:
            st.info("No closed queries")
        else:
            for q in closed_queries:
                with st.expander(f"{q['query_heading']}"):
                    st.markdown(f" Description: {q['query_description']}")
                    st.markdown(f" Email: {q['mail_id']}")
                    st.markdown(f" Mobile: {q['mobile_number']}")
                    st.markdown(f" Status: {q['status']}")
                    st.markdown(f" Created At: {q['query_created_time']}")
                    if q['query_closed_time']:
                        st.markdown(f" Closed At: {q['query_closed_time']}")
                    if q.get('answer'):
                        st.markdown(f" Answer: {q['answer']}")

    with col_right:
        st.markdown("#### Open Queries")
        open_queries = [q for q in queries if q["status"] == "Open"]
        if not open_queries:
            st.info("No open queries")
        else:
            for q in open_queries:
                with st.expander(f" {q['query_heading']}"):
                    st.markdown(f" Description: {q['query_description']}")
                    st.markdown(f" Email: {q['mail_id']}")
                    st.markdown(f" Mobile: {q['mobile_number']}")
                    st.markdown(f" Status: {q['status']}")
                    st.markdown(f" Created At: {q['query_created_time']}")
                    if q.get('answer'):
                        st.markdown(f" Answer: {q['answer']}")

    cursor.close()
    conn.close()
