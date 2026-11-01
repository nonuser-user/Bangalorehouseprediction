import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import pickle
import json
from utils.data_processor import DataProcessor
from utils.heap_sort import heap_sort

class ModelTrainer:
    def __init__(self):
        self.model = None
        self.X = None
        self.y = None
        self.locations = []
    
    def prepare_data(self):
        """Prepare data for training"""
        processor = DataProcessor()
        processor.load_data()
        processor.clean_data()
        processor.remove_outliers()
        df = processor.get_processed_data()
        
        # Create dummy variables for location
        dummies = pd.get_dummies(df.location)
        df = pd.concat([df, dummies.drop('other', axis='columns')], axis='columns')
        
        # Drop unnecessary columns
        df = df.drop(['location', 'size', 'price_per_sqft'], axis='columns')
        
        # Prepare X and y
        self.X = df.drop('price', axis='columns')
        self.y = df['price']
        self.locations = list(self.X.columns[3:])
        
        return self.X, self.y
    
    def train(self):
        """Train the model"""
        self.prepare_data()
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            self.X, self.y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        
        # Save model and locations
        with open('models/model.pkl', 'wb') as f:
            pickle.dump(self.model, f)
        
        with open('models/locations.json', 'w') as f:
            json.dump(self.locations, f)
        
        metrics = {
            'r2_score': round(r2, 4),
            'mae': round(mae, 2),
            'rmse': round(rmse, 2),
            'train_size': len(X_train),
            'test_size': len(X_test)
        }
        
        return metrics
    
    def predict(self, location, sqft, bath, bhk):
        """Make prediction"""
        loc_index = self.locations.index(location) if location in self.locations else -1
        x = np.zeros(len(self.locations) + 3)
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        if loc_index >= 0:
            x[loc_index + 3] = 1
        
        return self.model.predict([x])[0]
