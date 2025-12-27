
import os

filepath = r"g:\metin2-files-clean-64\M2-Dev\m2dev-server\channels\auth\syserr.log"
if os.path.exists(filepath):
    with open(filepath, "rb") as f:
        f.seek(0, 2)
        size = f.tell()
        f.seek(max(0, size - 4000))
        content = f.read().decode('utf-8', errors='ignore')
        print(content)
else:
    print("File not found")
