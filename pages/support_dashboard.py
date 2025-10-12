import streamlit as st
import mysql.connector
from datetime import datetime

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Abbivimi@7",
        database="user_management"
    )


def show_dashboard():

    st.markdown(
        """
        <style>
         .block-container {
            max-width: 95% !important;
            padding-top: 2rem !important;     
            padding-bottom: 1rem !important;  
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    

        
        .header-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
        }
         .logout-btn {
            
            position: absolute;
            top: 20px;
            right: 20px;
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
        </style>
        """,
        unsafe_allow_html=True
    )
    

    st.title("Support Dashboard")

    col1, col2 = st.columns([8, 2])
    with col1:
        st.header("Queries")
    with col2:
        if st.button("Logout", key="logout_btn"):
            st.session_state.clear()
            st.success("Logged out successfully!")
            st.stop()            

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM client_queries ORDER BY query_created_time DESC")
    queries = cursor.fetchall()
    conn.close()

    open_queries = [q for q in queries if q["status"] == "Open"]
    closed_queries = [q for q in queries if q["status"] == "Closed"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Closed Queries")
        if not closed_queries:
            st.info("No closed queries.")
        for q in closed_queries:
            with st.expander(f"{q['query_heading']}", expanded=False):
                st.markdown(f"**Email:** {q['mail_id']}")
                st.markdown(f"**Mobile:** {q['mobile_number']}")
                st.markdown(f"**Description:** {q['query_description']}")
                st.markdown(f"**Created:** {q['query_created_time']}")
                st.markdown(f"**Closed:** {q['query_closed_time']}")
                if q.get("answer"):
                    st.markdown(f"**Answer:** {q['answer']}")

    with col2:
        
        st.subheader("Open Queries")
        if not open_queries:
            st.info("No open queries.")
        for q in open_queries:
            with st.expander(f"{q['query_heading']}", expanded=False):
                st.markdown(f"**Email:** {q['mail_id']}")
                st.markdown(f"**Mobile:** {q['mobile_number']}")
                st.markdown(f"**Description:** {q['query_description']}")
                st.markdown(f"**Created:** {q['query_created_time']}")

                answer = st.text_area("Answer", value=q.get("answer") or "", key=f"ans_{q['query_id']}")
                if st.button("Close Query", key=f"close_{q['query_id']}"):
                    conn = get_db_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        UPDATE client_queries
                        SET status = %s, query_closed_time = %s, answer = %s
                        WHERE query_id = %s
                        """,
                        ("Closed", datetime.now(), answer, q["query_id"])
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"Query '{q['query_heading']}' closed successfully!")
                    st.rerun()
