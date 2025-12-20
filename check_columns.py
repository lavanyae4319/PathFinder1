import pandas as pd

df = pd.read_csv('dataset/cleaned_job_data.csv')
print("Columns in CSV:")
for col in df.columns:
    print(f"  - {col}")
print(f"\nTotal columns: {len(df.columns)}")
print(f"Total rows: {len(df)}")
print("\nFirst row:")
print(df.iloc[0].to_dict())
