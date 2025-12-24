import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "08_Database" / "theophysics.db"
MOCS_DIR = Path(__file__).resolve().parents[1] / "03_Docs" / "MOCs"

CHARACTERS = ["GF", "JC", "HS", "ADV"]
TOPICS = ["trinity", "entanglement", "consciousness", "grace", "sin"]

def generate_character_mocs():
    for char in CHARACTERS:
        p = MOCS_DIR / "Characters" / f"{char}.md"
        content = [
            f"# {char} — Character MOC",
            "",
            "```dataview",
            "TABLE file.link AS Paper, series, paper_number, topics",
            'FROM ""',
            f'WHERE contains(characters, "{char}")', 
            "SORT series asc, paper_number asc",
            "```",
            ""
        ]
        p.write_text("\n".join(content), encoding="utf-8")

def generate_topic_mocs():
    for topic in TOPICS:
        p = MOCS_DIR / "Topics" / f"{topic}.md"
        content = [
            f"# Topic: {topic}",
            "",
            "```dataview",
            "TABLE file.link AS Paper, series, paper_number, characters",
            'FROM ""',
            f'WHERE contains(topics, "{topic}")', 
            "SORT series asc, paper_number asc",
            "```",
            ""
        ]
        p.write_text("\n".join(content), encoding="utf-8")

def main():
    generate_character_mocs()
    generate_topic_mocs()
    print("MOCs generated successfully.")

if __name__ == "__main__":
    main()

