
import re

def check_content():
    filepath = r"assets\locale_pt\locale\pt\locale_game.txt"
    try:
        with open(filepath, "r", encoding="cp1252") as f:
            content = f.read()
        
        # Check for PT-PT spelling "Protecção"
        if "Protecção" in content:
            print("FOUND: Protecção (PT-PT spelling)")
        
        if "activad" in content: # activado/activada
             print("FOUND: activado/a (PT-PT spelling)")

        if "Activo" in content:
             print("FOUND: Activo (PT-PT spelling)")

        # Check for UTF-8 artifacts (Mojibake)
        # Ã followed by anything common in mojibake
        # Ã§ = ç, Ã£ = ã, Ãª = ê, etc.
        # But in cp1252, Ã is \xc3. 
        if "Ã§" in content or "Ã£" in content:
            print("FOUND: Mojibake (UTF-8 interpreted as ANSI characters inside the file)")

        # Print the specific line for Protecção to show context
        for line in content.splitlines():
            if "Protecção" in line or "ProtecÃ§Ã£o" in line:
                print(f"LINE: {line}")
            if "PVP_MODE_PROTECT" in line:
                print(f"DEBUG_LINE: {line}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_content()
