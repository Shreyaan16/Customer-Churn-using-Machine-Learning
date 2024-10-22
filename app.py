import streamlit as st
from joblib import load

#loading the model
model = load('churn_prediction_model.joblib')

#getting the user inputs
gender = st.selectbox("Gender", ('Male', 'Female'))
senior_citizen = st.selectbox("Senior Citizen (Age > 65)", ('Yes', "No"))
partner = st.selectbox('Partner', ('Yes', 'No'))
dependents = st.selectbox('Any Dependents', ('Yes', 'No'))
tenure = int(st.slider("Enter tenure", 0, 75, 0))
phone_service = st.selectbox('Phone Service', ('Yes', 'No'))

if phone_service == 'Yes':
    multiple_lines = st.selectbox('Multiple Lines', ('Yes', 'No'))
else:
    multiple_lines = 'No'

internet_service = st.selectbox('Internet Service', ('DSL', 'Fiber optic', 'No'))

if internet_service != 'No':
    online_security = st.selectbox('Online Security', ('Yes', 'No'))
    online_backup = st.selectbox('Online Backup', ('Yes', 'No'))
    device_protection = st.selectbox('Device Protection', ('Yes', 'No'))
    tech_support = st.selectbox('Tech Support', ('Yes', 'No'))
    streaming_tv = st.selectbox('Streaming TV', ('Yes', 'No'))
    streaming_movies = st.selectbox('Streaming Movies', ('Yes', 'No'))
else:
    online_security = 'No'
    online_backup = 'No'
    device_protection = 'No'
    tech_support = 'No'
    streaming_tv = 'No'
    streaming_movies = 'No'

contract = st.selectbox('Contract', ('Month-to-month', 'One year', 'Two Years'))
paperless_billing = st.selectbox('Paperless Billing', ('Yes', 'No'))
payment_method = st.selectbox('Payment Method', ('Electronic check', 'Mailed Check', 'Bank transfer (automatic)', 'Credit Card (automatic)'))
monthly_charges = st.number_input("Enter the monthly charges:", format="%.2f")
total_charges = st.number_input("Enter the total charges:", format="%.2f")

# Encode the user inputs
gender = 0 if gender == 'Female' else 1
senior_citizen = 1 if senior_citizen == 'Yes' else 0
partner = 1 if partner == 'Yes' else 0
dependents = 1 if dependents == 'Yes' else 0
phone_service = 1 if phone_service == 'Yes' else 0
multiple_lines = 1 if multiple_lines == 'Yes' else 0
online_security = 1 if online_security == 'Yes' else 0
online_backup = 1 if online_backup == 'Yes' else 0
device_protection = 1 if device_protection == 'Yes' else 0
tech_support = 1 if tech_support == 'Yes' else 0
streaming_tv = 1 if streaming_tv == 'Yes' else 0
streaming_movies = 1 if streaming_movies == 'Yes' else 0
paperless_billing = 1 if paperless_billing == 'Yes' else 0

# One-hot encoding for 'internet_service', 'contract', and 'payment_method'
if internet_service == 'DSL':
    internet_service = [1, 0, 0]
elif internet_service == 'Fiber optic':
    internet_service = [0, 1, 0]
else:
    internet_service = [0, 0, 1]

if contract == 'Month-to-month':
    contract = [1, 0, 0]
elif contract == 'One year':
    contract = [0, 1, 0]
else:
    contract = [0, 0, 1]

if payment_method == 'Electronic check':
    payment_method = [1, 0, 0, 0]
elif payment_method == 'Mailed Check':
    payment_method = [0, 1, 0, 0]
elif payment_method == 'Bank transfer (automatic)':
    payment_method = [0, 0, 1, 0]
else:
    payment_method = [0, 0, 0, 1]

# Prepare input for prediction by flattening lists into a single list
first_inputs = [
    gender, senior_citizen, partner, dependents, tenure,
    phone_service, multiple_lines, online_security, online_backup,
    device_protection, tech_support, streaming_tv, streaming_movies,
    paperless_billing, monthly_charges, total_charges
    ]

inputs = first_inputs + internet_service + contract + payment_method

# Perform prediction
prediction = model.predict([inputs])

# Display prediction result
st.title(f"Churn Prediction: {'Yes' if prediction[0] == 1 else 'No'}")
    