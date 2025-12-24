-- ============================================
--  Breakthrough Vault Schema (PostgreSQL)
--  Mirrors Phase 1+ Python system
-- ============================================

CREATE SCHEMA IF NOT EXISTS breakthrough;

SET search_path TO breakthrough;

-- ======================
-- Core Notes Table
-- ======================
CREATE TABLE notes (
    uid TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    path TEXT,
    domain TEXT,
    tags TEXT[],
    word_count INTEGER,
    hash CHAR(40), -- SHA1
    updated_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- Concept Registry
-- ======================
CREATE TABLE concepts (
    concept TEXT PRIMARY KEY,
    mentions INTEGER DEFAULT 0
);

-- ======================
-- Co-Mentions (concept pairs)
-- ======================
CREATE TABLE co_mentions (
    concept1 TEXT REFERENCES concepts(concept) ON DELETE CASCADE,
    concept2 TEXT REFERENCES concepts(concept) ON DELETE CASCADE,
    count INTEGER DEFAULT 0,
    PRIMARY KEY (concept1, concept2)
);

-- ======================
-- Edges (semantic relations)
-- supports / contradicts / analogy / related
-- ======================
CREATE TABLE edges (
    src TEXT REFERENCES notes(uid) ON DELETE CASCADE,
    dst TEXT REFERENCES notes(uid) ON DELETE CASCADE,
    rel TEXT CHECK (rel IN ('supports','contradicts','analogy','related')),
    weight NUMERIC(5,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (src, dst, rel)
);

-- ======================
-- Metrics (validation layer)
-- SIS / LCS / SRI
-- ======================
CREATE TABLE metrics (
    uid TEXT PRIMARY KEY REFERENCES notes(uid) ON DELETE CASCADE,
    sis NUMERIC(5,4),
    lcs NUMERIC(5,4),
    sri NUMERIC(5,4),
    computed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ======================
-- UID Registry (for deterministic ID generation)
-- ======================
CREATE TABLE uid_registry (
    domain TEXT,
    topic TEXT,
    kind TEXT,
    idx INTEGER DEFAULT 0,
    PRIMARY KEY (domain, topic, kind)
);

-- ======================
-- Duplicates Table
-- ======================
CREATE TABLE duplicates (
    uid1 TEXT REFERENCES notes(uid) ON DELETE CASCADE,
    uid2 TEXT REFERENCES notes(uid) ON DELETE CASCADE,
    similarity NUMERIC(5,4),
    exact BOOLEAN DEFAULT FALSE,
    detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (uid1, uid2)
);

-- ======================
-- File Hash Index (for rapid dedup)
-- ======================
CREATE INDEX idx_notes_hash ON notes(hash);
CREATE INDEX idx_notes_domain ON notes(domain);
CREATE INDEX idx_notes_tags_gin ON notes USING GIN (tags);

-- ======================
-- Concept Co-occurrence Performance Indexes
-- ======================
CREATE INDEX idx_concepts_mentions ON concepts(mentions DESC);
CREATE INDEX idx_comentions_count ON co_mentions(count DESC);

-- ======================
-- Edges Relationship Indexing
-- ======================
CREATE INDEX idx_edges_rel ON edges(rel);
CREATE INDEX idx_edges_weight ON edges(weight);

-- ======================
-- Metrics Indexing
-- ======================
CREATE INDEX idx_metrics_sis ON metrics(sis DESC);
CREATE INDEX idx_metrics_lcs ON metrics(lcs DESC);
CREATE INDEX idx_metrics_sri ON metrics(sri DESC);

-- ======================
-- Trigger Example (Auto-update concept mentions)
-- ======================
CREATE OR REPLACE FUNCTION increment_concept_mentions()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE concepts
    SET mentions = mentions + 1
    WHERE concept = NEW.concept1 OR concept = NEW.concept2;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_increment_mentions
AFTER INSERT ON co_mentions
FOR EACH ROW
EXECUTE FUNCTION increment_concept_mentions();
