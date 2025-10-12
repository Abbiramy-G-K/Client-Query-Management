Overview

The Client Query Management System is a web-based application built using Streamlit and MySQL to facilitate seamless interaction between support teams and clients.The system allows clients to submit queries, track their statuses, and receive responses, while support staff can efficiently manage, answer, and close client queries. The project emphasizes simplicity, usability, and a responsive dashboard layout for both clients and support teams.

Features
Client Side

Login & Authentication: Secure login for clients with password hashing.
Create New Query: Clients can submit new queries with a heading, description, email, and mobile number.
View Queries: Clients can view all their queries, separated into Open and Closed categories.
Query Status Tracking: Easily check whether queries have been addressed and view responses from support staff.
Logout: Clients can safely log out, with a confirmation message and page refresh.

Support Side

Login & Authentication: Secure login for support staff.
View Queries: All client queries are displayed in Open and Closed categories with detailed information.
Answer Queries: Provide answers directly through the support dashboard.
Close Queries: Mark queries as closed with an optional answer, updating the client dashboard in real-time.
Wide Dashboard Layout: Designed for better readability and usability, with columns for open and closed queries.
Logout: Support users can safely log out and return to the login page.

Technology Stack

Frontend : Streamlit
 – for UI and application flow.

Database: MySQL
 – for storing user credentials and client queries.

Python Libraries: 
Pandas - to read the excel file in the first place 

mysql.connector – for database connection.
datetime – to manage timestamps for query creation and closure.
hashlib – for secure password hashing.
