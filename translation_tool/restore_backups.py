import os
import shutil
from pathlib import Path

# Common Paths
DIRS = [
    r"g:\metin2-files-clean-64\M2-Dev\m2dev-client\assets\locale_pt\locale\pt",
    r"g:\metin2-files-clean-64\M2-Dev\m2dev-server\share\locale\english"
]

def restore_backups():
    for d in DIRS:
        if not os.path.exists(d):
            continue
            
        print(f"📁 Checking directory: {d}")
        for file in os.listdir(d):
            if file.endswith(".bak_pt"):
                original_file = os.path.join(d, file.replace(".bak_pt", ""))
                backup_file = os.path.join(d, file)
                
                print(f"🔄 Restoring {file} -> {os.path.basename(original_file)}")
                shutil.copy2(backup_file, original_file)
                # Keep backup just in case, or delete? Let's keep for now.

if __name__ == "__main__":
    restore_backups()
