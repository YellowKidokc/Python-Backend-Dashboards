import psycopg2

conn = psycopg2.connect('postgresql://postgres:Moss9pep28$@192.168.1.243/theophysics')
cur = conn.cursor()

# Types to add for the Universal Analyzer
new_types = [
    ('claim', 'Claim or Assertion', '#FF6B6B', '◇', 10),
    ('definition', 'Term Definition', '#4ECDC4', '📖', 15),
    ('equation', 'Mathematical Expression', '#FFE66D', '∫', 20),
    ('event', 'Timeline Event or Date', '#95E1D3', '📅', 25),
    ('theory_reference', 'External Theory Reference', '#A8DADC', '🔗', 30),
    ('breakthrough', 'Novel Insight or Discovery', '#F38181', '💡', 35)
]

try:
    for name, desc, color, icon, priority in new_types:
        cur.execute("""
            INSERT INTO epistemic.types (name, bundle_profile, description, color, icon, priority)
            VALUES (%s, 'personal', %s, %s, %s, %s)
            ON CONFLICT (name, bundle_profile) DO NOTHING
        """, (name, desc, color, icon, priority))
    
    conn.commit()
    print("✓ Successfully added 6 new types to 'personal' profile")
    print()
    
    # Verify
    cur.execute("SELECT name FROM epistemic.types WHERE bundle_profile = 'personal' ORDER BY priority")
    types = [row[0] for row in cur.fetchall()]
    print(f"Types now in 'personal' profile ({len(types)} total):")
    for t in types:
        print(f"  • {t}")
    
except Exception as e:
    conn.rollback()
    print(f"✗ Error: {e}")

conn.close()
