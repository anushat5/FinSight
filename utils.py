import pandas as pd

def load_data(uploaded_file):
    df = pd.read_csv(uploaded_file)
    
    # Clean basic column names
    df.columns = [col.strip().capitalize() for col in df.columns]
    
    # Ensure consistent formatting
    df['Description'] = df['Description'].astype(str).str.lower().str.strip()
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    return df

def categorize_expenses(df):
    def classify(desc):
        if any(x in desc for x in ['salary', 'credit', 'income']):
            return 'Income'
        elif any(x in desc for x in ['swiggy', 'zomato', 'restaurant', 'food']):
            return 'Food'
        elif any(x in desc for x in ['amazon', 'flipkart', 'shopping']):
            return 'Shopping'
        elif any(x in desc for x in ['uber', 'ola', 'transport', 'bus', 'taxi']):
            return 'Transport'
        elif any(x in desc for x in ['electricity', 'water', 'rent', 'bill']):
            return 'Utilities'
        elif any(x in desc for x in ['medical', 'hospital', 'doctor']):
            return 'Health'
        elif any(x in desc for x in ['movie', 'entertainment', 'netflix']):
            return 'Entertainment'
        else:
            return 'Other'

    df['Category'] = df['Description'].apply(classify)
    return df
