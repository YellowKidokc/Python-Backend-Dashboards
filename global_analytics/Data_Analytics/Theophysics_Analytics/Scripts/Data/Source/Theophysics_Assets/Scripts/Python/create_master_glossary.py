import json
import re
import os
import glob

# Re-use the string-based link extraction from before
def extract_links_from_text_string_based(text):
    """Extracts all Obsidian links from a given text block by string manipulation."""
    extracted_concepts = set()
    start_tag = "||"
    end_tag = "||"
    current_pos = 0
    while True:
        start_index = text.find(start_tag, current_pos)
        if start_index == -1:
            break
        
        end_index = text.find(end_tag, start_index + len(start_tag))
        if end_index == -1:
            break
            
        link_raw = text[start_index + len(start_tag) : end_index]
        
        if '|' in link_raw:
            concept = link_raw.split('|')[0].strip()
        else:
            concept = link_raw.strip()
            
        if concept and '#' not in concept and concept != '→':
            extracted_concepts.add(concept)
            
        current_pos = end_index + len(end_tag)
            
    return extracted_concepts

def create_master_glossary():
    """
    Reads markdown files in the glossary folder, extracts all unique linked terms and bolded terms,
    and creates a master JSON list of these terms.
    """
    glossary_file_pattern = r"D:\\THEOPHYSICS_MASTER\\02_LIBRARY\\Glossary\\*.md"
    glossary_files = glob.glob(glossary_file_pattern)
    
    unique_terms = set()

    for file_path in glossary_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Extract links using the helper function (string manipulation)
                unique_terms.update(extract_links_from_text_string_based(content))
                
                # Extract bolded terms (existing logic - simplified and less prone to regex issues)
                # This will extract all bolded text, and then we filter non-link bolded terms.
                bold_terms_raw = re.findall(r"**(.*?)**", content) 
                for term_raw in bold_terms_raw:
                    term = term_raw.strip()
                    # Filter out terms that are actually links or other non-desirable bolded text
                    if term and '#' not in term and term != '→' and not term.startswith('[') and not term.endswith(']'):
                        if len(term.split()) <= 5 and 'AXIOM' not in term and 'Law' not in term and 'Paper' not in term and 'DEBUG' not in term: # Added more filters
                            unique_terms.add(term)

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            continue

    output_path = r"D:\\THEOPHYSICS_MASTER\\00_VAULT_SYSTEM\\04_Analysis\\Master Sheets\\master_glossary.json"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(sorted(list(unique_terms)), f, indent=4, ensure_ascii=False)
        
    print(f"\nMaster glossary (flat list of terms) created at: {output_path}")
    print(f"Total unique terms found: {len(unique_terms)}")

if __name__ == "__main__":
    create_master_glossary()
