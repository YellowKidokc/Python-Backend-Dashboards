
import shutil
import pathlib

# --- CONFIGURATION ---

# The root directory of the vault
ROOT_DIR = pathlib.Path(r"D:\\THEOPHYSICS_MASTER")

# The destination for all old files and folders
ARCHIVE_DIR = ROOT_DIR / "ARCHIVE"


# --- Items to be ARCHIVED ---
# These folders and files will be moved into the ARCHIVE directory.
# The script will skip any items that don't exist.
ITEMS_TO_ARCHIVE = [
    # Old Structure Folders
    "00_System", "01_Assets", "02_Foundations", "03_Analysis", "04_Integration",
    "05_Doctrine", "09_Tools", "10_Core-Theory", "30_Theophysics", "40_Apologetics",
    "50_Resources", "70_Projects", "80 Tags", "81_Hubs_and_MOCs", "82_Dashboards",
    "83_Templates", "84_Wizards", "Glossary", "Papers", ".trash",
    
    # Redundant Publication Folders (we keep '06_Publication/Logos_Papers')
    "06_Publication/Copy Logos Papers", "06_Publication/Family", "06_Publication/Logos Paper",
    "06_Publication/References",
    
    # Loose Root Files (excluding essential/new files)
    "ANSWER_DO_WE_NEED_MORE_PICS.txt", "AUDIT_COMPLETE_EXECUTIVE_SUMMARY.txt",
    "DESKTOP_LOGOS_FOLDERS_IMAGE_AUDIT.md", "DESKTOP_VS_ORGANIZED_COMPARISON.md",
    "FINAL_VERIFICATION_REPORT.txt", "IMAGES_COMPLETE_SUMMARY.md", "IMAGES_NEEDED_FINAL_LIST.md",
    "Many-Worlds.md", "Master_Index.md", "MASTER_LOGOS_PAPERS_CATALOG.yaml",
    "Neural-Correlates.md", "Paper 2 - The Quantum Bridge.md", "Paper-5-Resurrection.md",
    "Quantum-To-Classical.md", "Quantum-Zeno-Effect.md", "SHORTFALL_LIST_FOR_CREATION.txt",
    "Split-Brain.md", "STRUCTURE.md", "TASK_COMPLETE_SUMMARY.txt", "The Coherence Factor.md",
    "Untitled.base", "Untitled.canvas",
    
    # Loose files from 06_Publication
    "06_Publication/00_Gemini_Critical_Analysis.md", "06_Publication/00-Series-Index.md",
    "06_Publication/LOGOS_PAPERS_COMPLETE_SUMMARY.md", "06_Publication/PAPERS_FORMATTING_PROGRESS.md"
]


# --- Helper Function ---

def safe_move(src_path, dest_dir):
    """Moves a file or directory into the destination directory. Skips if source doesn't exist."""
    try:
        if not src_path.exists():
            print(f"SKIPPED: Source '{src_path.name}' not found.")
            return
        
        # Ensure destination exists
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        # Construct final destination path
        final_dest_path = dest_dir / src_path.name
        
        # If a file/folder with the same name exists, add a suffix to avoid overwriting
        counter = 1
        while final_dest_path.exists():
            final_dest_path = dest_dir / f"{src_path.stem}_{counter}{src_path.suffix}"
            counter += 1
            if counter > 50: # Safety break
                print(f"ERROR: Could not find a unique name for '{src_path.name}' in archive. Aborting move.")
                return

        shutil.move(str(src_path), str(final_dest_path))
        print(f"ARCHIVED: '{src_path.name}' -> '{final_dest_path.relative_to(ROOT_DIR)}'")

    except Exception as e:
        print(f"ERROR moving '{src_path.name}': {e}")


# --- Main Cleanup Logic ---

def main():
    print(f"--- Starting Vault Cleanup ---")
    print(f"All specified items will be moved to: '{ARCHIVE_DIR}'")
    
    # Create the ARCHIVE directory if it doesn't exist
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)

    # Archive all specified items
    for item_name in ITEMS_TO_ARCHIVE:
        src_path = ROOT_DIR / item_name
        safe_move(src_path, ARCHIVE_DIR)

    print("\n--- Cleanup Script Finished ---")
    print("Please review the vault structure.")

if __name__ == "__main__":
    # This script is intended to be run from the command line.
    # Example: python cleanup_folders.py
    confirm = input(f"This script will archive many files and folders into '{ARCHIVE_DIR.name}'.\nThis action is reversible but significant. Are you sure you want to continue? (yes/no): ")
    if confirm.lower() == 'yes':
        main()
    else:
        print("Operation cancelled by user.")
