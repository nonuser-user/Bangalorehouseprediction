# Bangalore Home Price Prediction

A machine learning web application for predicting home prices in Bangalore using Linear Regression with Flask backend and responsive dark-themed frontend. Features integrated DSA implementations for data analysis.

## Features

- **ML Model**: Linear Regression with 79% accuracy
- **Dark Theme**: Modern cyberpunk-style UI with hover animations
- **Real-time Predictions**: Instant price estimates with interactive charts
- **DSA Algorithms**: Heap Sort, Binary Search, and Kth Largest Element
- **Live Demo**: Interactive DSA visualization using your prediction data
- **Responsive Design**: Works seamlessly on all devices

## Tech Stack

**Backend**: Python, Flask, NumPy, Pandas, Scikit-Learn  
**Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js  
**ML**: Linear Regression, Data preprocessing, Outlier removal  
**DSA**: Heap Sort (O(n log n)), Binary Search (O(log n)), Kth Largest

## DSA Implementation

### 1. Heap Sort - O(n log n)
- Sorts price predictions efficiently
- Used for organizing data and finding statistics
- In-place sorting with minimal memory usage

### 2. Binary Search - O(log n)
- Fast searching in sorted price arrays
- Finds specific predictions instantly
- Demonstrates logarithmic time complexity

### 3. Kth Largest Element
- Finds top N highest prices
- Uses heap sort for efficient computation
- Useful for price range analysis

**Live Demo**: Make predictions, then click "Run DSA Demo" to see algorithms work on your data!

## Quick Start

### 1. Setup Environment
```bash
python setup_env.py
```

### 2. Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Train Model
```bash
python train_model.py
```

### 4. Run Application
```bash
python app.py
```

Open browser at: **http://localhost:5000**

## Project Structure

```
├── app.py                  # Flask application
├── train_model.py          # Model training
├── utils/
│   ├── data_processor.py   # Data cleaning
│   ├── model_trainer.py    # ML training
│   └── heap_sort.py        # DSA implementation
├── templates/
│   └── index.html          # Frontend
├── static/
│   ├── css/style.css       # Styling
│   └── js/script.js        # JavaScript
└── models/
    ├── model.pkl           # Trained model
    └── locations.json      # Location data
```

## Model Performance

- **R² Score**: 0.79 (79% accuracy)
- **MAE**: ~19.67 Lakhs
- **Features**: 240 Bangalore locations
- **Training Data**: 12,500+ records

## DSA Algorithms in Action

The project demonstrates three key algorithms:

1. **Heap Sort**: Sorts your predictions in O(n log n) time
2. **Binary Search**: Searches sorted data in O(log n) time  
3. **Kth Largest**: Finds top prices using heap-based approach

Try it: Make predictions → Click "DSA Demo" → See algorithms work on your data!

## API Endpoints

### Predict Price
```
POST /predict
{
  "location": "Whitefield",
  "sqft": 1200,
  "bath": 2,
  "bhk": 2
}
```

### Get Statistics
```
GET /stats
```

## Dataset

- **Source**: Kaggle - Bangalore House Prices
- **Records**: 13,000+
- **Features**: Location, Size, Sqft, Bath, Price

## License

MIT License

---

**Ready to use!** Just follow the Quick Start steps above.
