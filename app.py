from flask import Flask, render_template, request, jsonify
import numpy as np
import pandas as pd
import pickle
import json
import os
from utils.data_processor import DataProcessor
from utils.model_trainer import ModelTrainer
from utils.heap_sort import heap_sort, binary_search, find_kth_largest

app = Flask(__name__)

# Load model and data
model = None
locations = []
data_processor = None

def load_artifacts():
    global model, locations, data_processor
    try:
        with open('models/model.pkl', 'rb') as f:
            model = pickle.load(f)
        with open('models/locations.json', 'r') as f:
            locations = json.load(f)
        data_processor = DataProcessor()
        print("Artifacts loaded successfully")
    except Exception as e:
        print(f"Error loading artifacts: {e}")

@app.route('/')
def home():
    return render_template('index.html', locations=sorted(locations))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        location = data['location']
        sqft = float(data['sqft'])
        bath = int(data['bath'])
        bhk = int(data['bhk'])
        
        # Prepare input
        loc_index = locations.index(location) if location in locations else -1
        x = np.zeros(len(locations) + 3)
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        if loc_index >= 0:
            x[loc_index + 3] = 1
        
        # Predict
        predicted_price = model.predict([x])[0]
        
        return jsonify({
            'success': True,
            'predicted_price': round(predicted_price, 2),
            'price_per_sqft': round((predicted_price * 100000) / sqft, 2)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/train', methods=['POST'])
def train_model():
    try:
        trainer = ModelTrainer()
        metrics = trainer.train()
        return jsonify({'success': True, 'metrics': metrics})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/stats')
def get_stats():
    try:
        df = pd.read_csv('bengaluru_house_prices.xls')
        prices = df['price'].tolist()
        
        # Use DSA algorithms for statistics
        top_10_price = find_kth_largest(prices, 10)
        
        stats = {
            'total_records': len(df),
            'locations': len(df['location'].unique()),
            'avg_price': round(df['price'].mean(), 2),
            'price_range': {
                'min': round(df['price'].min(), 2),
                'max': round(df['price'].max(), 2)
            },
            'top_10_price': round(top_10_price, 2)
        }
        return jsonify({'success': True, 'stats': stats})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dsa-demo', methods=['POST'])
def dsa_demo():
    """Demonstrate DSA algorithms on sample data"""
    try:
        data = request.json
        prices = data.get('prices', [100, 50, 200, 75, 150, 300, 25, 175])
        
        # Heap Sort
        sorted_prices = heap_sort(prices.copy())
        
        # Kth Largest
        top_3 = find_kth_largest(prices, 3)
        
        # Binary Search
        target = data.get('target', 150)
        search_index = binary_search(sorted_prices, target)
        
        return jsonify({
            'success': True,
            'original': prices,
            'sorted': sorted_prices,
            'top_3_price': round(top_3, 2),
            'binary_search': {
                'target': target,
                'found_at_index': search_index,
                'found': search_index != -1
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    load_artifacts()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
