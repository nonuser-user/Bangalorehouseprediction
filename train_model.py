"""
Train the machine learning model
Run this script to train and save the model
"""
from utils.model_trainer import ModelTrainer
from utils.heap_sort import heap_sort, binary_search, find_kth_largest
import numpy as np

def main():
    print("=" * 60)
    print("BANGALORE HOME PRICE PREDICTION - MODEL TRAINING")
    print("=" * 60)
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    print("\n[1/3] Loading and preparing data...")
    trainer.prepare_data()
    print(f"✓ Data prepared: {len(trainer.X)} samples")
    print(f"✓ Features: {len(trainer.X.columns)}")
    print(f"✓ Locations: {len(trainer.locations)}")
    
    print("\n[2/3] Training model...")
    metrics = trainer.train()
    
    print("\n[3/3] Model trained successfully!")
    print("\nModel Performance Metrics:")
    print("-" * 40)
    print(f"R² Score:     {metrics['r2_score']}")
    print(f"MAE:          {metrics['mae']} Lakhs")
    print(f"RMSE:         {metrics['rmse']} Lakhs")
    print(f"Train Size:   {metrics['train_size']}")
    print(f"Test Size:    {metrics['test_size']}")
    print("-" * 40)
    
    # Demonstrate DSA algorithms (Data Structures & Algorithms)
    print("\n[DSA] Demonstrating Algorithms on Sample Predictions...")
    sample_predictions = np.random.uniform(30, 200, 10)
    
    print(f"\nOriginal prices: {[round(x, 2) for x in sample_predictions]}")
    
    # Heap Sort
    sorted_prices = heap_sort(sample_predictions.copy().tolist())
    print(f"Heap Sorted:     {[round(x, 2) for x in sorted_prices]}")
    
    # Kth Largest Element
    top_3 = find_kth_largest(sample_predictions.tolist(), 3)
    print(f"\n3rd Highest Price: {round(top_3, 2)} Lakhs")
    
    # Binary Search
    target = sorted_prices[5]
    index = binary_search(sorted_prices, target)
    print(f"Binary Search for {round(target, 2)}: Found at index {index}")
    
    print("\n✓ Model saved to 'models/model.pkl'")
    print("✓ Locations saved to 'models/locations.json'")
    print("\nYou can now run the Flask app: python app.py")
    print("=" * 60)

if __name__ == "__main__":
    main()
