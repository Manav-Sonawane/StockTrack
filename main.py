from excel_handler import load_excel, backup_excel
from generator import generate_barcodes

EXCEL_FILE = "data/new_stock.xlsx"

def main():
    backup_file = backup_excel(EXCEL_FILE)
    print(f"Backup created at: {backup_file}")

    df = load_excel(EXCEL_FILE)
    print(f"Loaded {len(df)} items from Excel.")

    generate_barcodes(df)

if __name__ == "__main__":
    main()
