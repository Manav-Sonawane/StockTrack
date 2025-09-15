import os

from excel_handler import load_excel, backup_excel
from generator import generate_barcodes
from config import NEW_STOCK_FILE

def main():
    backup_file = backup_excel(NEW_STOCK_FILE)
    print(f"Backup created at: {backup_file}")

    df = load_excel(NEW_STOCK_FILE)
    print(f"Loaded {len(df)} items from Excel.")

    generate_barcodes(df)

    os.remove(NEW_STOCK_FILE)

if __name__ == "__main__":
    main()
