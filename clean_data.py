import pandas as pd
import numpy as np
import re

def clean_price(price_str):
    """Clean price string and convert to float"""
    if pd.isna(price_str) or price_str == 'N/A':
        return np.nan
    
    # Remove 'US $', commas, and extra spaces
    cleaned = str(price_str).replace('US $', '').replace(',', '').strip()
    
    # Extract numeric value
    match = re.search(r'(\d+\.?\d*)', cleaned)
    if match:
        return float(match.group(1))
    return np.nan

def clean_data():
    """Clean and process the raw eBay data"""
    
    # Load data with all columns as strings
    df = pd.read_csv('ebay_tech_deals.csv', dtype=str)
    
    # Clean price columns
    df['price'] = df['price'].apply(clean_price)
    df['original_price'] = df['original_price'].apply(clean_price)
    
    # If original_price is missing, replace with price
    df['original_price'] = df['original_price'].fillna(df['price'])
    
    # Clean shipping column
    df['shipping'] = df['shipping'].fillna('Shipping info unavailable')
    df['shipping'] = df['shipping'].replace({
        'N/A': 'Shipping info unavailable',
        '': 'Shipping info unavailable'
    })
    df['shipping'] = df['shipping'].apply(
        lambda x: 'Shipping info unavailable' if str(x).strip() == '' else x
    )
    
    # Calculate discount percentage
    df['discount_percentage'] = ((1 - df['price'] / df['original_price']) * 100).round(2)
    
    # Save cleaned data
    df.to_csv('cleaned_ebay_deals.csv', index=False)
    print(f"Cleaned data saved! Total records: {len(df)}")
    
    return df

if __name__ == "__main__":
    clean_data()