#hello world!
#herein will be an amazing script that will clean your csv files!
#truly magical

import pandas as pd

def load_data(file_path: str):
    return pd.read_csv(file_path)
    #This function reads the imported .csv as a Panda dataframe
    #This allows functionality between any .csv and this program

def clean_column_names(df):
    df = df.copy()
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
    )
    return df
   #This function cleans column names
   #This prevents input inconsistencies from reappearing in columns

def handle_missing_values(df):
    df = df.copy()
    for column in ["product_name", "category"]:
        if column in df.columns:
            df[column] = df[column].astype("string").str.strip()
    
    df = df.replace({"": pd.NA})
        
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    if "price" in df.columns and "quantity" in df.columns:
        df = df.dropna(subset=["price", "quantity"])

    return df
   #This function adjusts any values considered "invalid"
   #The newly invalidated values are being prepared for erasure
 
def remove_invalid_rows(df):
    df = df.copy()
    if "price" in df.columns:
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df = df[df["price"].notna() & (df["price"] >= 0)]
    if "quantity" in df.columns:
        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df = df[df["quantity"].notna() & (df["quantity"] >= 0)]
    return df
    #This function removes any values that were marked invalid
    #The new .csv will now be fully cleaned!

if __name__ == "__main__":
    raw_path = "data/raw/sales_data_raw.csv"
    cleaned_path = "data/processed/sales_data_clean.csv"

    df_raw = load_data(raw_path)
    df_clean = clean_column_names(df_raw)
    df_clean = handle_missing_values(df_clean)
    df_clean = remove_invalid_rows(df_clean)
    df_clean.to_csv(cleaned_path, index=False)
    print("Cleaning complete. First few rows:")
    print(df_clean.head())