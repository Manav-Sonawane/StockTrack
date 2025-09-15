import os
import pandas as pd
import barcode
from barcode import Code128
from barcode.writer import ImageWriter

MAPPINGS_FILE = "data/code_mappings.xlsx"


# ------------------ Mapping Utilities ------------------


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




# ------------------ Barcode Generator ------------------

def generate_barcodes(df):
    # Load existing mappings
    mappings = load_mappings()
    brand_df, model_df, color_df = mappings["BrandCodes"], mappings["ModelCodes"], mappings["ColorCodes"]

    for _, row in df.iterrows():
        uid = row["UID"]

        # Assign codes (or fetch if already exists)
        brand_code, brand_df = get_or_assign_code(row["Brand"], brand_df, "B")
        model_code, model_df = get_or_assign_code(row["Model"], model_df, "M")
        color_code, color_df = get_or_assign_code(row["Color"], color_df, "C")

        # Short barcode string
        barcode_data = f"{uid}-{brand_code}-{model_code}-{color_code}-S{row['Size']}"

        # Save barcode image
        filename = f"output/barcodes/{uid}.png"
        Code128(barcode_data, writer=ImageWriter()).save(filename)
        print(f"✅ Barcode generated: {filename} → {barcode_data}")

    # 🔹 Save updated mappings back to Excel
    save_mappings({
        "Brand": brand_df,
        "Model": model_df,
        "Color": color_df
    })
    print("💾 Mappings updated in data/code_mappings.xlsx")


