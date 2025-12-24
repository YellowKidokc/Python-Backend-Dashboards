def extract_links_from_text_pure_string(text):
    """Extracts all Obsidian links from a given text block using pure string manipulation."""
    extracted_concepts = set()
    
    start_tag = "[["
    end_tag = "]]"
    
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
