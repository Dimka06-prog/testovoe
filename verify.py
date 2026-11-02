import pandas as pd

# Read original data
df = pd.read_csv('materials/Dannye_dlya_testovogo_zadania.csv')

# Check a specific example from the first rows
print('=== Verification of first few rows ===')
print('Original data for UYT-0002 on 2026-09-06:')
sample = df[(df['sku'] == 'UYT-0002') & (df['order_date'] == '2026-09-06')]
print(sample)

# Calculate manually on deduplicated data
sample_dedup = sample.drop_duplicates()
print('\nManual calculation (after deduplication):')
print(f'Orders (unique order_id): {sample_dedup["order_id"].nunique()}')
delivered = sample_dedup[sample_dedup['status'].str.lower() == 'delivered']
print(f'Revenue (delivered only): {(delivered["quantity"] * delivered["price"]).sum()}')

# Read result
result = pd.read_csv('daily_by_sku.csv')
print('\n=== Result from daily_by_sku.csv ===')
print(result[(result['sku'] == 'UYT-0002') & (result['order_date'] == '2026-09-06')])

# Overall totals
print('\n=== Overall totals ===')
print(f'Total orders in result: {result["orders"].sum()}')
print(f'Total revenue in result: {result["revenue"].sum()}')

# Compare with original
print('\n=== Original data totals ===')
df_clean = df.dropna(subset=['quantity']).drop_duplicates()
df_clean['status'] = df_clean['status'].str.lower()
print(f'Total unique orders: {df_clean["order_id"].nunique()}')
delivered_only = df_clean[df_clean['status'] == 'delivered']
print(f'Total revenue (delivered): {(delivered_only["quantity"] * delivered_only["price"]).sum()}')

# Check cancelled orders are counted in orders but not revenue
print('\n=== Check cancelled order handling ===')
cancelled_sample = df[(df['status'].str.lower() == 'cancelled')].head(5)
print('Sample cancelled orders:')
print(cancelled_sample[['order_id', 'sku', 'order_date', 'status']])
