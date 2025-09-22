import os
import pandas as pd
from config import MASTER_FILE, MAPPINGS_FILE
from excel_handler import backup_excel
# --- Code assignment utility ---
def get_or_assign_code(value: str, df: pd.DataFrame, prefix: str):
    """
    Get code if exists, else assign new one and update df.
    Ensures codes are sorted before generating the next code.
    """
    if value in df.iloc[:, 0].values:
        code = df.loc[df.iloc[:, 0] == value, "Code"].values[0]
        return code, df
    else:
        # Auto-generate new code
        if df.empty:
            next_num = 1
        else:
            # Sort codes to ensure last is the highest
            sorted_df = df.copy()
            sorted_df["num"] = sorted_df["Code"].str.extract(rf"{prefix}(\d+)").astype(float)
            sorted_df = sorted_df.sort_values("num")
            last_code = sorted_df["Code"].iloc[-1]
            last_num = int(last_code[1:])
            next_num = last_num + 1

        new_code = f"{prefix}{next_num:02d}"
        new_row = pd.DataFrame({df.columns[0]: [value], "Code": [new_code]})
        df = pd.concat([df, new_row], ignore_index=True)
        return new_code, df


# --- Utility functions for UID ---
def normalize_uid(uid: str) -> str:
    """
    Normalize UID to always be 4-digit padded.
    Example: SH1 -> SH0001, SH12 -> SH0012
    """
    import re
    match = re.match(r"SH(\d+)", uid)
    if not match:
        return uid
    num = int(match.group(1))
    return f"SH{num:04d}"

def generate_new_uid(master_df):
    """
    Generate the next UID based on the highest existing one in master.
    Format: SH0001, SH0002, ...
    """
    if master_df.empty:
        return "SH0001"

    # Extract numeric part of last UID
    existing_uids = master_df["UID"].dropna().astype(str)
    numeric_parts = [
        int(uid.replace("SH", "")) for uid in existing_uids if uid.startswith("SH")
    ]
    next_num = max(numeric_parts) + 1 if numeric_parts else 1
    return f"SH{next_num:04d}"


def merge_to_master(new_stock_df):
    master_columns = ["UID", "Brand", "Model", "Color", "Size", "Quantity"]

    # Backup master before updating
    if os.path.exists(MASTER_FILE):
        backup_excel(MASTER_FILE, backup_type="master")
        master_df = pd.read_excel(MASTER_FILE)
    else:
        master_df = pd.DataFrame(columns=master_columns)

    # 🔹 Assign UIDs if missing
    for idx, row in new_stock_df.iterrows():
        if pd.isna(row.get("UID")) or str(row["UID"]).strip().lower() in ["", "nan"]:
            new_uid = generate_new_uid(master_df)
            new_stock_df.at[idx, "UID"] = new_uid
            # also add to master_df so the next UID increments properly
            master_df.loc[len(master_df)] = [new_uid, row["Brand"], row["Model"], row["Color"], row["Size"], row["Quantity"]]
            print(f"✅ Assigned new UID {new_uid} to {row['Brand']} {row['Model']}")

    # Ensure only required columns
    new_stock_core = new_stock_df[master_columns]

    # Combine master + new stock
    combined = pd.concat([master_df, new_stock_core], ignore_index=True)

    # 🔹 Group by identifiers and sum quantities
    combined = (
        combined.groupby(["UID", "Brand", "Model", "Color", "Size"], as_index=False)
        .agg({"Quantity": "sum"})
    )

    # Save updated master
    combined.to_excel(MASTER_FILE, index=False)
    print(f"💾 Master inventory updated: {MASTER_FILE}")

    return combined




def save_mappings(mappings: dict) -> None:
    """
    Save all mapping DataFrames back into the mappings Excel file.
    Uses consistent sheet names: 'Brand', 'Model', 'Color'.
    """
    try:
        with pd.ExcelWriter(MAPPINGS_FILE, engine="openpyxl", mode="w") as writer:
            for sheet, df in mappings.items():
                df.to_excel(writer, sheet_name=sheet, index=False)
    except Exception as e:
        print(f"❌ Error saving mappings: {e}")


def load_mappings() -> dict:
    """
    Load code mappings from Excel or create new ones.
    Uses consistent sheet names: 'Brand', 'Model', 'Color'.
    """
    if os.path.exists(MAPPINGS_FILE):
        try:
            mappings = pd.read_excel(MAPPINGS_FILE, sheet_name=None)
        except Exception as e:
            print(f"❌ Error loading mappings: {e}")
            mappings = {}
    else:
        mappings = {
            "Brand": pd.DataFrame(columns=["Brand", "Code"]),
            "Model": pd.DataFrame(columns=["Model", "Code"]),
            "Color": pd.DataFrame(columns=["Color", "Code"])
        }
    return mappings