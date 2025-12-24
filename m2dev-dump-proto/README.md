# DumpProto


For x32 and x64 Windows environments.

Uses LZO 2.10.

Compatible with latest Windows 10 SDK Platform, C++ 20, C 17.


**No need for external includes/lib folder or vcpkg!**



## How to build
```
cd <cloned_repo_root_directory>
```

```
cmake -S . -B build
```

For x64
```
cmake --build build --config <Debug|MinSizeRel|Release|RelWithDebInfo> --target dump_proto
```

For x32
```
cmake --build build --config <Debug|MinSizeRel|Release|RelWithDebInfo> --target dump_proto -A Win32
```

## 🚀 Changelog: Build & Development Tools

### ✨ Major Feature: One-Click Multi-Locale Proto Compilation

We have dramatically simplified the process for building and deploying item and mob prototypes (protos) across multiple language locales.

| Feature | Old Method | **New Method (One-Click-for-All)** |
| :--- | :--- | :--- |
| **One-run limit** | Running only once for every pair (one names + proto for item, one names + proto for mob). | **One-run all-done**: all locales, in their directories, no renaming, one copy away from your packs! |

#### ⚙️ How It Works:

1.  Place the `dump_proto.exe` compiler and all required source files into the **same working directory ($\text{cwd}$)**.
	* *Required Source Files:* `item_names.txt + item_proto.txt` to produce `item_proto`, `mob_names.txt + mob_proto.txt` to produce mob_proto, and any custom locale files (e.g., `item_names_ru.txt`, `mob_names_cz.txt`).
	* *`item_proto.txt` + any `item_names(_XX).txt` is required* to compile the `item_proto` for the target locale (or default)
	* *`mob_proto.txt` + any `mob_names(_XX).txt` is required* to compile the `mob_proto` for the target locale (or default)

2.  Run the compiler **once**.

#### 🎯 Output Structure (Automatic):

The compiler now intelligently generates all required files in their final destinations:

**EXAMPLE:** `item_names.txt`, `item_proto.txt`, `item_names_ru.txt`, `mob_names.txt`, `mob_proto.txt` and `mob_names_cz.txt` in the same directory as `dump_proto.exe` can generate in one click:
* **Base (Current Working Directory):**
	* `item_proto` (Compiled base proto)
	* `mob_proto` (Compiled base proto)
* **Locale-Specific Directories:**
	* `<cwd>/locale_cz/locale/cz/mob_proto` (Compiled mob proto for Czech locale)
	* `<cwd>/locale_ru/locale/ru/item_proto` (Compiled item proto for Russian locale)

This change is designed to eliminate tedious manual steps and ensures consistency across all supported languages.

