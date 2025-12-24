"""
THEOPHYSICS Word Ontology Validator
Computes semantic similarity between new term definitions and source words.

Usage:
    python validate_term.py --definition "your definition" --sources "word1,word2,word3"
    
Returns:
    - Similarity score (0-1)
    - Validation status (APPROVED/REJECTED)
    - Zone classification
    - Recommendations
"""

import argparse
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple

# Load embedding model (using all-MiniLM-L6-v2 for fast, accurate embeddings)
MODEL = None

def load_model():
    """Load the sentence transformer model."""
    global MODEL
    if MODEL is None:
        print("Loading embedding model...")
        MODEL = SentenceTransformer('all-MiniLM-L6-v2')
    return MODEL

def compute_similarity(definition: str, source_words: List[str]) -> float:
    """
    Compute cosine similarity between definition and source words.
    
    Args:
        definition: The definition of the new term
        source_words: List of source words/phrases being replaced
        
    Returns:
        Cosine similarity score (0-1)
    """
    model = load_model()
    
    # Embed the definition
    def_embedding = model.encode(definition, convert_to_numpy=True)
    
    # Embed each source word
    source_embeddings = model.encode(source_words, convert_to_numpy=True)
    
    # Average source embeddings
    avg_source = np.mean(source_embeddings, axis=0)
    
    # Compute cosine similarity
    similarity = np.dot(def_embedding, avg_source) / (
        np.linalg.norm(def_embedding) * np.linalg.norm(avg_source)
    )
    
    return float(similarity)

def classify_zone(similarity: float) -> Tuple[str, str]:
    """
    Classify similarity into validation zones.
    
    Returns:
        (status, zone_name)
    """
    if similarity < 0.70:
        return "REJECTED", "Too Dissimilar (<70%)"
    elif similarity <= 0.90:
        return "APPROVED", "Valid Birth Zone (70-90%)"
    else:
        return "REJECTED", "Too Similar (>90%)"

def validate_term(definition: str, source_words: List[str]) -> dict:
    """
    Complete validation of a term.
    
    Returns:
        Dictionary with validation results
    """
    similarity = compute_similarity(definition, source_words)
    status, zone = classify_zone(similarity)
    
    # Generate recommendations
    recommendations = []
    if similarity < 0.70:
        recommendations.append("Definition too disconnected from source concepts")
        recommendations.append("Add more inheritance from source meanings")
        recommendations.append("Ensure core semantic features are preserved")
    elif similarity > 0.90:
        recommendations.append("Definition too redundant with source")
        recommendations.append("Add more novel/differentiating features")
        recommendations.append("Ensure this term adds something new")
    else:
        recommendations.append("Excellent balance of inheritance and novelty")
        recommendations.append("This term successfully bridges concepts")
    
    return {
        'similarity': similarity,
        'percentage': f"{similarity * 100:.1f}%",
        'status': status,
        'zone': zone,
        'inheritance': similarity,
        'novelty': 1 - similarity,
        'recommendations': recommendations
    }

def format_output(result: dict, definition: str, source_words: List[str]) -> str:
    """Format validation results for display."""
    status_symbol = "✅" if result['status'] == "APPROVED" else "❌"
    
    output = f"""
{'='*70}
THEOPHYSICS TERM VALIDATION REPORT
{'='*70}

DEFINITION:
{definition}

SOURCE WORDS:
{', '.join(source_words)}

{'='*70}
RESULTS:
{'='*70}

Similarity Score:  {result['similarity']:.4f} ({result['percentage']})
Status:            {status_symbol} {result['status']}
Zone:              {result['zone']}

Inheritance:       {result['inheritance']:.2f} (preserved meaning from source)
Novelty:           {result['novelty']:.2f} (new meaning introduced)

{'='*70}
RECOMMENDATIONS:
{'='*70}
"""
    for i, rec in enumerate(result['recommendations'], 1):
        output += f"{i}. {rec}\n"
    
    output += f"\n{'='*70}\n"
    
    if result['status'] == "APPROVED":
        output += "✅ VALIDATION PASSED - Term ready for ontology\n"
    else:
        output += "❌ VALIDATION FAILED - Revise definition and retry\n"
    
    output += f"{'='*70}\n"
    
    return output

def main():
    parser = argparse.ArgumentParser(
        description='Validate THEOPHYSICS ontology terms'
    )
    parser.add_argument(
        '--definition',
        type=str,
        required=True,
        help='Definition of the new term'
    )
    parser.add_argument(
        '--sources',
        type=str,
        required=True,
        help='Comma-separated list of source words/concepts'
    )
    
    args = parser.parse_args()
    
    # Parse source words
    source_words = [s.strip() for s in args.sources.split(',')]
    
    # Validate
    result = validate_term(args.definition, source_words)
    
    # Output
    print(format_output(result, args.definition, source_words))
    
    # Exit code (0 = success, 1 = failure)
    return 0 if result['status'] == "APPROVED" else 1

if __name__ == "__main__":
    exit(main())
