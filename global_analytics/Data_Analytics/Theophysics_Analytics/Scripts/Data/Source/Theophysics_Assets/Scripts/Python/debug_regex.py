import re
import os

file_path = r"D:\THEOPHYSICS_MASTER\02_LIBRARY\THE CONSCIOUSNESS AXIOMS All.md"

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
    exit()

# Test regex for [[link]] or [[link|alias]] - now just capturing anything between [[ and ]]
test_regex = re.compile(r"\[\[(.*?)\]\]")
matches = test_regex.findall(content)

if matches:
    print("Found matches with specific regex (maximally permissive):")
    for match in matches:
        print(f"- {match}")
else:
    print("No matches found with the specific regex.")
