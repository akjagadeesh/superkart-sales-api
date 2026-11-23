
import streamlit as st
import pandas as pd
import requests

# Base URL of the Flask backend
BACKEND_URL = "http://backend:7860"

# Streamlit UI
st.title("SuperKart Sales Prediction App")

st.write(
    "This app predicts product-store sales using the "
    "trained SuperKart Random Forest model."
)

st.write("Enter the product and store characteristics below.")

# Numerical features
st.subheader("Numerical Features")

Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.5,
    step=0.1
)

Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.05,
    step=0.01
)

Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=150.0,
    step=1.0
)

Store_Age = st.number_input(
    "Store Age",
    min_value=0,
    value=15,
    step=1
)


# Categorical features
st.subheader("Categorical Features")

Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

Product_Type = st.text_input(
    "Product Type",
    value="Snack Foods"
)

Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier1", "Tier2", "Tier3"]
)

Store_Type = st.text_input(
    "Store Type",
    value="Supermarket Type1"
)


# Create input data
input_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_Type": Product_Type,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Store_Age": Store_Age
}


# Single prediction
if st.button("Predict", type="primary"):

    try:
        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=input_data,
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()

            predicted_sales = result[
                "Predicted_Product_Store_Sales_Total"
            ]

            st.success(
                f"Predicted Product-Store Sales: "
                f"${predicted_sales:,.2f}"
            )

        else:
            st.error(
                f"API Error: {response.status_code}"
            )
            st.write(response.text)

    except requests.exceptions.RequestException as e:
        st.error(f"Could not connect to backend: {e}")


# Batch prediction
st.subheader("Batch Prediction")

st.write(
    "Upload a CSV file containing product and store features "
    "to generate predictions for multiple observations."
)

file = st.file_uploader(
    "Upload CSV file",
    type=["csv"]
)

if file is not None:

    try:
        uploaded_data = pd.read_csv(file)

        st.write("Uploaded Data Preview")
        st.dataframe(uploaded_data.head())

        if st.button("Predict for Batch", type="primary"):

            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={
                    "file": (
                        file.name,
                        file.getvalue(),
                        "text/csv"
                    )
                },
                timeout=60
            )

            if response.status_code == 200:

                result = pd.DataFrame(response.json())

                st.subheader("Batch Prediction Results")
                st.dataframe(result)

                # Download predictions
                csv_data = result.to_csv(index=False)

                st.download_button(
                    label="Download Predictions CSV",
                    data=csv_data,
                    file_name="superkart_predictions.csv",
                    mime="text/csv"
                )

            else:
                st.error(
                    f"API Error: {response.status_code}"
                )
                st.write(response.text)

    except Exception as e:
        st.error(f"Error processing file: {e}")
