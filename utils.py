# utils.py
import os

import pandas as pd

from config import MASTER_FILE
from excel_handler import backup_excel


def merge_to_master(new_stock_df):
    # Backup master first
    if os.path.exists(MASTER_FILE):
        backup_excel(MASTER_FILE)
        master_df = pd.read_excel(MASTER_FILE)
    else:
        master_df = pd.DataFrame(columns=new_stock_df.columns)

    # Merge: sum quantities for duplicate UIDs
    combined = pd.concat([master_df, new_stock_df], ignore_index=True)
    combined = combined.groupby(["UID","Brand","Model","Color","Size"], as_index=False).agg({"Quantity":"sum"})

    # Save back
    combined.to_excel(MASTER_FILE, index=False)
    print(f"💾 Master inventory updated: {MASTER_FILE}")

def save_mappings(mappings):
    """Save all mapping DataFrames back into code_mappings.xlsx"""
    path = "data/code_mappings.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl", mode="w") as writer:
        for sheet, df in mappings.items():
            df.to_excel(writer, sheet_name=sheet, index=False)


def load_mappings():
    """Load code mappings from Excel or create new ones"""
    path = "data/code_mappings.xlsx"
    if os.path.exists(path):
        mappings = pd.read_excel(path, sheet_name=None)  # returns dict of DataFrames
    else:
        mappings = {
            "Brand": pd.DataFrame(columns=["Brand", "Code"]),
            "Model": pd.DataFrame(columns=["Model", "Code"]),
            "Color": pd.DataFrame(columns=["Color", "Code"])
        }
    return mappings



def get_or_assign_code(value, df, prefix):
    """Get code if exists, else assign new one and update df"""

    if value in df.iloc[:, 0].values:
        code = df.loc[df.iloc[:, 0] == value, "Code"].values[0]
        return code, df   # <-- Always return 2 values
    else:
        # Auto-generate new code
        if df.empty:
            next_num = 1
        else:
            last_code = df["Code"].iloc[-1]
            last_num = int(last_code[1:])  # remove prefix
            next_num = last_num + 1

        new_code = f"{prefix}{next_num:02d}"
        new_row = pd.DataFrame({df.columns[0]: [value], "Code": [new_code]})
        df = pd.concat([df, new_row], ignore_index=True)
        return new_code, df   # <-- Also return 2 values