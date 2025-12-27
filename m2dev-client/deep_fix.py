import os

# Lista de arquivos para corrigir
files_to_fix = [
    r"assets\locale_pt\locale\pt\locale_game.txt",
    r"assets\locale_pt\locale\pt\locale_interface.txt",
    r"assets\root\uiscriptlocale.py"
]

# Mapeamento de possíveis corrupções de UTF-8 lidas como ANSI
def fix_double_encoding(text):
    replacements = {
        "Ã§": "ç", "Ã‡": "Ç",
        "Ã£": "ã", "Ãƒ": "Ã",
        "Ãµ": "õ", "Ã•": "Õ",
        "Ã¡": "á", "Ã": "Á",
        "Ã©": "é", "Ã‰": "É",
        "Ã-": "í", "Ã": "Í",
        "Ã³": "ó", "Ã“": "Ó",
        "Ãº": "ú", "Ãš": "Ú",
        "Ã¢": "â", "Ã‚": "Â",
        "Ãª": "ê", "ÃŠ": "Ê",
        "Ã´": "ô", "Ã”": "Ô",
        "Ã ": "à", "Ã€": "À",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def process_file(filepath):
    if not os.path.exists(filepath):
        print(f"Ignorando (não encontrado): {filepath}")
        return

    print(f"Processando: {filepath}")
    
    # Tenta ler como UTF-8 primeiro
    try:
        with open(filepath, "rb") as f:
            raw = f.read()
        
        # Tenta decodificar como UTF-8
        try:
            content = raw.decode("utf-8")
        except UnicodeDecodeError:
            # Se falhar, já está em ANSI/CP1252
            content = raw.decode("cp1252", errors="replace")
            
        # Corrigir textos que já podem estar salvos erroneamente como Ã§ etc.
        content = fix_double_encoding(content)
        
        # Adicionar/Forçar Tahoma no locale_game.txt
        if "locale_game.txt" in filepath:
            lines = content.splitlines()
            font_defs = [
                "UI_DEF_FONT\tTahoma:12",
                "UI_DEF_FONT_LARGE\tTahoma:14",
                "UI_DEF_FONT_SMALL\tTahoma:9"
            ]
            # Remove definições antigas de fonte
            lines = [l for l in lines if "UI_DEF_FONT" not in l]
            # Insere as novas no topo
            lines = font_defs + lines
            content = "\n".join(lines)

        # Salva como ANSI (CP1252)
        with open(filepath, "wb") as f:
            f.write(content.encode("cp1252", errors="replace"))
            
        print(f"OK: {filepath} corrigido e salvo em ANSI.")
    except Exception as e:
        print(f"Erro ao processar {filepath}: {e}")

if __name__ == "__main__":
    for f in files_to_fix:
        process_file(f)
