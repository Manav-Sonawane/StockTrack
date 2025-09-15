import pandas as pd
import os
from datetime import datetime
import shutil

def load_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def backup_excel(file_path: str, backup_dir: str = "backups"):
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(backup_dir, f"{os.path.basename(file_path).split('.')[0]}_{timestamp}.xlsx")
    shutil.copy(file_path, backup_file)
    return backup_file