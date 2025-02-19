from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

# Load the trained model, scaler, and label encoders
model = joblib.load('best_model.pkl')
scaler = joblib.load('scaler.pkl')
label_encoders = joblib.load('label_encoders.pkl')

# Function to preprocess input data
def preprocess_input(input_data, label_encoders, scaler):
    # Convert input data to DataFrame
    input_df = pd.DataFrame([input_data])
    
    # Encode categorical variables
    for column, le in label_encoders.items():
        if column in input_df.columns:
            input_df[column] = le.transform(input_df[column])
    
    # Scale the features
    scaled_input = scaler.transform(input_df)
    
    return scaled_input

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input from the form
        input_data = {
            'Age': int(request.form['Age']),
            'Gender': request.form['Gender'],
            'Race': request.form['Race'],
            'Region': request.form['Region'],
            'Urban_or_Rural': request.form['Urban_or_Rural'],
            'Socioeconomic_Status': request.form['Socioeconomic_Status'],
            'Family_History': request.form['Family_History'],
            'Previous_Cancer_History': request.form['Previous_Cancer_History'],
            'Stage_at_Diagnosis': request.form['Stage_at_Diagnosis'],
            'Tumor_Aggressiveness': request.form['Tumor_Aggressiveness'],
            'Colonoscopy_Access': request.form['Colonoscopy_Access'],
            'Screening_Regularity': request.form['Screening_Regularity'],
            'Diet_Type': request.form['Diet_Type'],
            'BMI': float(request.form['BMI']),
            'Physical_Activity_Level': request.form['Physical_Activity_Level'],
            'Smoking_Status': request.form['Smoking_Status'],
            'Alcohol_Consumption': request.form['Alcohol_Consumption'],
            'Red_Meat_Consumption': request.form['Red_Meat_Consumption'],
            'Fiber_Consumption': request.form['Fiber_Consumption'],
            'Insurance_Coverage': request.form['Insurance_Coverage'],
            'Time_to_Diagnosis': request.form['Time_to_Diagnosis'],
            'Treatment_Access': request.form['Treatment_Access'],
            'Chemotherapy_Received': request.form['Chemotherapy_Received'],
            'Radiotherapy_Received': request.form['Radiotherapy_Received'],
            'Surgery_Received': request.form['Surgery_Received'],
            'Follow_Up_Adherence': request.form['Follow_Up_Adherence']
        }

        # Preprocess the input data
        processed_input = preprocess_input(input_data, label_encoders, scaler)

        # Make prediction
        prediction = model.predict(processed_input)

        # Map prediction to human-readable result
        result = "Survived" if prediction[0] == 1 else "Deceased"

        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)