from flask import Flask, render_template, request, jsonify
import json
import numpy as np
import pandas as pd
from flask_cors import CORS
import requests
import time
import os


# Initialize the H2O cluster
#h2o.init()

# Load H2O model
#model_path = "./models/GBM_5_AutoML_1_20241031_73853"  # Replace with the actual model path
#h2o_model = h2o.load_model(model_path)

# Load JSON files for aggregate data and groupings
with open('aggregate_data.json', 'r') as agg_file:
    aggregate_data = json.load(agg_file)

with open('groupings.json', 'r') as group_file:
    groupings = json.load(group_file)

app = Flask(__name__)

# Function to transform features
def transform_features(input_data, aggregate_data, groupings):
    pid = input_data['pid']

    # Convert numeric fields to the correct type
    input_data['price'] = float(input_data['price'])
    input_data['competitorPrice'] = float(input_data['competitorPrice'])
    input_data['content'] = float(input_data['content'])
    input_data['rrp'] = float(input_data['rrp'])
    input_data['availability'] = int(input_data['availability'])
    input_data['genericProduct'] = int(input_data['genericProduct'])

    # Aggregate Data Features (retrieve once)
    aggregate = aggregate_data.get(pid, {})
    total_clicks = aggregate.get('total_clicks', 0)
    total_baskets = aggregate.get('total_baskets', 0)
    total_orders = aggregate.get('total_orders', 0)
    
    input_data['total_clicks'] = total_clicks
    input_data['total_baskets'] = total_baskets
    input_data['total_orders'] = total_orders

    # Action Ratios
    input_data['click_to_basket_ratio'] = round(total_clicks / (total_baskets + 1e-5), 2)
    input_data['basket_to_order_ratio'] = round(total_baskets / (total_orders + 1e-5), 2)
    input_data['click_to_order_ratio'] = round(total_clicks / (total_orders + 1e-5), 2)

    # Competitor Price Features
    input_data['price_competitiveness'] = round((input_data['price'] - input_data['competitorPrice']) / input_data['competitorPrice'], 2)
    input_data['price_rrp_ratio'] = round(input_data['price'] / input_data['rrp'], 2)
    input_data['competitor_undercut_flag'] = int(input_data['price'] < input_data['competitorPrice'])

    # Revenue Per Action Features
    input_data['revenue_per_click'] = round(0.014797, 2)
    input_data['revenue_per_basket'] = round(0.025585, 2)
    input_data['revenue_per_order'] = round(0.011233, 2)

    # Interaction Features
    input_data['price_availability_interaction'] = round(input_data['price'] * input_data['availability'], 2)
    input_data['competitor_availability_interaction'] = round(input_data['competitorPrice'] * input_data['availability'], 2)

    # Adding Grouping Features
    for key, mapping in groupings.items():
        if key in input_data and input_data[key] in mapping:
            input_data[f'{key}_grouped'] = mapping[input_data[key]]
        else:
            input_data[f'{key}_grouped'] = None  # Default if key not found

    # Rearrange the output in the specified order
    ordered_output = {
        'adFlag': int(input_data.get('adFlag')),
        'availability': int(input_data.get('availability')),
        'competitorPrice': float(input_data.get('competitorPrice')),
        'price': float(input_data.get('price')),
        'content': float(input_data.get('content')),
        'genericProduct': int(input_data.get('genericProduct')),
        'rrp': float(input_data.get('rrp')),
        'group_grouped': pd.NA if input_data.get('group_grouped') is None else int(input_data.get('group_grouped')),
        'pharmForm_grouped': float(input_data.get('pharmForm_grouped', np.nan)),
        'manufacturer_grouped': pd.NA if input_data.get('manufacturer_grouped') is None else int(input_data.get('manufacturer_grouped')),
        'category_grouped': float(input_data.get('category_grouped', np.nan)),
        'total_clicks': int(input_data.get('total_clicks')),
        'total_baskets': int(input_data.get('total_baskets')),
        'total_orders': int(input_data.get('total_orders')),
        'click_to_basket_ratio': float(input_data.get('click_to_basket_ratio')),
        'basket_to_order_ratio': float(input_data.get('basket_to_order_ratio')),
        'click_to_order_ratio': float(input_data.get('click_to_order_ratio')),
        'price_competitiveness': float(input_data.get('price_competitiveness')),
        'price_rrp_ratio': float(input_data.get('price_rrp_ratio')),
        'competitor_undercut_flag': int(input_data.get('competitor_undercut_flag')),
        'revenue_per_click': float(input_data.get('revenue_per_click')),
        'revenue_per_basket': float(input_data.get('revenue_per_basket')),
        'revenue_per_order': float(input_data.get('revenue_per_order')),
        'price_availability_interaction': float(input_data.get('price_availability_interaction')),
        'competitor_availability_interaction': float(input_data.get('competitor_availability_interaction'))
    }
    ordered_output = pd.DataFrame([ordered_output])

    return ordered_output

# Route for rendering HTML page
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():

    start_time = time.time()  # Record the start time
    try:
        print("Request received. Processing prediction...")  # Log when request is received

        # Parse input data
        user_input = request.json
        print(f"User Input: {user_input}")  # Log input data for debugging

        # Transform features
        features = transform_features(user_input, aggregate_data, groupings)

        print("Calculating prediction...")  # Log that prediction is being calculated

        # Convert features to H2OFrame
        # h2o_features = H2OFrame(features)

        #backend_url = os.getenv('JAVA_BACKEND_URL', 'http://localhost:8080')

        url = 'http://java-backend:8080/predict'
        # Convert the DataFrame to a dictionary without index
        ordered_output_dict = features.iloc[0].to_dict()

        # Now create the CSV-like string format
        input_data = ','.join([f"{key}:{value}" for key, value in ordered_output_dict.items()])

        response = requests.post(url, data=input_data)
        prediction = response.json()

        print("Calculating prediction...")  # Log that prediction is being calculated
        print(prediction)
        # Make predictions using the H2O model
        #predictions = h2o_model.predict(h2o_features)
        #y_pred_h2o_gbm = h2o.as_list(predictions, use_pandas=False)[1:]
        #y_pred_h2o_gbm = np.array(y_pred_h2o_gbm, dtype=np.float32).flatten()
            
        # Calculate average revenue
        avg_revenue = round(float(np.mean(prediction)), 2)  # Convert to standard float

        print(f"Prediction completed. Predicted Revenue: {avg_revenue}")  # Log prediction result

        # Return JSON response
        return jsonify({'predicted_revenue': avg_revenue})
        

    except Exception as e:
        print(f"Error during prediction: {str(e)}")  # Log any error that occurs
        return jsonify({'error': 'An error occurred during prediction.'}), 500
    finally:
        end_time = time.time()  # Record the end time
        duration = end_time - start_time  # Calculate the duration

        print(f"Time taken to run the prediction: {duration:.4f} seconds")  # Print the time taken

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

CORS(app)  # Allow all origins to access the API
