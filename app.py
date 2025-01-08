import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load the scaler and model
with open(r"D:\My Work\Infosys Spring Board AI Intern\Energy Consumption Prediction\Model\scaler.pkl", 'rb') as file:
    loaded_scaler = pickle.load(file)

with open(r"D:\My Work\Infosys Spring Board AI Intern\Energy Consumption Prediction\Model\energy_predict.pkl", 'rb') as file:
    loaded_model = pickle.load(file)

# Sample user credentials
users = {
    "admin": "password123",
    "user1": "userpass",
}

# Function to check login credentials
def login(username, password):
    return users.get(username) == password

# Session state for login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Login interface
if not st.session_state["logged_in"]:
    st.sidebar.title("Login")
    with st.sidebar.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if login(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.sidebar.success(f"Welcome, {username}!")
            else:
                st.sidebar.error("Invalid credentials. Please try again.")
else:
    st.sidebar.success(f"Welcome, {st.session_state['username']}!")
    st.sidebar.button("Logout", on_click=lambda: st.session_state.update({"logged_in": False}))

    # Sidebar buttons for navigation
    st.sidebar.markdown("---")
    menu = st.sidebar.radio(
        "Select an option:",
        ["⚡ Energy Consumption Prediction", "👁️ Visualize Data", "📚 Instructions", "📊 Data","📊 Key Performance Indicators","🔮 Forecasting"]
    )
    st.sidebar.markdown("---")
    st.sidebar.markdown("Developed by Saipraneeth Sattu")

    if menu == "⚡ Energy Consumption Prediction":
        # Main app content for Energy Prediction
        st.title("Energy Consumption Prediction & Insights")
        st.markdown(
            "Predict and analyze energy consumption in smart buildings based on various environmental factors. "
            "Gain insights into energy patterns for improved energy management."
        )

        # Input fields with validation
        st.header("🔧 Input Parameters")
        heat = st.number_input("Heat (J)", min_value=40.0, max_value=140.0, value=90.0)
        relative_humidity = st.number_input("Relative Humidity (%)", min_value=28.0, max_value=100.0, value=60.0)
        air_temperature = st.number_input("Air Temperature (°C)", min_value=-10.0, max_value=10.0, value=0.0)
        wind_speed = st.number_input("Wind Speed (m/s)", min_value=0.0, max_value=15.0, value=5.0)
        weekend = st.selectbox("Weekend", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")
        pressure = st.number_input("Pressure (msl) (hPa)", min_value=960.0, max_value=1030.0, value=995.0)

        # Prepare the input data as a DataFrame
        input_values = pd.DataFrame({
            'Heat': [heat],
            'Relative humidity (%)': [relative_humidity],
            'Air temperature (degC)': [air_temperature],
            'Wind speed (m/s)': [wind_speed],
            'Weekend': [weekend],
            'Pressure (msl) (hPa)': [pressure]
        })

        # Scale the input values
        scaled_values = loaded_scaler.transform(input_values)

        # Prediction button
        if st.button("⚡ Predict Energy Consumption"):
            prediction = loaded_model.predict(scaled_values)
            st.markdown("## 📊 Energy Consumption Prediction Result")
            st.metric(label="Predicted Energy Consumption (kWh)", value=f"{prediction[0]:.2f}")

            # Display input values in a table
            st.markdown("### 🔍 Input Values Overview")
            st.table(input_values)

    elif menu == "👁️ Visualize Data":
        # Analysis section
        # Section Header
        st.markdown("---")
        st.markdown("## 🔍 Energy Consumption Insights & Analysis")

        # Mock data for analysis (replace with real data if available)
        data = pd.DataFrame({
            "Date": pd.date_range(start="2023-01-01", periods=30),
            "Energy Consumption (kWh)": np.random.uniform(50, 150, 30),
            "Heat (J)": np.random.uniform(40, 140, 30),
            "Humidity (%)": np.random.uniform(28, 100, 30),
            "Temperature (°C)": np.random.uniform(15, 35, 30)
        })

        ### 📅 Energy Consumption Trend
        st.markdown("### 📅 Energy Consumption Trend")
        fig = px.line(data, x="Date", y="Energy Consumption (kWh)", title="Daily Energy Consumption Trend")
        fig.update_layout(
            xaxis_title='Date',
            yaxis_title='Energy Consumption (kWh)',
            xaxis_rangeslider_visible=True,
            template="plotly_dark"
        )
        st.plotly_chart(fig)

        ### 🔥 Correlation Heatmap: Inputs vs Energy Consumption
        st.markdown("### 🔥 Correlation Heatmap: Inputs vs Energy Consumption")
        corr = data[['Energy Consumption (kWh)', 'Heat (J)', 'Humidity (%)', 'Temperature (°C)']].corr()
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu", title="Correlation Heatmap")
        st.plotly_chart(fig)

        ### 📊 Distribution of Energy Consumption
        st.markdown("### 📊 Distribution of Energy Consumption")
        fig = px.histogram(data, x="Energy Consumption (kWh)", nbins=15, title="Distribution of Energy Consumption")
        fig.update_layout(
            xaxis_title="Energy Consumption (kWh)",
            yaxis_title="Frequency",
            template="plotly_dark"
        )
        st.plotly_chart(fig)

        ### 🌡️ Temperature vs Energy Consumption
        st.markdown("### 🌡️ Temperature vs Energy Consumption")
        fig = px.scatter(data, x="Temperature (°C)", y="Energy Consumption (kWh)", title="Temperature vs Energy Consumption")
        fig.update_traces(marker=dict(size=10, color='orange', line=dict(width=1, color='black')))
        fig.update_layout(
            xaxis_title="Temperature (°C)",
            yaxis_title="Energy Consumption (kWh)",
            template="plotly_dark"
        )
        st.plotly_chart(fig)

        ### 💧 Humidity vs Energy Consumption
        st.markdown("### 💧 Humidity vs Energy Consumption")
        fig = px.scatter(data, x="Humidity (%)", y="Energy Consumption (kWh)", title="Humidity vs Energy Consumption", color="Humidity (%)")
        fig.update_layout(
            xaxis_title="Humidity (%)",
            yaxis_title="Energy Consumption (kWh)",
            template="plotly_dark"
        )
        st.plotly_chart(fig)

        ### 📈 Trend Comparison: Energy Consumption vs Heat
        st.markdown("### 📈 Trend Comparison: Energy Consumption vs Heat")
        fig = px.line(data, x="Date", y=["Energy Consumption (kWh)", "Heat (J)"], title="Trend Comparison: Energy Consumption vs Heat")
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Values",
            template="plotly_dark"
        )
        st.plotly_chart(fig)

    elif menu == "📚 Instructions":
        st.markdown("### 🔎 Instructions for Using the App")
        st.markdown(""" 
        1. **Enter the Input Parameters**: Fill in the fields for Heat, Relative Humidity, Air Temperature, Wind Speed, Weekend, and Pressure.
        2. **Click on '⚡ Predict Energy Consumption'**: After entering the data, click this button to get the energy consumption prediction.
        3. **Click on '👁️ Visualize Data'**: This button will show the energy consumption trends, correlation heatmap, and weekend vs weekday comparisons.
        4. **Click on '📚 Instructions'**: This button shows how to use the app.
        5. **Click on '📊 Data'**: This button shows more information about the dataset used for this prediction tool.
        """)
        
    elif menu == "📊 Data":
        st.markdown("### 📂 Dataset Information")
        st.markdown(""" 
        The data for this study was collected from the Electricity Consumption and Weather Indicators Datasets, available on the AI4EU platform. You can access the dataset here:
        👉 [AI4EU Platform - Electricity Consumption Dataset](https://www.ai4europe.eu/research/ai-catalog/electricity-consumption-and-weather-indicators-datasets)

        This dataset contains hourly electricity and heating consumption data from an office building located in the Malmi area of Helsinki, Finland. It includes weather-related variables from the Helsinki Malmi lentokenttä meteorological station.
        """)

        # Load and display the dataset from a CSV file
        df = pd.read_csv(r"D:\My Work\Infosys Spring Board AI Intern\Energy Consumption Prediction\Dataset\Malmi_office_building_hourly.csv")  # Replace with the correct path to your CSV file
        st.markdown("### 📊 Dataset")
        st.dataframe(df)

    elif menu == "🔮 Forecasting":
        st.markdown("## 🔮 Energy Consumption Forecasting")
        st.write("Coming Soon! Stay Tuned.")

    elif menu == "📊 Key Performance Indicators":
        df = pd.read_csv(r"D:\My Work\Infosys Spring Board AI Intern\Energy Consumption Prediction\Dataset\Final_dataset.csv")

        st.markdown("### 📊 Key Performance Indicators")
        col1, col2, col3 = st.columns(3)
        col1.metric("Average Energy Consumption", f"{df['ElCons'].mean():.2f} kWh")
        col2.metric("Average Temperature", f"{df['Air temperature (degC)'].mean():.2f} °C")
        col3.metric("Average Humidity", f"{df['Relative humidity (%)'].mean():.2f} %")

    # Footer
    st.markdown("---")
    
