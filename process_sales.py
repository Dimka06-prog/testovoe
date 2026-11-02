import pandas as pd

def process_sales(input_file, output_file):
    """
    Process sales data and generate daily aggregation by SKU.
    
    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file
    """
    # Read CSV
    df = pd.read_csv(input_file)
    
    # Drop rows with missing quantity (4 rows found)
    df = df.dropna(subset=['quantity'])
    
    # Normalize status to lowercase for consistent comparison
    df['status'] = df['status'].str.lower()
    
    # Remove duplicate rows - keep first occurrence
    # One order should be counted once even if duplicated in source
    df = df.drop_duplicates()
    
    # Calculate revenue for delivered orders only AFTER deduplication
    df['revenue'] = df.apply(
        lambda row: row['quantity'] * row['price'] if row['status'] == 'delivered' else 0,
        axis=1
    )
    
    # Group by sku and order_date
    grouped = df.groupby(['sku', 'order_date']).agg({
        'order_id': 'nunique',  # Count unique orders (including cancelled)
        'revenue': 'sum'        # Sum revenue (only delivered have non-zero)
    }).reset_index()
    
    # Rename columns
    grouped.columns = ['sku', 'order_date', 'orders', 'revenue']
    
    # Sort by sku, then by date
    grouped = grouped.sort_values(['sku', 'order_date'])
    
    # Save to CSV
    grouped.to_csv(output_file, index=False)
    
    print(f"Processed {len(df)} rows")
    print(f"Generated {len(grouped)} sku-date combinations")
    print(f"Output saved to {output_file}")
    
    return grouped

if __name__ == "__main__":
    input_csv = "materials/Dannye_dlya_testovogo_zadania.csv"
    output_csv = "daily_by_sku.csv"
    
    result = process_sales(input_csv, output_csv)
    
    # Print sample of results
    print("\nSample output:")
    print(result.head(10))
