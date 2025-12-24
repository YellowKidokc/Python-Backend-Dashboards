import json
import re # Only for re.search for axiom/law headers now
import os

# Purely string-based link extraction function (copied from corrected create_master_glossary.py logic)
def extract_links_from_text_pure_string(text):
    """Extracts all Obsidian links from a given text block using pure string manipulation."""
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


def extract_blocks(file_path, header_keyword):
    """A more robust function to extract blocks of text following a header line,
    stopping at the next header of the same level or a horizontal rule (---).
    """
    blocks = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return []

    header_indices = [i for i, line in enumerate(lines) if line.strip().startswith(header_keyword)]
    
    if not header_indices:
        return []

    for i, start_index in enumerate(header_indices):
        header_line = lines[start_index].strip()
        
        # Find the end of the block more precisely
        block_end_index = len(lines)
        for j in range(start_index + 1, len(lines)):
            line = lines[j].strip()
            # Stop if we hit another header of the same level or a horizontal rule
            if line.startswith(header_keyword) or line.startswith('---'):
                block_end_index = j
                break
        
        # Content starts from the line after the header
        content_start_index = start_index + 1
        # Skip empty lines immediately following the header
        while content_start_index < block_end_index and not lines[content_start_index].strip():
            content_start_index += 1

        axiom_text_content = "".join(lines[content_start_index : block_end_index]).strip()
        
        # Combine header and actual content for link extraction
        full_block_for_links = header_line + '\n' + axiom_text_content
        
        # Use the purely string-based helper function for key concepts
        # This directly returns the cleaned concepts, no further processing needed here
        cleaned_concepts = sorted(list(extract_links_from_text_pure_string(full_block_for_links)))

        # Extract axiom number and name
        axiom_num = 0
        axiom_name = "Unknown"

        # For **AXIOM ...** headers
        axiom_num_match = re.search(r'AXIOM\s+(\d+)', header_line)
        if axiom_num_match:
            axiom_num = int(axiom_num_match.group(1))
            name_match = re.search(r'\|([^\\]+)\]\]', header_line) # Get name from within the link alias
            axiom_name = name_match.group(1).strip() if name_match else f"Axiom {axiom_num}"
        else: # For ### Law ... headers
            law_num_match = re.search(r'Law\s+(\d+):\s+(.*)', header_line)
            if law_num_match:
                axiom_num = int(law_num_match.group(1))
                axiom_name = f"Law {axiom_num}: {law_num_match.group(2).strip()}"


        blocks.append({
            "number": axiom_num,
            "name": axiom_name,
            "header": header_line,
            "content": axiom_text_content,
            "key_concepts": cleaned_concepts
        })
        
    return blocks

def create_profile(file_path, output_dir):
    """
    Reads a markdown file, extracts axioms and laws, and saves them as a structured JSON file.
    """
    # Try to parse axioms first
    results = extract_blocks(file_path, "**AXIOM")
    
    # If no axioms, try to parse laws
    if not results:
        results = extract_blocks(file_path, "### Law")

    if not results:
        print(f"No axioms or laws found in {os.path.basename(file_path)}.")
        return

    base_name = os.path.basename(file_path)
    file_name_without_ext = os.path.splitext(base_name)[0]
    output_filename = f"{file_name_without_ext}_profile.json"
    output_path = os.path.join(output_dir, output_filename)
    
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
        
    print(f"Profile created for '{base_name}' at: {output_path}")
    print(f"Total items found: {len(results)}")

if __name__ == "__main__":
    core_axiom_file = r"D:\\THEOPHYSICS_MASTER\\02_LIBRARY\\THE CONSCIOUSNESS AXIOMS All.md"
    master_sheets_dir = r"D:\\THEOPHYSICS_MASTER\\00_VAULT_SYSTEM\\04_Analysis\\Master Sheets"
    print(f"Processing core axiom file: {os.path.basename(core_axiom_file)}")
    create_profile(core_axiom_file, master_sheets_dir)
    print("-" * 20)

    paper_1_file = r"D:\\THEOPHYSICS_MASTER\\03_PUBLICATIONS\\COMPLETE_LOGOS_PAPERS_FINAL\\P01-Logos-Principle\\Paper-1-The-Logos-Principle-CANONICAL.md"
    paper_analysis_dir = r"D:\\THEOPHYSICS_MASTER\\00_VAULT_SYSTEM\\04_Analysis\\Data Analytics"
    print(f"Processing Paper 1: {os.path.basename(paper_1_file)}")
    create_profile(paper_1_file, paper_analysis_dir)
