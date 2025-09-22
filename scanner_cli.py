from decoder import update_stock

def main():
	print("=== Shoe Shop Inventory Scanner CLI ===")
	while True:
		try:
			action = input("Enter action (in/out/exit): ").strip().lower()
			if action == "exit":
				print("Exiting scanner.")
				break
			if action not in ("in", "out"):
				print("Invalid action. Please enter 'in', 'out', or 'exit'.")
				continue
			barcode = input("Scan barcode: ").strip()
			if not barcode:
				print("No barcode entered.")
				continue
			update_stock(barcode, action)
			print("✅ Stock updated successfully.\n")
		except Exception as e:
			print(f"❌ Error: {e}\n")

if __name__ == "__main__":
	main()
