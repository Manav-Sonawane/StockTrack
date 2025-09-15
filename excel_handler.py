import pandas as pd
import os
from datetime import datetime
import shutil

def load_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def backup_excel(file_path: str, backup_type: str = "stock"):
    """
    Creates a timestamped backup of the given Excel file.
    backup_type = "stock" or "master" → decides folder.
    """
    base_dir = os.path.join("backups", backup_type)
    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(file_path).split(".")[0]
    backup_file = os.path.join(base_dir, f"{filename}_{timestamp}.xlsx")

    shutil.copy(file_path, backup_file)
    return backup_file
