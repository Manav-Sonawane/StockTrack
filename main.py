import os
from excel_handler import load_excel, backup_excel
from generator import generate_barcodes
from decoder import parse_barcode, update_stock
from config import NEW_STOCK_FILE, MASTER_FILE


def main():
    # Backup both stock and master before processing
    backup_excel(NEW_STOCK_FILE, backup_type="stock")
    backup_excel(MASTER_FILE, backup_type="master")

    # Load new stock
    df = load_excel(NEW_STOCK_FILE)
    print(f"Loaded {len(df)} items from Excel.")

    # Generate barcodes and update master
    df = generate_barcodes(df)

    # Remove new stock file after processing
    if os.path.exists(NEW_STOCK_FILE):
        os.remove(NEW_STOCK_FILE)
        print("🗑️ Removed new_stock.xlsx after processing")

    # 🔹 Demo: parse and update stock using actual UIDs
    for idx, row in df.iterrows():
        uid = row["UID"]
        size = row["Size"]

        # Build a sample barcode string from actual codes
        test_code = f"{uid}-B01-M01-C01-S{size}"  # demo purposes only
        parsed = parse_barcode(test_code)
        print("🔎 Parsed:", parsed)

        # Try stock update
        try:
            update_stock(test_code, action="out")
            print(f"📉 Stock updated OUT for {uid}")
        except Exception as e:
            print("⚠️ Error during update:", e)


if __name__ == "__main__":
    main()
