import os
import subprocess
import shutil

# Paths
CLIENT_LOCALE_DIR = r"g:\metin2-files-clean-64\M2-Dev\m2dev-client\assets\locale_pt\locale\pt"
SERVER_LOCALE_DIR = r"g:\metin2-files-clean-64\M2-Dev\m2dev-server\share\locale\english"
TOOL_PATH = r"g:\metin2-files-clean-64\M2-Dev\translation_tool\translate_m2.py"

# Files to translate (Mode, Input, Output)
TASKS = [
    # Client Files (KV mode with TAB awareness)
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "locale_game.txt"), os.path.join(CLIENT_LOCALE_DIR, "locale_game.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "locale_interface.txt"), os.path.join(CLIENT_LOCALE_DIR, "locale_interface.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "itemdesc.txt"), os.path.join(CLIENT_LOCALE_DIR, "itemdesc.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "skilldesc.txt"), os.path.join(CLIENT_LOCALE_DIR, "skilldesc.txt")),
    
    # Descriptions (Plain mode)

    ("kv", os.path.join(CLIENT_LOCALE_DIR, "empiredesc_a.txt"), os.path.join(CLIENT_LOCALE_DIR, "empiredesc_a.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "empiredesc_b.txt"), os.path.join(CLIENT_LOCALE_DIR, "empiredesc_b.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "empiredesc_c.txt"), os.path.join(CLIENT_LOCALE_DIR, "empiredesc_c.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "jobdesc_warrior.txt"), os.path.join(CLIENT_LOCALE_DIR, "jobdesc_warrior.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "jobdesc_assassin.txt"), os.path.join(CLIENT_LOCALE_DIR, "jobdesc_assassin.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "jobdesc_sura.txt"), os.path.join(CLIENT_LOCALE_DIR, "jobdesc_sura.txt")),
    ("kv", os.path.join(CLIENT_LOCALE_DIR, "jobdesc_shaman.txt"), os.path.join(CLIENT_LOCALE_DIR, "jobdesc_shaman.txt")),
    
    # Server Files
    ("string", os.path.join(SERVER_LOCALE_DIR, "locale_string.txt"), os.path.join(SERVER_LOCALE_DIR, "locale_string.txt")),
    ("lua", os.path.join(SERVER_LOCALE_DIR, "translate.lua"), os.path.join(SERVER_LOCALE_DIR, "translate.lua")),
]

def run_translation():
    print("🚀 Starting Global Translation (PT-PT/EN -> PT-BR) 🚀")
    print("=====================================================")
    
    for mode, input_file, output_file in TASKS:
        if not os.path.exists(input_file):
            print(f"⏩ Skipping {os.path.basename(input_file)} (Not found)")
            continue
            
        # Marker for "Already Done"
        done_marker = input_file + ".done"
        if os.path.exists(done_marker):
            print(f"✅ Skipping {os.path.basename(input_file)} (Already translated)")
            continue
            
        # Create backup if not exists
        bak_file = input_file + ".bak_pt"
        if not os.path.exists(bak_file):
            print(f"📦 Backup: {os.path.basename(bak_file)}")
            shutil.copy2(input_file, bak_file)
        
        print(f"\n✨ Translating: {os.path.basename(input_file)} (Mode: {mode})")
        # Use a temporary file for the translation process
        temp_output = output_file + ".tmp"
        
        cmd = ["py", TOOL_PATH, "--mode", mode, "--input", input_file, "--output", temp_output]
        
        try:
            subprocess.run(cmd, check=True)
            
            # Verify file size (should be roughly similar)
            if os.path.getsize(temp_output) > 10:
                os.replace(temp_output, output_file)
                # Create the "Done" marker
                with open(done_marker, "w") as f:
                    f.write("done")
                print(f"✅ Success: {os.path.basename(output_file)} is now PT-BR.")
            else:
                print(f"⚠️ Warning: Output for {os.path.basename(input_file)} seems empty. Aborting swap.")
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed: {os.path.basename(input_file)} error code {e.returncode}")
        except KeyboardInterrupt:
            print("\n🛑 Process interrupted by user. Cleaning up temp files...")
            if os.path.exists(temp_output): os.remove(temp_output)
            return

    print("\n🏁 Translation Complete! 🏁")

if __name__ == "__main__":
    run_translation()
