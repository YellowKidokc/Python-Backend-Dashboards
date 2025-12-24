-- ═══════════════════════════════════════════════════════════
-- UNIFIED KNOWLEDGE GRAPH SCHEMA
-- Integration: Spatial Layer + Epistemic Layer + Memory Layer
-- Database: kj @ 192.168.1.93:5432
-- Author: David Lowe + Claude
-- Date: 2025-11-19
-- ═══════════════════════════════════════════════════════════

-- ═══════════════════════════════════════════════════════════
-- SPATIAL INTELLIGENCE LAYER (from vault_refresh_v2.py)
-- ═══════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS vault_notes (
    uid TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    relative_path TEXT,
    folder_context TEXT,
    scan_zone TEXT,              -- Logos Papers, Library, Glossary, etc.
    content_type TEXT,            -- paper, note, glossary, reference
    domain TEXT,
    tags TEXT[],
    word_count INTEGER,
    hash TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_vault_notes_zone ON vault_notes(scan_zone);
CREATE INDEX IF NOT EXISTS idx_vault_notes_type ON vault_notes(content_type);
CREATE INDEX IF NOT EXISTS idx_vault_notes_folder ON vault_notes(folder_context);
CREATE INDEX IF NOT EXISTS idx_vault_notes_tags ON vault_notes USING GIN(tags);

-- ═══════════════════════════════════════════════════════════
-- CONCEPT TRACKING (from vault scanner)
-- ═══════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS vault_concepts (
    concept TEXT PRIMARY KEY,
    mentions INTEGER DEFAULT 0,
    zones TEXT[],                 -- Which scan zones use this concept
    first_seen TIMESTAMPTZ DEFAULT NOW(),
    last_seen TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS vault_concept_cooccurrence (
    concept_a TEXT,
    concept_b TEXT,
    cooccurrence_count INTEGER,
    zones TEXT[],
    PRIMARY KEY (concept_a, concept_b)
);

-- ═══════════════════════════════════════════════════════════
-- EPISTEMIC RELATIONSHIP LAYER (from Truth Engine)
-- ═══════════════════════════════════════════════════════════

-- Install pgvector extension for semantic embeddings
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS atomic_nodes (
    uuid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    content TEXT NOT NULL,
    node_type TEXT NOT NULL,      -- Hypothesis, Evidence, Theory, etc.
    file_path TEXT,
    file_uid TEXT,                 -- Links to vault_notes.uid
    confidence_score DECIMAL(3,2) DEFAULT 0.50,
    uses_sister_nomenclature BOOLEAN DEFAULT FALSE,
    embedding_vector vector(1536), -- OpenAI ada-002 embeddings
    metadata JSONB,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    
    FOREIGN KEY (file_uid) REFERENCES vault_notes(uid) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_atomic_nodes_type ON atomic_nodes(node_type);
CREATE INDEX IF NOT EXISTS idx_atomic_nodes_file ON atomic_nodes(file_uid);
CREATE INDEX IF NOT EXISTS idx_atomic_nodes_embedding ON atomic_nodes 
    USING ivfflat (embedding_vector vector_cosine_ops);

-- ═══════════════════════════════════════════════════════════
-- SEMANTIC EDGES (relationships between nodes)
-- ═══════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS semantic_edges (
    edge_id SERIAL PRIMARY KEY,
    source_uuid UUID NOT NULL,
    target_uuid UUID NOT NULL,
    relationship_type TEXT NOT NULL, -- SUPPORTS, REFUTES, EXTENDS, etc.
    confidence_score DECIMAL(3,2) DEFAULT 0.70,
    evidence TEXT,
    cross_zone BOOLEAN DEFAULT FALSE, -- Spans different scan zones
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    FOREIGN KEY (source_uuid) REFERENCES atomic_nodes(uuid) ON DELETE CASCADE,
    FOREIGN KEY (target_uuid) REFERENCES atomic_nodes(uuid) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_edges_source ON semantic_edges(source_uuid);
CREATE INDEX IF NOT EXISTS idx_edges_target ON semantic_edges(target_uuid);
CREATE INDEX IF NOT EXISTS idx_edges_type ON semantic_edges(relationship_type);

-- ═══════════════════════════════════════════════════════════
-- SISTER SCHOOL LEXICON (conceptual drift tracking)
-- ═══════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS sister_lexicon (
    lexicon_id SERIAL PRIMARY KEY,
    legacy_term TEXT NOT NULL,
    sister_term TEXT NOT NULL,
    drift_percentage DECIMAL(3,2) NOT NULL, -- 0.00 to 1.00
    domain TEXT,
    first_used TIMESTAMPTZ DEFAULT NOW(),
    usage_count INTEGER DEFAULT 1,
    
    UNIQUE(legacy_term, sister_term)
);

CREATE INDEX IF NOT EXISTS idx_lexicon_legacy ON sister_lexicon(legacy_term);
CREATE INDEX IF NOT EXISTS idx_lexicon_sister ON sister_lexicon(sister_term);

-- ═══════════════════════════════════════════════════════════
-- THEORY REGISTRY (70 external theories for congruency analysis)
-- ═══════════════════════════════════════════════════════════

CREATE TABLE IF NOT EXISTS theory_registry (
    theory_id SERIAL PRIMARY KEY,
    theory_name TEXT NOT NULL,
    author TEXT,
    year INTEGER,
    domain TEXT,
    key_concepts TEXT[],
    summary TEXT,
    embedding_vector vector(1536),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS theory_congruency (
    congruency_id SERIAL PRIMARY KEY,
    node_uuid UUID NOT NULL,
    theory_id INTEGER NOT NULL,
    congruency_score DECIMAL(3,2), -- Semantic similarity
    congruency_type TEXT,           -- SUPPORTS, OPPOSES, NEUTRAL
    notes TEXT,
    
    FOREIGN KEY (node_uuid) REFERENCES atomic_nodes(uuid) ON DELETE CASCADE,
    FOREIGN KEY (theory_id) REFERENCES theory_registry(theory_id) ON DELETE CASCADE
);

-- ═══════════════════════════════════════════════════════════
-- CONVERSATION MEMORY LAYER (existing table)
-- ═══════════════════════════════════════════════════════════

-- Table already exists: conversation_log
-- Adding columns to link conversations to vault context

ALTER TABLE conversation_log 
ADD COLUMN IF NOT EXISTS vault_context TEXT[],  -- Which notes/zones discussed
ADD COLUMN IF NOT EXISTS epistemic_nodes UUID[], -- Which atomic_nodes created
ADD COLUMN IF NOT EXISTS breakthrough_detected BOOLEAN DEFAULT FALSE;

-- ═══════════════════════════════════════════════════════════
-- UNIFIED QUERY VIEWS
-- ═══════════════════════════════════════════════════════════

-- View: Papers with epistemic annotations
CREATE OR REPLACE VIEW papers_with_hypotheses AS
SELECT 
    vn.title AS paper_title,
    vn.scan_zone,
    vn.folder_context,
    an.content AS hypothesis,
    an.confidence_score,
    an.uses_sister_nomenclature,
    COUNT(DISTINCT se.edge_id) AS relationship_count
FROM vault_notes vn
JOIN atomic_nodes an ON vn.uid = an.file_uid
LEFT JOIN semantic_edges se ON an.uuid = se.source_uuid OR an.uuid = se.target_uuid
WHERE vn.content_type = 'paper'
  AND an.node_type = 'Hypothesis'
GROUP BY vn.uid, an.uuid;

-- View: Cross-zone epistemic bridges
CREATE OR REPLACE VIEW cross_zone_bridges AS
SELECT 
    vn_source.scan_zone AS source_zone,
    vn_target.scan_zone AS target_zone,
    se.relationship_type,
    an_source.content AS source_content,
    an_target.content AS target_content,
    se.confidence_score
FROM semantic_edges se
JOIN atomic_nodes an_source ON se.source_uuid = an_source.uuid
JOIN atomic_nodes an_target ON se.target_uuid = an_target.uuid
JOIN vault_notes vn_source ON an_source.file_uid = vn_source.uid
JOIN vault_notes vn_target ON an_target.file_uid = vn_target.uid
WHERE vn_source.scan_zone != vn_target.scan_zone
  AND se.cross_zone = TRUE;

-- View: Sister School adoption metrics
CREATE OR REPLACE VIEW sister_adoption_metrics AS
SELECT 
    vn.scan_zone,
    COUNT(DISTINCT an.uuid) AS total_nodes,
    COUNT(DISTINCT CASE WHEN an.uses_sister_nomenclature THEN an.uuid END) AS sister_nodes,
    ROUND(
        COUNT(DISTINCT CASE WHEN an.uses_sister_nomenclature THEN an.uuid END)::NUMERIC / 
        NULLIF(COUNT(DISTINCT an.uuid), 0) * 100, 
        2
    ) AS sister_percentage
FROM vault_notes vn
LEFT JOIN atomic_nodes an ON vn.uid = an.file_uid
WHERE vn.scan_zone IS NOT NULL
GROUP BY vn.scan_zone
ORDER BY sister_percentage DESC;

-- View: Conversation-driven breakthroughs
CREATE OR REPLACE VIEW conversation_breakthroughs AS
SELECT 
    cl.date,
    cl.topics,
    cl.decisions,
    COUNT(DISTINCT an.uuid) AS nodes_created,
    array_agg(DISTINCT an.node_type) AS node_types
FROM conversation_log cl
JOIN LATERAL unnest(cl.epistemic_nodes) AS en(node_uuid) ON TRUE
JOIN atomic_nodes an ON an.uuid = en.node_uuid
WHERE cl.breakthrough_detected = TRUE
GROUP BY cl.date, cl.topics, cl.decisions
ORDER BY cl.date DESC;

-- ═══════════════════════════════════════════════════════════
-- HELPER FUNCTIONS
-- ═══════════════════════════════════════════════════════════

-- Find semantically similar nodes
CREATE OR REPLACE FUNCTION find_similar_nodes(
    query_embedding vector(1536),
    similarity_threshold DECIMAL DEFAULT 0.80,
    result_limit INTEGER DEFAULT 10
)
RETURNS TABLE (
    uuid UUID,
    content TEXT,
    node_type TEXT,
    similarity_score DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        an.uuid,
        an.content,
        an.node_type,
        ROUND((1 - (an.embedding_vector <=> query_embedding))::NUMERIC, 3) AS similarity_score
    FROM atomic_nodes an
    WHERE 1 - (an.embedding_vector <=> query_embedding) >= similarity_threshold
    ORDER BY an.embedding_vector <=> query_embedding
    LIMIT result_limit;
END;
$$ LANGUAGE plpgsql;

-- Find contradictions to a given node
CREATE OR REPLACE FUNCTION find_contradictions(node_uuid UUID)
RETURNS TABLE (
    contradicting_uuid UUID,
    contradicting_content TEXT,
    relationship_confidence DECIMAL
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        an.uuid,
        an.content,
        se.confidence_score
    FROM semantic_edges se
    JOIN atomic_nodes an ON se.source_uuid = an.uuid
    WHERE se.target_uuid = node_uuid
      AND se.relationship_type IN ('REFUTES', 'CONTRADICTS')
    ORDER BY se.confidence_score DESC;
END;
$$ LANGUAGE plpgsql;

-- Track Sister School term usage over time
CREATE OR REPLACE FUNCTION sister_term_timeline(term TEXT)
RETURNS TABLE (
    month DATE,
    usage_count INTEGER,
    papers_using INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        DATE_TRUNC('month', an.created_at)::DATE AS month,
        COUNT(*)::INTEGER AS usage_count,
        COUNT(DISTINCT an.file_uid)::INTEGER AS papers_using
    FROM atomic_nodes an
    JOIN sister_lexicon sl ON an.content ILIKE '%' || sl.sister_term || '%'
    WHERE sl.sister_term = term
    GROUP BY DATE_TRUNC('month', an.created_at)
    ORDER BY month;
END;
$$ LANGUAGE plpgsql;

-- ═══════════════════════════════════════════════════════════
-- EXAMPLE UNIFIED QUERIES
-- ═══════════════════════════════════════════════════════════

-- Query 1: Find hypotheses in Logos Papers with supporting evidence from Library
-- SELECT * FROM papers_with_hypotheses WHERE scan_zone = 'Logos Papers';

-- Query 2: Show cross-zone epistemic connections
-- SELECT * FROM cross_zone_bridges WHERE source_zone = 'Logos Papers';

-- Query 3: Track Sister School adoption by zone
-- SELECT * FROM sister_adoption_metrics;

-- Query 4: Find conversations that led to breakthroughs
-- SELECT * FROM conversation_breakthroughs WHERE date >= NOW() - INTERVAL '30 days';

-- Query 5: Semantic similarity search
-- SELECT * FROM find_similar_nodes(
--     (SELECT embedding_vector FROM atomic_nodes WHERE uuid = 'some-uuid'),
--     0.85,
--     20
-- );

-- ═══════════════════════════════════════════════════════════
-- MAINTENANCE & OPTIMIZATION
-- ═══════════════════════════════════════════════════════════

-- Vacuum and analyze for performance
VACUUM ANALYZE vault_notes;
VACUUM ANALYZE atomic_nodes;
VACUUM ANALYZE semantic_edges;

-- Update statistics
ANALYZE vault_concepts;
ANALYZE theory_registry;

COMMENT ON TABLE vault_notes IS 'Spatial intelligence: WHERE ideas live in the vault';
COMMENT ON TABLE atomic_nodes IS 'Epistemic substrate: WHAT claims exist and HOW they relate';
COMMENT ON TABLE semantic_edges IS 'Graph relationships: WHY ideas connect';
COMMENT ON TABLE sister_lexicon IS 'Conceptual drift: Translation between Legacy and Sister terminology';
COMMENT ON TABLE theory_registry IS 'External theories: Congruency analysis with 70 established frameworks';
COMMENT ON TABLE conversation_log IS 'Memory layer: Conversation history and breakthrough detection';
