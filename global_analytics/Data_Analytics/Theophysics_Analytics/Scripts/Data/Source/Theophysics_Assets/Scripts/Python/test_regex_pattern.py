import re

pattern_str = r"[[.*?]]"
try:
    compiled_pattern = re.compile(pattern_str)
    print(f"Successfully compiled pattern: {compiled_pattern.pattern}")
except re.error as e:
    print(f"Error compiling pattern: {e}")

# This is a dummy content to test the pattern
test_content = "Some text with a [[link to a file]] and another [[link with | an alias]]. Also [[#header]] should be ignored."
matches = compiled_pattern.findall(test_content)

if matches:
    print("\nMatches found:")
    for match in matches:
        print(f"- {match}")
else:
    print("No matches found in test content.")

