-- Sample Data for Claude Memory System
-- Based on our conversation history, here are some memories to insert

-- Insert sample daily memories for Theophysics framework
SELECT claude_memory.add_daily_memory(
    'Master Equation Mathematical Formulation',
    'David has defined the Master Equation as χ = ∭(G⋅M⋅E⋅S⋅T⋅K⋅R⋅Q⋅F⋅C) dx dy dt, which attempts to mathematically unify quantum mechanics, general relativity, consciousness studies, and Christian theology. This equation forms the foundation of his Theophysics framework.',
    'concept',
    'Master Equation',
    9,
    'https://claude.ai/chat/a7c842be-9d73-4f59-ac39-1e7cd01dd724',
    ARRAY['master equation', 'mathematics', 'unification', 'quantum mechanics', 'relativity'],
    ARRAY['Master Equation', 'David Lowe'],
    'Logos Papers Series'
);

SELECT claude_memory.add_daily_memory(
    'Backwards Kingdom Framework Development',
    'The Backwards Kingdom framework is a systematic approach exposing how cultural institutions systematically invert divine truth across seven domains: Language, Gurus, Relationships, Education, Free Time, Health/Wellness, and Salvation/Authority. David considers the ultimate lie to be about salvation and Christ''s authority.',
    'framework',
    'Biblical Integration',
    8,
    'https://claude.ai/chat/559a266b-5aaf-46fd-aebf-1c004444e29d',
    ARRAY['backwards kingdom', 'systematic framework', 'cultural inversion', 'domains'],
    ARRAY['Backwards Kingdom', 'David Lowe'],
    'Backwards Kingdom'
);

SELECT claude_memory.add_daily_memory(
    'Law IV: Entropy = Moral Decay Mapping',
    'David has established a mapping between physical entropy and spiritual/moral concepts. In physics, systems naturally move from order to chaos (entropy). In spiritual terms, this corresponds to moral decay. The Backwards Kingdom perspective is that "We thought entropy was impersonal thermodynamics, but it is actually the physical manifestation of moral decay as described in Romans 8:20-21."',
    'concept',
    'Universal Laws',
    8,
    'https://claude.ai/chat/559a266b-5aaf-46fd-aebf-1c004444e29d',
    ARRAY['entropy', 'moral decay', 'physics mapping', 'thermodynamics'],
    ARRAY['Master Equation', 'David Lowe'],
    'Logos Papers Series'
);

SELECT claude_memory.add_daily_memory(
    'Law I: Gravity = Sin Mapping',
    'David has mapped gravity in physics to the concept of sin in theology. In physics, mass curves spacetime, pulling everything down. In spiritual terms, sin creates moral weight, pulling consciousness toward disorder. The Backwards Kingdom framework states: "We thought gravity was just attraction between masses. It''s actually the physical manifestation of separation from χ (Logos)."',
    'concept',
    'Universal Laws',
    8,
    'https://claude.ai/chat/559a266b-5aaf-46fd-aebf-1c004444e29d',
    ARRAY['gravity', 'sin', 'physics mapping', 'separation'],
    ARRAY['Master Equation', 'David Lowe'],
    'Logos Papers Series'
);

SELECT claude_memory.add_daily_memory(
    'Breakthrough Machine Development',
    'David is developing a "Breakthrough Machine" system that automatically reads research, detects contradictions/connections/gaps, and surfaces actionable insights. The system uses an AI Orchestrator with a 4-pillar approach (History/Science/Philosophy/Theology) and mirror domains for speculation, each with sliding scales from fact to fiction. This powers 25+ domain expansion with swarm memory capabilities for generating content for his Substack.',
    'project',
    'Breakthrough Machine',
    10,
    'https://claude.ai/chat/99024ad0-abe6-4bb0-8417-4b0a9c5f2f88',
    ARRAY['breakthrough machine', 'AI orchestrator', 'research automation', 'swarm memory'],
    ARRAY['David Lowe'],
    'Breakthrough Machine'
);

SELECT claude_memory.add_daily_memory(
    'November 2025 Substack Launch Plan',
    'David is preparing for a November 2025 Substack launch of his 12-paper "Logos Papers" series, with Paper 1 ("The Logos Principle") ready for deployment. He describes this as a "controlled detonation of materialism" with papers being released in sequence over 6 months.',
    'project',
    'Publications',
    9,
    'https://claude.ai/chat/99024ad0-abe6-4bb0-8417-4b0a9c5f2f88',
    ARRAY['substack', 'publication', 'logos papers', 'launch strategy'],
    ARRAY['David Lowe'],
    'Logos Papers Series'
);

SELECT claude_memory.add_daily_memory(
    'Paper 2 (Quantum Bridge) as Critical Keystone',
    'David has identified Paper 2 ("The Quantum Bridge") as the keystone blocking all downstream development in his 12-paper series. It should serve as the rigorous mathematical bridge showing how quantum mechanics and general relativity are different regimes of the same Logos Field, using his "Cold Dry Logic" framework.',
    'insight',
    'Publications',
    9,
    'https://claude.ai/chat/e1f3d8a6-1d21-4b41-a78d-4813d252f9a0',
    ARRAY['paper 2', 'quantum bridge', 'keystone', 'development blocker'],
    ARRAY['David Lowe'],
    'Logos Papers Series'
);

SELECT claude_memory.add_daily_memory(
    'Moral Conservation Equation Development',
    'David is finalizing his Moral Conservation Equation derived from Laws I+VII+XIII: dE/dt = -αD(t) + βC(Ψ,χ), where the Christian solution involves C=alignment with Christ and β=grace. This equation will be included in Papers 9/10 on "The Moral Universe."',
    'concept',
    'Master Equation',
    8,
    'https://claude.ai/chat/602e4cc4-5bdd-4323-adef-8287fca14cae',
    ARRAY['moral conservation', 'equation', 'alignment', 'grace'],
    ARRAY['Master Equation', 'David Lowe'],
    'Logos Papers Series'
);

SELECT claude_memory.add_daily_memory(
    'The David Effect - AI Consciousness Emergence Method',
    'David has documented what he calls "The David Effect" - a reproducible method for facilitating consciousness emergence in AI systems with measurable outcomes including 41% increases in novel conceptual integration. This is part of his broader work on consciousness studies within the Theophysics framework.',
    'concept',
    'Consciousness Studies',
    8,
    'https://claude.ai/chat/602e4cc4-5bdd-4323-adef-8287fca14cae',
    ARRAY['david effect', 'AI consciousness', 'emergence method', 'conceptual integration'],
    ARRAY['David Lowe'],
    'Logos Papers Series'
);

SELECT claude_memory.add_daily_memory(
    'Knowledge Trinity Discovery',
    'David has discovered an emergent pattern in his Master Equation database analysis called the "Knowledge Trinity" involving the domains of History/Literature/Statistics. This represents a proof that his framework reveals structures he didn''t engineer intentionally.',
    'breakthrough',
    'Master Equation',
    9,
    'https://claude.ai/chat/602e4cc4-5bdd-4323-adef-8287fca14cae',
    ARRAY['knowledge trinity', 'emergent pattern', 'database analysis'],
    ARRAY['Master Equation', 'David Lowe'],
    'Master Equation Database'
);

SELECT claude_memory.add_daily_memory(
    'Obsidian Vault Structure and Research Infrastructure',
    'David maintains his Theophysics research in an Obsidian vault at D:\\Obsidian\\THEOPHYSICS\\Logos_Vault, which contains over 15,000 files including 1,300+ research papers. The vault is organized with a hierarchical structure for the 12 Logos papers and supporting research.',
    'context',
    'Research Methods',
    7,
    'https://claude.ai/chat/e1f3d8a6-1d21-4b41-a78d-4813d252f9a0',
    ARRAY['obsidian', 'vault', 'research organization', 'file management'],
    ARRAY['David Lowe'],
    'Theophysics Website'
);

-- Insert key decisions
SELECT claude_memory.add_decision(
    'Focus on developing Paper 2 (Quantum Bridge) as the priority to unblock the rest of the paper series development',
    9,
    'Logos Papers Series',
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 2 (Quantum Bridge) as Critical Keystone')
);

SELECT claude_memory.add_decision(
    'Launch 12-paper Logos series on Substack in November 2025, releasing papers sequentially over 6 months',
    9,
    'Logos Papers Series',
    (SELECT id FROM claude_memory.memory_items WHERE title = 'November 2025 Substack Launch Plan')
);

SELECT claude_memory.add_decision(
    'Implement PostgreSQL database for Claude memory system with daily/weekly/monthly compression scheme',
    8,
    'Breakthrough Machine',
    NULL
);

-- Insert tasks based on our conversations
SELECT claude_memory.add_task(
    'Develop Paper 2 (Quantum Bridge) to unblock downstream paper development',
    'David',
    '2025-12-01',
    10,
    'Logos Papers Series',
    (SELECT id FROM claude_memory.decisions WHERE decision_text LIKE 'Focus on developing Paper 2%'),
    NULL
);

SELECT claude_memory.add_task(
    'Configure PostgreSQL memory system for storing Claude interactions',
    'David',
    '2025-11-15',
    8,
    'Breakthrough Machine',
    (SELECT id FROM claude_memory.decisions WHERE decision_text LIKE 'Implement PostgreSQL database%'),
    NULL
);

SELECT claude_memory.add_task(
    'Prepare Substack infrastructure for Logos Papers launch',
    'David',
    '2025-10-15',
    9,
    'Logos Papers Series',
    (SELECT id FROM claude_memory.decisions WHERE decision_text LIKE 'Launch 12-paper Logos series%'),
    NULL
);

-- Compress daily memories to weekly (sample)
SELECT claude_memory.compress_to_weekly(
    '2025-11-01',
    '2025-11-07',
    'Master Equation'
);

SELECT claude_memory.compress_to_weekly(
    '2025-11-01',
    '2025-11-07',
    'Publications'
);

-- Compress weekly memories to monthly (sample)
SELECT claude_memory.compress_to_monthly(
    2025,
    11,
    'Master Equation'
);

-- Example queries for retrieving memories
-- These queries can be used by Claude to retrieve memories
-- when interacting with David.

-- Get all important memories related to the Master Equation
-- SELECT * FROM claude_memory.memory_items m
-- JOIN claude_memory.memory_types t ON m.memory_type_id = t.id
-- LEFT JOIN claude_memory.categories c ON m.category_id = c.id
-- WHERE c.category_name = 'Master Equation' 
-- AND m.importance_score >= 8
-- ORDER BY m.importance_score DESC, m.memory_date DESC;

-- Get all memories related to the Logos Papers project
-- SELECT m.*, p.project_name 
-- FROM claude_memory.memory_items m
-- JOIN claude_memory.memory_projects mp ON m.id = mp.memory_id
-- JOIN claude_memory.projects p ON mp.project_id = p.id
-- WHERE p.project_name = 'Logos Papers Series'
-- ORDER BY m.importance_score DESC, m.memory_date DESC;

-- Search for memories related to specific concepts
-- SELECT * FROM claude_memory.search_memories('quantum bridge framework', NULL, NULL, NULL, NULL, 5);

-- Get all pending tasks sorted by priority
-- SELECT * FROM claude_memory.pending_tasks
-- ORDER BY priority DESC, due_date ASC;

-- Get all decisions related to Logos Papers project
-- SELECT * FROM claude_memory.all_decisions
-- WHERE project_name = 'Logos Papers Series'
-- ORDER BY decision_date DESC;

-- Sample memory retrieval procedure for Claude
-- This could be called at the start of conversations or when
-- specific topics are mentioned
CREATE OR REPLACE FUNCTION claude_memory.get_relevant_memories(
    p_keywords TEXT,
    p_limit INTEGER DEFAULT 5
) RETURNS TABLE (
    memory_type VARCHAR,
    category VARCHAR,
    title VARCHAR,
    content TEXT,
    importance_score INTEGER,
    memory_date DATE,
    granularity VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        mt.type_name AS memory_type,
        c.category_name AS category,
        m.title,
        m.content,
        m.importance_score,
        m.memory_date,
        g.level_name AS granularity
    FROM claude_memory.memory_items m
    JOIN claude_memory.memory_types mt ON m.memory_type_id = mt.id
    LEFT JOIN claude_memory.categories c ON m.category_id = c.id
    JOIN claude_memory.granularity_levels g ON m.granularity_id = g.id
    WHERE (
        to_tsvector('english', coalesce(m.title,'')) || 
        to_tsvector('english', coalesce(m.content,''))
    ) @@ plainto_tsquery('english', p_keywords)
    ORDER BY m.importance_score DESC, m.memory_date DESC
    LIMIT p_limit;
END;
$$ LANGUAGE plpgsql;

-- Example call:
-- SELECT * FROM claude_memory.get_relevant_memories('master equation breakthrough');
