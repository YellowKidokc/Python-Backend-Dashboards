"""
THEOPHYSICS Word Ontology - Command Line Interface
Interactive menu for managing the semantic ontology system.
"""

import os
import sys
from pathlib import Path

# Add Scripts to path
SCRIPTS_DIR = Path(__file__).parent / "Scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from validate_term import validate_term, format_output

ONTOLOGY_ROOT = Path(__file__).parent
TERMS_DIR = ONTOLOGY_ROOT / "Terms"
TEMPLATE = ONTOLOGY_ROOT / "Templates" / "new-term-template.md"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("=" * 70)
    print("THEOPHYSICS WORD ONTOLOGY SYSTEM")
    print("Semantic Bridge Builder v1.0")
    print("=" * 70)
    print()

def main_menu():
    while True:
        clear_screen()
        print_header()
        print("MAIN MENU:")
        print()
        print("1. Validate a new term")
        print("2. Create term file from template")
        print("3. List all terms")
        print("4. Search papers for old terminology")
        print("5. View system status")
        print()
        print("0. Exit")
        print()
        
        choice = input("Enter choice: ").strip()
        
        if choice == "1":
            validate_term_interactive()
        elif choice == "2":
            create_term_file()
        elif choice == "3":
            list_terms()
        elif choice == "4":
            search_papers()
        elif choice == "5":
            system_status()
        elif choice == "0":
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Press Enter to continue...")
            input()

def validate_term_interactive():
    clear_screen()
    print_header()
    print("TERM VALIDATION")
    print("=" * 70)
    print()
    
    term_name = input("Enter term name: ").strip()
    if not term_name:
        print("\nNo term name provided.")
        input("Press Enter to continue...")
        return
    
    print("\nEnter definition (multi-line, empty line to finish):")
    definition_lines = []
    while True:
        line = input()
        if not line:
            break
        definition_lines.append(line)
    
    definition = " ".join(definition_lines)
    
    if not definition:
        print("\nNo definition provided.")
        input("Press Enter to continue...")
        return
    
    source_words_str = input("\nEnter source words (comma-separated): ").strip()
    if not source_words_str:
        print("\nNo source words provided.")
        input("Press Enter to continue...")
        return
    
    source_words = [s.strip() for s in source_words_str.split(',')]
    
    print("\nValidating...")
    result = validate_term(definition, source_words)
    
    print("\n" + format_output(result, definition, source_words))
    
    if result['status'] == "APPROVED":
        create_file = input("\nCreate term file? (y/n): ").strip().lower()
        if create_file == 'y':
            create_term_file_with_data(term_name, definition, source_words, result)
    
    input("\nPress Enter to continue...")

def create_term_file():
    clear_screen()
    print_header()
    print("CREATE TERM FILE")
    print("=" * 70)
    print()
    
    term_name = input("Enter term name (e.g., 'Primordial-Actualization'): ").strip()
    if not term_name:
        print("\nNo term name provided.")
        input("Press Enter to continue...")
        return
    
    # Get next available number
    existing = list(TERMS_DIR.glob("*.md"))
    if existing:
        numbers = []
        for f in existing:
            name = f.stem
            if '-' in name:
                num_part = name.split('-')[0]
                if num_part.isdigit():
                    numbers.append(int(num_part))
        next_num = max(numbers) + 1 if numbers else 1
    else:
        next_num = 1
    
    filename = f"{next_num:02d}-{term_name}.md"
    filepath = TERMS_DIR / filename
    
    if filepath.exists():
        overwrite = input(f"\n{filename} already exists. Overwrite? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("\nCancelled.")
            input("Press Enter to continue...")
            return
    
    # Copy template
    try:
        with open(TEMPLATE, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # Replace {{NEW_TERM}} with actual term name
        content = template_content.replace("{{NEW_TERM}}", term_name)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ Created: {filename}")
        print(f"Location: {filepath}")
        print("\nNow edit the file to fill in all sections.")
        
    except Exception as e:
        print(f"\n❌ Error creating file: {e}")
    
    input("\nPress Enter to continue...")

def create_term_file_with_data(term_name, definition, source_words, validation_result):
    """Create term file with validation data pre-filled."""
    existing = list(TERMS_DIR.glob("*.md"))
    numbers = []
    for f in existing:
        name = f.stem
        if '-' in name:
            num_part = name.split('-')[0]
            if num_part.isdigit():
                numbers.append(int(num_part))
    next_num = max(numbers) + 1 if numbers else 1
    
    filename = f"{next_num:02d}-{term_name}.md"
    filepath = TERMS_DIR / filename
    
    # Read template
    with open(TEMPLATE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace placeholders
    content = content.replace("{{NEW_TERM}}", term_name)
    content = content.replace("{{0.XX}}", f"{validation_result['similarity']:.2f}")
    content = content.replace("{{XX}}%", validation_result['percentage'])
    
    # Add source words
    source_list = "\n".join([f"- {word}" for word in source_words])
    content = content.replace("```\n- {{source_word_1}}\n- {{source_word_2}}\n- {{source_word_3}}\n```", 
                            f"```\n{source_list}\n```")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n✅ Created: {filename}")
    print(f"Location: {filepath}")

def list_terms():
    clear_screen()
    print_header()
    print("ALL TERMS")
    print("=" * 70)
    print()
    
    terms = sorted(TERMS_DIR.glob("*.md"))
    if not terms:
        print("No terms found.")
    else:
        for term_file in terms:
            print(f"  • {term_file.name}")
    
    print(f"\nTotal: {len(terms)} terms")
    print()
    input("Press Enter to continue...")

def search_papers():
    clear_screen()
    print_header()
    print("SEARCH PAPERS FOR OLD TERMINOLOGY")
    print("=" * 70)
    print()
    print("This feature will be implemented soon.")
    print()
    print("Planned functionality:")
    print("  - Scan all .md files in Papers directory")
    print("  - Find instances of old terminology")
    print("  - Suggest replacements")
    print("  - Generate replacement report")
    print()
    input("Press Enter to continue...")

def system_status():
    clear_screen()
    print_header()
    print("SYSTEM STATUS")
    print("=" * 70)
    print()
    
    # Count terms
    terms = list(TERMS_DIR.glob("*.md"))
    validated_count = len(terms)
    total_terms = 14
    
    print(f"Terms Created:    {validated_count}/{total_terms} ({validated_count/total_terms*100:.0f}%)")
    print(f"Terms Remaining:  {total_terms - validated_count}")
    print()
    
    if terms:
        print("Validated Terms:")
        for term_file in sorted(terms):
            print(f"  ✅ {term_file.stem}")
    
    print()
    print("Status: " + ("✅ OPERATIONAL" if validated_count > 0 else "⚠️  SETUP NEEDED"))
    print()
    input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        sys.exit(0)
