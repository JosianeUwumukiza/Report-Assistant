import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# Set page configuration
st.set_page_config(page_title="Report Making Helper", page_icon=":memo:", layout="centered")

# Set a predefined username and password
USERNAME = "admin"
PASSWORD = "gX5@#vP8zL!q"

# Define a function to check the credentials
def check_password():
    # Use Streamlit's session state to store authentication status
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.subheader("Please log in")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.button("Log in"):
            if username == USERNAME and password == PASSWORD:
                st.session_state.authenticated = True
                st.success("You are logged in!")
            else:
                st.error("Invalid username or password")
                
    return st.session_state.authenticated

# Check if the user is authenticated
if check_password():
    st.title("Welcome to the Report Making Helper")
    st.write("You are now authenticated to use this app.")

    # Load custom CSS for styling
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Display header with a light blue background
    st.markdown('<div class="main-header">Report Making Helper</div>', unsafe_allow_html=True)
    st.write("This app generates a report from bullet points and visualizes data in charts.")

    # Report Generation Section
    st.markdown('<div class="section-header">Report Generator</div>', unsafe_allow_html=True)
    bullet_points = st.text_area("Enter bullet points for the report:")

    if st.button("Generate Report"):
        response = requests.post("http://127.0.0.1:5000/generate_report", json={"bullet_points": bullet_points})
        report = response.json().get("report", "No report generated.")
        
        st.subheader("Generated Report")
        st.markdown(f'<div class="report-box">{report}</div>', unsafe_allow_html=True)
        st.download_button(
            label="Download Report",
            data=report,
            file_name="generated_report.txt",
            mime="text/plain",
            key="download_button"
        )

    # Data Visualization Section
    st.markdown('<div class="section-header">Data Visualization</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        st.write("Data Preview", data.head())
        
        # Select columns for x and y axes
        x_column = st.selectbox("Select X-axis column", data.columns)
        y_column = st.selectbox("Select Y-axis column", data.columns)
        
        # Select chart type
        chart_type = st.selectbox("Select Chart Type", ["Line Chart", "Bar Chart", "Pie Chart", "Scatter Plot", "Sankey Chart"])
        
        # Generate and display the selected chart type
        if st.button("Generate Chart"):
            if chart_type == "Line Chart":
                fig = px.line(data, x=x_column, y=y_column, title="Line Chart")
            elif chart_type == "Bar Chart":
                fig = px.bar(data, x=x_column, y=y_column, title="Bar Chart")
            elif chart_type == "Pie Chart":
                fig = px.pie(data, names = x_column, values= y_column, title="Pie Chart")
            elif chart_type == "Scatter Plot":
                fig = px.scatter(data, x=x_column, y=y_column, title="Scatter Plot")
            elif chart_type == "Sankey Chart":
                fig = go.Figure(data=[go.Sankey(
                    node=dict(
                        pad=15,
                        thickness=20,
                        line=dict(color="black", width=0.5),
                        label=data[x_column].unique().tolist(),
                        color="blue"
                    ),
                    link=dict(
                        source=[0, 1, 0, 2, 3],  
                        target=[1, 2, 3, 4, 4],  
                        value=[1, 2, 2, 2, 1]    
                    )
                )])
                fig.update_layout(title_text="Sankey Chart", font_size=10)
            
            st.plotly_chart(fig)
