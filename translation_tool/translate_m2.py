import os
import time
import re
import argparse
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from tqdm import tqdm

# Load environment variables
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY or API_KEY == "YOUR_API_KEY_HERE":
    print("❌ Error: GEMINI_API_KEY not found in .env file.")
    exit(1)

genai.configure(api_key=API_KEY)

MODEL_NAME = os.getenv("MODEL_NAME", "gemini-2.0-flash")
TARGET_LANG = os.getenv("TARGET_LANG", "pt-BR")
DELAY = float(os.getenv("REQUEST_DELAY", 4.0))

print(f"🔧 Configuration: Model={MODEL_NAME}, Target={TARGET_LANG}, Delay={DELAY}s")

model = genai.GenerativeModel(MODEL_NAME)


# --- Context & Glossary ---
GLOSSARY = """
Mandatory Metin2 PT-BR Terminology (Localização Brasil):
- Skill Damage -> Dano de Habilidade
- Average Damage -> Dano Médio
- Mob -> Monstro
- Drop -> Drop
- Metin -> Metin
- Upgrade -> Refinação/Melhoria
- Blacksmith -> Ferreiro
- Guild -> Guilda
- Party -> Grupo
- GM -> GM
- Yang -> Yang
- Won -> Won
- Level -> Nível
- EXP -> EXP
- HP -> HP
- SP -> SP
- Archer -> Arqueiro
- Warrior -> Guerreiro
- Sura -> Sura
- Shaman -> Shaman
- Assassin -> Ninja (assassin category in Metin2 BR is "Ninja")

PT-PT to PT-BR Localisation rules:
- Fato -> Traje/Terno
- Fato de Casamento -> Terno de Casamento
- Cana de pesca -> Vara de Pesca
- Pinças -> Alicate
- Rapaz -> Garoto/Jovem
- Autocarro -> Ônibus
- Ecrã -> Tela
- Equipamento -> Equipamento
- Shaman -> Shaman
- "Podes" -> "Pode/Você pode"
- "Fazes" -> "Faz/Você faz"
- "Tens" -> "Tem/Você tem"
"""

SYSTEM_PROMPT = f"""
You are an expert localizer for Metin2 BR.
Translate the following strings from English/PT-PT to PT-BR.

{GLOSSARY}

Rules:
1. Use strictly the PT-BR terms (localização brasileira).
2. NO "tu", "podes", "fazes". Use "você".
3. Preserve variables like %s, %d, %x, %.2f, %u.
4. Preserve newlines: [ENTER], \\n.
5. Preserve color tags: |cffff0000, |h, |r.
6. Output ONLY the translated text inside the ID blocks.
"""

def translate_batch(texts, pbar=None):
    if not texts: return []
    
    joined_text = ""
    for i, text in enumerate(texts):
        joined_text += f"ID:{i} {{{text}}}\n"
        
    prompt = f"{SYSTEM_PROMPT}\n\nTranslate these lines:\n{joined_text}"
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = model.generate_content(prompt)
            if not response.candidates:
                print(f"⚠️ No candidates in response (blocked?). Skipping batch.")
                return texts
                
            result_text = response.text
            
            translated_map = {}
            # Greedy regex to catch content between brackets even if multiline
            matches = re.findall(r"ID:(\d+)\s+{(.*?)}", result_text, re.DOTALL)
            for idx_str, content in matches:
                translated_map[int(idx_str)] = content.strip()
            
            # Fallback for simple ID lines if brackets fail
            if len(translated_map) < len(texts):
                for line in result_text.split('\n'):
                    m = re.match(r"ID:(\d+)\s+(.*)", line.strip())
                    if m:
                        idx = int(m.group(1))
                        if idx not in translated_map:
                            translated_map[idx] = m.group(2).strip()

            final_list = []
            for i in range(len(texts)):
                val = translated_map.get(i, texts[i])
                # Clean any lingering artifacts
                val = val.strip('{}')
                final_list.append(val)
                
            time.sleep(DELAY)
            return final_list

        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Rate limit. Waiting 20s...")
                time.sleep(20)
                continue
            if "safety" in str(e).lower():
                print(f"⚠️ Safety block triggered. Returning originals for this batch.")
                return texts
            print(f"❌ Error during translation: {e}")
            return texts
    return texts

def process_file_kv(input_path, output_path):
    """
    Handles Metin2 Key-Value files with precise column detection.
    Supports:
    - VNUM <tab> NAME <tab> DESCRIPTION
    - "KEY" <tab> "VALUE"
    """
    print(f"📂 Processing KV File: {input_path}")
    
    encodings = ['cp1252', 'utf-8', 'ansi']
    lines = []
    enc_used = 'cp1252'
    for e in encodings:
        try:
            with open(input_path, 'r', encoding=e) as f:
                lines = f.readlines()
                enc_used = e
                break
        except: continue

    if not lines: return

    processed_lines = []
    batch_texts = []
    batch_map = [] # List of tuples: (line_idx, part_idx)

    BATCH_SIZE = 80

    def flush_batch():
        if not batch_texts: return
        translations = translate_batch(batch_texts)
        for t_text, (line_idx, part_idx) in zip(translations, batch_map):
            processed_lines[line_idx][part_idx] = t_text
        batch_texts.clear()
        batch_map.clear()

    for i, line in enumerate(tqdm(lines, desc="Parsing Structure")):
        line_raw = line.rstrip('\n\r')
        if not line_raw.strip() or line_raw.startswith(('#', '//')):
            processed_lines.append(line_raw)
            continue

        # Split by any whitespace but preserve the actual gaps? 
        # Better: split by TAB to preserve column structure of itemdesc/skilldesc
        parts = line_raw.split('\t')
        line_struct = []
        
        for p_idx, part in enumerate(parts):
            # Logic: Translate if it looks like text (not just numbers/IDs)
            strip_part = part.strip('" ')
            is_text = any(c.isalpha() for c in strip_part) 
            # and not is a single short identifier or UI path
            is_valid = is_text and len(strip_part) > 1 and not (strip_part.startswith('ui/') or strip_part.endswith('.sub'))

            if is_valid:
                batch_texts.append(strip_part)
                batch_map.append((len(processed_lines), p_idx))
                line_struct.append(part) # Store original for now
            else:
                line_struct.append(part)

        processed_lines.append(line_struct)
        if len(batch_texts) >= BATCH_SIZE:
            flush_batch()

    flush_batch()

    # Reconstruct
    final_output = []
    for line in processed_lines:
        if isinstance(line, list):
            final_output.append('\t'.join(line))
        else:
            final_output.append(line)

    with open(output_path, 'w', encoding=enc_used) as f:
        f.write('\n'.join(final_output))
    print(f"✅ Saved: {output_path}")

def process_lua(input_path, output_path):
    # Reuse base logic but slightly simplified for Lua strings
    print(f"📂 Processing Lua: {input_path}")
    with open(input_path, 'r', encoding='utf-8', errors='replace') as f:
        lines = f.readlines()

    new_lines = []
    batch_values = []
    batch_indices = []

    for i, line in enumerate(tqdm(lines, desc="Scanning Lua")):
        # Simple match for strings in quotes
        matches = re.finditer(r'["\'](.*?)["\']', line)
        temp_line = line
        
        # We only translate if it looks like real sentences/words
        for m in matches:
            content = m.group(1)
            if len(content) > 3 and any(c.isalpha() for c in content) and "gameforge." not in content:
                batch_values.append(content)
                batch_indices.append((len(new_lines), content))
        
        new_lines.append(line)
        
        if len(batch_values) >= 20:
            translated = translate_batch(batch_values)
            for t_text, (l_idx, orig_text) in zip(translated, batch_indices):
                # Replace the exact sequence with quotes to avoid partial matches
                # Warning: This is a bit unsafe if same quote text appears multiple times differently
                new_lines[l_idx] = new_lines[l_idx].replace(f'"{orig_text}"', f'"{t_text}"').replace(f"'{orig_text}'", f"'{t_text}'")
            batch_values.clear()
            batch_indices.clear()

    # Flush remaining
    if batch_values:
        translated = translate_batch(batch_values)
        for t_text, (l_idx, orig_text) in zip(translated, batch_indices):
            new_lines[l_idx] = new_lines[l_idx].replace(f'"{orig_text}"', f'"{t_text}"').replace(f"'{orig_text}'", f"'{t_text}'")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print(f"✅ Saved: {output_path}")

def process_locale_string(input_path, output_path):
    print(f"📂 Processing locale_string: {input_path}")
    with open(input_path, 'r', encoding='cp1252', errors='replace') as f:
        lines = f.readlines()
        
    new_lines = []
    batch_texts = []
    batch_indices = []
    
    is_key = True
    for i, line in enumerate(tqdm(lines)):
        m = re.match(r'^"(.*)";$', line.strip())
        if m:
            if is_key:
                new_lines.append(line)
                is_key = False
            else:
                val = m.group(1)
                batch_texts.append(val)
                batch_indices.append(len(new_lines))
                new_lines.append(line)
                is_key = True
        else:
            new_lines.append(line)
            if not line.strip(): is_key = True

        if len(batch_texts) >= 30:
            ts = translate_batch(batch_texts)
            for t, idx in zip(ts, batch_indices):
                new_lines[idx] = f'"{t}";\n'
            batch_texts.clear()
            batch_indices.clear()

    if batch_texts:
        ts = translate_batch(batch_texts)
        for t, idx in zip(ts, batch_indices):
            new_lines[idx] = f'"{t}";\n'

    with open(output_path, 'w', encoding='cp1252') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", required=True)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    if args.mode == "kv" or args.mode == "plain": # merge plain into kv for simplicity
        process_file_kv(args.input, args.output)
    elif args.mode == "lua":
        process_lua(args.input, args.output)
    elif args.mode == "string":
        process_locale_string(args.input, args.output)
