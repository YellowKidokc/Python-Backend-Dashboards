
import json
import os
import re

def hyperlink_papers():
    """
    Reads a JSON database of terms and URLs, and then iterates through a directory of markdown papers,
    replacing occurrences of the terms with markdown hyperlinks.
    """
    db_path = r"D:\THEOPHYSICS_MASTER\09_Tools\link_database.json"
    papers_dir = r"D:\THEOPHYSICS_MASTER\06_Publication\Logos Paper\BACKUPS"
    
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            link_db = json.load(f)
    except FileNotFoundError:
        print(f"Error: Link database not found at {db_path}")
        return
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {db_path}")
        return

    # Sort terms by length, longest first, to avoid partial replacements (e.g., "David Bohm" before "Bohm")
    sorted_terms = sorted(link_db.keys(), key=len, reverse=True)

    for filename in os.listdir(papers_dir):
        if filename.endswith(".md"):
            file_path = os.path.join(papers_dir, filename)
            print(f"Processing {filename}...")

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except IOError as e:
                print(f"  Could not read file: {e}")
                continue

            original_content = content

            for term in sorted_terms:
                url = link_db[term]
                # Regex to find the term as a whole word, not preceded by `[` or followed by `]` or `](`,
                # which would indicate it's already part of a link.
                # The negative lookbehind `(?<!\[)` ensures the term is not preceded by `[`. 
                # The negative lookahead `(?![^\\\[]*\]\()` ensures the term is not followed by `](` within a link.
                # `\b` ensures we match whole words.
                regex = r"(?<!\[)\b" + re.escape(term) + r"\b(?![^\\\[]*?\]\()"
                
                replacement = f"[{term}]({url})"
                
                content = re.sub(regex, replacement, content)

            if content != original_content:
                try:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"  Updated links for: {', '.join([term for term in sorted_terms if term in content])}")
                except IOError as e:
                    print(f"  Could not write to file: {e}")
            else:
                print("  No changes made.")

if __name__ == "__main__":
    hyperlink_papers()
    print("\nHyperlinking process complete.")
