import pandas as pd
import numpy as np

class DataProcessor:
    def __init__(self):
        self.df = None
    
    def load_data(self, filepath='bengaluru_house_prices.xls'):
        """Load dataset"""
        self.df = pd.read_csv(filepath)
        return self.df
    
    def clean_data(self):
        """Clean and preprocess data"""
        # Drop unnecessary columns
        df = self.df.drop(['area_type', 'availability', 'society', 'balcony'], axis='columns')
        
        # Drop null values
        df = df.dropna()
        
        # Extract BHK
        df['bhk'] = df['size'].apply(lambda x: int(x.split(" ")[0]))
        
        # Convert total_sqft to numeric
        df['total_sqft'] = df['total_sqft'].apply(self._convert_sqft_to_num)
        
        # Drop rows with None in total_sqft
        df = df[df['total_sqft'].notna()]
        
        # Add price per sqft
        df['price_per_sqft'] = df['price'] * 100000 / df['total_sqft']
        
        # Dimensionality reduction for location
        df.location = df.location.apply(lambda x: x.strip())
        location_stats = df.groupby('location')['location'].agg('count').sort_values(ascending=False)
        location_stats_less_than_10 = location_stats[location_stats <= 10]
        df.location = df.location.apply(lambda x: 'other' if x in location_stats_less_than_10 else x)
        
        self.df = df
        return df
    
    def _convert_sqft_to_num(self, x):
        """Convert sqft ranges to numeric"""
        tokens = str(x).split("-")
        if len(tokens) == 2:
            return (float(tokens[0]) + float(tokens[1])) / 2
        try:
            return float(x)
        except:
            return None
    
    def remove_outliers(self):
        """Remove outliers from data"""
        df = self.df.copy()
        
        # Remove properties with sqft/bhk < 300
        df = df[~(df.total_sqft / df.bhk < 300)]
        
        # Remove price per sqft outliers
        def remove_pps_outliers(df):
            df_out = pd.DataFrame()
            for key, subdf in df.groupby('location'):
                m = np.mean(subdf.price_per_sqft)
                st = np.std(subdf.price_per_sqft)
                reduced_df = subdf[(subdf.price_per_sqft > (m - st)) & (subdf.price_per_sqft <= (m + st))]
                df_out = pd.concat([df_out, reduced_df], ignore_index=True)
            return df_out
        
        df = remove_pps_outliers(df)
        
        # Remove properties where bath > bhk + 2
        df = df[df.bath < df.bhk + 2]
        
        self.df = df
        return df
    
    def get_processed_data(self):
        """Get final processed data"""
        return self.df
