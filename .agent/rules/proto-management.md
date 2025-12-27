# Metin2 Item Proto Management

This document describes the workflow for updating, compiling, and deploying Item Prototypes (`item_proto`) for both the Server and the Client.

## Summary
The Item Proto defines the properties of all items in the game.
- **Server**: Reads `item_proto.txt` (text format).
- **Client**: Reads `item_proto` (binary format), packed inside `locale_xx.pck`.

**CRITICAL**: Modifications must be made on the Server text file first, then compiled into a binary for the Client, keeping them in sync.

## Workflow

### 1. Update Server Side (Source of Truth)
Edit the text file on the server.
- **File**: `m2dev-server/share/conf/item_proto.txt`
- **Format**: Tab-separated values.
- **Action**: Modify logic (Type, Flags, Wear, Limits, ApplyTypes).

**Example: Enabling a Stone**
```text
Original: 28532	Stone+5	ITEM_NONE	0	1	NONE	NONE	NONE	...
New:	  28532	Stone+5	ITEM_METIN	METIN_NORMAL	1	NONE	NONE	WEAR_WEAPON	...
```

*Note: You likely also need to update `m2dev-server/channels/db/conf/item_proto.txt` if using separate configs, or ensure symlinks are correct.*

### 2. Compile DumpProto (Tooling)
To generate the client binary, you need `dump_proto.exe`.
- **Source**: `m2dev-dump-proto/`
- **Dependencies**: CMake, Visual Studio (MSVC), LZO.
- **Build Command**:
  ```powershell
  cd m2dev-dump-proto
  cmake -S . -B build
  cmake --build build --config Release --target dump_proto
  ```
- **Output**: `m2dev-dump-proto/build/dump_proto/Release/dump_proto.exe`

### 3. Generate Client Binary
The `dump_proto` tool converts text config -> binary.
1.  Copy `item_proto.txt` and `item_names.txt` from Server (`share/conf/`) to the folder with `dump_proto.exe`.
2.  Run `dump_proto.exe`.
3.  **Output**: `item_proto` (Binary file).

### 4. Deploy to Client (Patching)
1.  Copy the generated `item_proto` binary to your locale folder:
    - Path: `m2dev-client/assets/locale_<lang>/locale/<lang>/item_proto`
2.  **Repack** the locale:
    - Tool: `PackMaker.exe` (located in `assets/`).
    - Command:
      ```powershell
      cd m2dev-client/assets
      ./PackMaker.exe --input locale_<lang> --output ../pack
      ```
      *(Replace `<lang>` with `pt`, `en`, etc.)*

### 5. Finalize
- **Server**: Reload via `/reload p` or reboot.
- **Client**: Restart the game to load the new `.pck` files.

## Troubleshooting
- **Item not equipping?** Client likely thinks it is `ITEM_NONE`. Check if `item_proto` was actually updated in the client pack.
- **Names missing?** Verify `item_names.txt` is in sync and compiled into `item_proto` (modern DumpProto handles names internally).
