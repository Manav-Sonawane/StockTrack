import os

from excel_handler import load_excel, backup_excel
from generator import generate_barcodes
from config import NEW_STOCK_FILE, MASTER_FILE

def main():
    stock_backup = backup_excel(NEW_STOCK_FILE, backup_type="stock")
    print(f"📦 Stock backup created at: {stock_backup}")

    master_backup = backup_excel(MASTER_FILE, backup_type="master")
    print(f"💾 Master backup created at: {master_backup}")

    df = load_excel(NEW_STOCK_FILE)
    print(f"Loaded {len(df)} items from Excel.")

    generate_barcodes(df)

    if os.path.exists(NEW_STOCK_FILE):
        os.remove(NEW_STOCK_FILE)
        print("🗑️ Removed new_stock.xlsx after processing")


if __name__ == "__main__":
    main()
