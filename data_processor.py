import pandas as pd

def load_and_process_data(filepath='financial_data.csv'):
    """Загружает данные и рассчитывает финансовые метрики"""
    df = pd.read_csv(filepath)
    
    # Рассчитываем рост выручки (в процентах)
    df['revenue_growth'] = df['revenue'].pct_change() * 100
    
    # Рассчитываем операционную маржу (в процентах)
    # Операционная прибыль = revenue - cogs - operating_expenses
    df['operating_margin'] = ((df['revenue'] - df['cogs'] - df['operating_expenses']) / df['revenue']) * 100
    
    # Рассчитываем чистую маржу (в процентах)
    df['net_margin'] = (df['net_income'] / df['revenue']) * 100
    
    return df

def get_data_summary(df):
    """Возвращает текстовое представление данных для LLM"""
    lines = []
    for _, row in df.iterrows():
        year = int(row['year'])
        revenue = f"${row['revenue']:,.0f}"
        growth = f"{row['revenue_growth']:.1f}%" if pd.notna(row['revenue_growth']) else "N/A"
        op_margin = f"{row['operating_margin']:.1f}%"
        net_margin = f"{row['net_margin']:.1f}%"
        
        lines.append(f"{year}: revenue={revenue}, growth={growth}, op_margin={op_margin}, net_margin={net_margin}")
    
    return "\n".join(lines)

if __name__ == "__main__":
    # Тестовый запуск
    df = load_and_process_data()
    print(get_data_summary(df))