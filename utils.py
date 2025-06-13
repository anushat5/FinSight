import pandas as pd

def load_data(uploaded_file):
    return pd.read_csv(uploaded_file)

def categorize_expenses(df):
    def classify(desc):
        desc = desc.lower()
        if any(x in desc for x in ['salary', 'credit']):
            return 'Income'
        elif any(x in desc for x in ['swiggy', 'zomato']):
            return 'Food'
        elif 'amazon' in desc:
            return 'Shopping'
        elif 'uber' in desc or 'ola' in desc:
            return 'Transport'
        else:
            return 'Other'
    df['Category'] = df['Description'].apply(classify)
    return df
