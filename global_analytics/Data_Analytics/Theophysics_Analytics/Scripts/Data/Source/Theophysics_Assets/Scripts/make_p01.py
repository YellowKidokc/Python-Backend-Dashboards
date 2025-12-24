from pathlib import Path

folder = Path('P01-[[Theophysics_Glossary#Logos|Logos]]-Principle')
md_files = sorted([f for f in folder.glob('*.md') if 'Final ALL' not in f.name and 'README' not in f.name])
output = folder / 'P01 Final ALL.md'

print(f'Found {len(md_files)} files in P01-[[Theophysics_Glossary#Logos|Logos]]-Principle')
for f in md_files:
    print(f'  - {f.name}')

with open(output, 'w', encoding='utf-8') as out:
    out.write('# P01-[[Theophysics_Glossary#Logos|LOGOS]]-PRINCIPLE: COMPLETE COLLECTION\n\n')
    out.write('**All Papers from P01-[[Theophysics_Glossary#Logos|Logos]]-Principle Folder**\n')
    out.write('**Compiled:** November 22, 2025\n')
    out.write(f'**Papers Included:** {len(md_files)}\n\n---\n\n')
    out.write('## TABLE OF CONTENTS\n\n')
    
    for i, f in enumerate(md_files, 1):
        out.write(f'{i}. [{f.stem}]\n')
    out.write('\n---\n\n')
    
    for i, f in enumerate(md_files, 1):
        print(f'Adding: {f.name}')
        out.write(f'# {i}. {f.stem.upper()}\n\n**Source:** `{f.name}`\n\n---\n\n')
        with open(f, 'r', encoding='utf-8') as inf:
            out.write(inf.read())
        out.write('\n\n---\n\n**END OF {f.stem.upper()}**\n\n---\n\n\n')

print(f'\n✓ Created: {output}')
print(f'  Size: {output.stat().st_size:,} bytes')
