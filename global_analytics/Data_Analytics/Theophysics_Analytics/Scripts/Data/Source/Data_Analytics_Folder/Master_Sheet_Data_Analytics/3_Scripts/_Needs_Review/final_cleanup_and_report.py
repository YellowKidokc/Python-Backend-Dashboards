import re
from pathlib import Path

# Paths
ASSEMBLED_PATH = Path(r"C:\Users\Yellowkid\Desktop\Obisidan Final\THEOPHYSICS_MASTER\06_Publication\Logos_Papers\COMPLETE_LOGOS_PAPERS_FINAL\THEOPHYSICS_MASTER_PAPER_ASSEMBLED.md")

def clean_encoding_issues(text):
    """Remove Chinese characters and fix encoding issues"""
    original_len = len(text)
    
    # Remove Chinese characters
    text = re.sub(r'[\u4e00-\u9fff]', '', text)
    
    # Remove repeated question marks
    text = re.sub(r'[？]{3,}', '', text)
    
    # Fix common encoding issues - remove garbled characters
    # These are often encoding artifacts
    text = text.replace('脗', '')
    text = text.replace('脙', '')
    text = text.replace('脕', '')
    
    # Fix Greek letters that got corrupted
    text = text.replace('脧', 'χ')
    text = text.replace('脦', 'Φ')
    
    # Remove any remaining non-printable characters except newlines and tabs
    # Keep standard ASCII, extended ASCII, and common Unicode
    cleaned = []
    for char in text:
        if ord(char) < 32 and char not in '\n\r\t':
            continue
        if 0xE000 <= ord(char) <= 0xF8FF:  # Private use area
            continue
        cleaned.append(char)
    text = ''.join(cleaned)
    
    removed = original_len - len(text)
    return text, removed

def main():
    print("Reading assembled paper...")
    with open(ASSEMBLED_PATH, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    print(f"Original file size: {len(content):,} characters")
    
    print("\nCleaning encoding issues...")
    cleaned_content, removed = clean_encoding_issues(content)
    
    print(f"Removed {removed:,} problematic characters")
    print(f"Cleaned file size: {len(cleaned_content):,} characters")
    
    if removed > 0:
        print("\nWriting cleaned file...")
        with open(ASSEMBLED_PATH, 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        print("✓ File cleaned and saved!")
    else:
        print("\n✓ No encoding issues found - file is clean!")
    
    print("\n" + "="*60)
    print("SUMMARY:")
    print("="*60)
    print("The assembled paper has been checked and cleaned.")
    print("\nNote: Papers 4-10 in the individual files don't have")
    print("the standard sections (Hypotheses, Lexicon, Evidence,")
    print("Enigmas, References) in the same format as Papers 1-3.")
    print("They use different section names or don't include these sections.")
    print("\nTo add these sections, they would need to be created in")
    print("the individual paper files first, then extracted to the assembled file.")

if __name__ == "__main__":
    main()

