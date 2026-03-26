import pandas as pd

def load_and_process_data(filepath='financial_data.csv'):
    """Loads data and calculates financial metrics"""
    
    df = pd.read_csv(filepath, encoding='utf-8')
    
    # Calculate metrics
    df['revenue_growth'] = df['revenue'].pct_change() * 100
    df['operating_margin'] = ((df['revenue'] - df['cogs'] - df['operating_expenses']) / df['revenue']) * 100
    df['net_margin'] = (df['net_income'] / df['revenue']) * 100
    
    return df

def get_data_summary(df):
    """Returns text summary with ASCII only"""
    lines = []
    for _, row in df.iterrows():
        year = int(row['year'])
        revenue = int(row['revenue'])
        growth = round(row['revenue_growth'], 1) if pd.notna(row['revenue_growth']) else 0
        op_margin = round(row['operating_margin'], 1)
        net_margin = round(row['net_margin'], 1)
        
        # No special characters, only numbers and spaces
        lines.append(f"{year} rev={revenue} growth={growth} op={op_margin} net={net_margin}")
    
    return "\n".join(lines)