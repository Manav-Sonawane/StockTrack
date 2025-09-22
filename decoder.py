import pandas as pd
import os
from excel_handler import backup_excel
from config import MASTER_FILE
from utils import normalize_uid

def parse_barcode(barcode_str: str):
    try:
        uid, brand_code, model_code, color_code, size_code = barcode_str.split('-')

        return {
            "UID": uid,
            "BrandCode": brand_code,
            "ModelCode": model_code,
            "ColorCode": color_code,
            "Size": size_code[1:],
        }

    except ValueError:
        raise ValueError(barcode_str)

def update_stock(barcode_str: str, action: str = "out"):

    parsed = parse_barcode(barcode_str)
    from utils import normalize_uid
    uid = normalize_uid(parsed["UID"])

    if not os.path.exists(MASTER_FILE):
        raise FileNotFoundError("Master file not found")

    backup_excel(MASTER_FILE, backup_type="master")

    df = pd.read_excel(MASTER_FILE)

    if uid not in df["UID"].values:
        raise ValueError(f"❌ UID {uid} not found in master inventory.")

    current_qty = int(df.loc[df["UID"] == uid, "Quantity"].values[0])

    if action == "out":
        if current_qty <= 0:
            raise ValueError(f"❌ No stock available for {uid}.")
        df.loc[df["UID"] == uid, "Quantity"] = current_qty - 1
        print(f"📦 Stock OUT → {uid}: {current_qty} → {current_qty - 1}")

    elif action == "in":
        df.loc[df["UID"] == uid, "Quantity"] = current_qty + 1
        print(f"📥 Stock IN → {uid}: {current_qty} → {current_qty + 1}")

    else:
        raise ValueError(f"❌ '{action}' is not a valid action (use 'in' or 'out').")

    df.to_excel(MASTER_FILE, index=False)
    print(f"💾 Master inventory updated: {MASTER_FILE}")