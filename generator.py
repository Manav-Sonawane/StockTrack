from barcode import Code128
from barcode.writer import ImageWriter

from utils import (
    load_mappings,
    save_mappings,
    get_or_assign_code,
    merge_to_master,
)


def generate_barcodes(df):
    """
    Merge new stock into master, auto-assign UIDs if missing,
    then generate barcodes for each item and save them.
    """

    # Merge stock into master and update UIDs
    df = merge_to_master(df)   # ✅ ensures UIDs are filled

    # Load existing mappings
    mappings = load_mappings()
    brand_df, model_df, color_df = mappings["Brand"], mappings["Model"], mappings["Color"]

    for _, row in df.iterrows():
        uid = str(row["UID"]).strip()

        if not uid or uid.lower() == "nan":
            print(f"⚠️ Skipping row with invalid UID: {row.to_dict()}")
            continue

        # Assign or fetch codes
        brand_code, brand_df = get_or_assign_code(row["Brand"], brand_df, "B")
        model_code, model_df = get_or_assign_code(row["Model"], model_df, "M")
        color_code, color_df = get_or_assign_code(row["Color"], color_df, "C")

        # Barcode string
        barcode_data = f"{uid}-{brand_code}-{model_code}-{color_code}-S{row['Size']}"

        # Save barcode image
        filename = f"output/barcodes/{uid}.png"
        Code128(barcode_data, writer=ImageWriter()).save(filename)
        print(f"✅ Barcode generated: {filename} → {barcode_data}")

    # Save updated mappings
    save_mappings({"Brand": brand_df, "Model": model_df, "Color": color_df})
    print("💾 Mappings updated in data/code_mappings.xlsx")

    return df   # ✅ return updated DataFrame (with UIDs)
