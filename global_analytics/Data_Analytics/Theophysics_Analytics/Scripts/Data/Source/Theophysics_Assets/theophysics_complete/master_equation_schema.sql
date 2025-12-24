
-- ===============================================================
-- Master Equation Mapping DB (PostgreSQL)
-- Author: GPT-5 Thinking (with David Lowe)
-- Purpose: Store and explore the Master Equation graph
-- ===============================================================

CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS fuzzystrmatch;
CREATE EXTENSION IF NOT EXISTS vector;

-- 1) Core reference tables
CREATE TABLE IF NOT EXISTS laws (
  id        SERIAL PRIMARY KEY,
  code      TEXT UNIQUE NOT NULL,
  name      TEXT NOT NULL,
  summary   TEXT
);

CREATE TABLE IF NOT EXISTS layers (
  id        SERIAL PRIMARY KEY,
  code      TEXT UNIQUE NOT NULL,
  name      TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS variables (
  id        SERIAL PRIMARY KEY,
  code      TEXT UNIQUE NOT NULL,
  name      TEXT NOT NULL,
  domain    TEXT,
  description TEXT
);

CREATE TABLE IF NOT EXISTS axioms (
  id          SERIAL PRIMARY KEY,
  law_id      INT NOT NULL REFERENCES laws(id) ON DELETE CASCADE,
  layer_id    INT NOT NULL REFERENCES layers(id) ON DELETE CASCADE,
  short_label TEXT NOT NULL,
  definition  TEXT,
  UNIQUE (law_id, layer_id)
);

CREATE TABLE IF NOT EXISTS law_variables (
  law_id      INT NOT NULL REFERENCES laws(id) ON DELETE CASCADE,
  variable_id INT NOT NULL REFERENCES variables(id) ON DELETE CASCADE,
  role        TEXT,
  weight      NUMERIC,
  PRIMARY KEY (law_id, variable_id)
);

CREATE TABLE IF NOT EXISTS law_links (
  src_law_id  INT NOT NULL REFERENCES laws(id) ON DELETE CASCADE,
  dst_law_id  INT NOT NULL REFERENCES laws(id) ON DELETE CASCADE,
  relation    TEXT,
  weight      NUMERIC,
  CHECK (src_law_id < dst_law_id),
  PRIMARY KEY (src_law_id, dst_law_id)
);

CREATE TABLE IF NOT EXISTS papers (
  id        SERIAL PRIMARY KEY,
  slug      TEXT UNIQUE,
  title     TEXT NOT NULL,
  published_on DATE,
  url       TEXT,
  summary   TEXT
);

CREATE TABLE IF NOT EXISTS paper_mentions (
  paper_id    INT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
  variable_id INT NOT NULL REFERENCES variables(id) ON DELETE CASCADE,
  count       INT DEFAULT 1,
  weight      NUMERIC,
  PRIMARY KEY (paper_id, variable_id)
);

CREATE TABLE IF NOT EXISTS tags (
  id    SERIAL PRIMARY KEY,
  name  TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS paper_tags (
  paper_id INT NOT NULL REFERENCES papers(id) ON DELETE CASCADE,
  tag_id   INT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  PRIMARY KEY (paper_id, tag_id)
);

CREATE TABLE IF NOT EXISTS embeddings (
  id         SERIAL PRIMARY KEY,
  item_type  TEXT NOT NULL,
  item_id    INT NOT NULL,
  embedding  VECTOR(768),
  UNIQUE (item_type, item_id)
);

-- 2) Seed data
INSERT INTO laws (code, name, summary) VALUES
('L1','Gravitation ↔ Sin’s Pull','Separation force; entropy gradient as moral analogue'),
('L2','Strong Nuclear ↔ Divine Unity','Binding potential; covenant cohesion'),
('L3','Electromagnetism ↔ Truth','Signal channel; revelation as disclosure'),
('L4','Weak Nuclear ↔ Transformation','Decay pathway; redemptive change'),
('L5','Entropy ↔ Decay','Second Law; the Fall as disorder'),
('L6','Wave–Particle ↔ Divine Complexity','Duality; Christic two-nature mystery'),
('L7','Relativity ↔ Eternal Perspective','Frame invariance; omnipresence across observers'),
('L8','Entanglement ↔ Communion','Nonlocal unity; ekklesia as network'),
('L9','Uncertainty ↔ Free Will','Bounds of knowledge; choice probability'),
('L10','Unified Theory ↔ Logos','Grand unification; master integral χ')
ON CONFLICT (code) DO NOTHING;

INSERT INTO layers (code, name) VALUES
('math','Mathematical'),
('theo','Theological'),
('info','Informational'),
('divine','Law of God')
ON CONFLICT (code) DO NOTHING;

INSERT INTO variables (code, name, domain, description) VALUES
('G','Grace','theo|field','Negentropic restorative field'),
('M','Motion','physics','Dynamics / strong binding analogue'),
('E','Energy','physics','Electromagnetic / truth-carrying capacity'),
('S','Entropy','thermo','Decay / disorder / sin analogue'),
('T','Time','relativity','Temporal / eternity axis'),
('K','Knowledge','epistemic','Logos / information content'),
('R','Resurrection','transform','Tunneling / renewal operator'),
('Q','Quantum','probability','Choice / superposition mechanics'),
('F','Faith','control','Belief → action operator / prior'),
('C','Consciousness','observer','Observer / actualizer / measurement')
ON CONFLICT (code) DO NOTHING;

WITH l AS (SELECT code, id FROM laws), y AS (SELECT code, id FROM layers)
INSERT INTO axioms (law_id, layer_id, short_label, definition) VALUES
((SELECT id FROM l WHERE code='L1'), (SELECT id FROM y WHERE code='math'),  'Inverse Square', 'Attraction scales with 1/r^2'),
((SELECT id FROM l WHERE code='L1'), (SELECT id FROM y WHERE code='theo'),  'Separation',     'Sin as separating pull'),
((SELECT id FROM l WHERE code='L1'), (SELECT id FROM y WHERE code='info'),  'Entropy Gradient','Direction of disorder growth'),
((SELECT id FROM l WHERE code='L1'), (SELECT id FROM y WHERE code='divine'),'Moral Attraction','Pull toward consequence'),

((SELECT id FROM l WHERE code='L2'), (SELECT id FROM y WHERE code='math'),  'Binding',        'Short-range binding potential'),
((SELECT id FROM l WHERE code='L2'), (SELECT id FROM y WHERE code='theo'),  'Covenant',       'Divine unity, held fast'),
((SELECT id FROM l WHERE code='L2'), (SELECT id FROM y WHERE code='info'),  'Lock',           'Information lock-in / code concatenation'),
((SELECT id FROM l WHERE code='L2'), (SELECT id FROM y WHERE code='divine'),'Eternal Hold',   'Bond that does not fail'),

((SELECT id FROM l WHERE code='L3'), (SELECT id FROM y WHERE code='math'),  'Maxwell',        'Field equations for EM'),
((SELECT id FROM l WHERE code='L3'), (SELECT id FROM y WHERE code='theo'),  'Revelation',     'Truth disclosed as light'),
((SELECT id FROM l WHERE code='L3'), (SELECT id FROM y WHERE code='info'),  'Channel',        'Capacity, SNR, coding'),
((SELECT id FROM l WHERE code='L3'), (SELECT id FROM y WHERE code='divine'),'Light Bearer',   'God as source of truth'),

((SELECT id FROM l WHERE code='L4'), (SELECT id FROM y WHERE code='math'),  'Decay',          'Beta decay / weak interactions'),
((SELECT id FROM l WHERE code='L4'), (SELECT id FROM y WHERE code='theo'),  'Redemption',     'Transformative passage'),
((SELECT id FROM l WHERE code='L4'), (SELECT id FROM y WHERE code='info'),  'Error Correction','Syndrome detect/correct'),
((SELECT id FROM l WHERE code='L4'), (SELECT id FROM y WHERE code='divine'),'Change Agent',   'God acts to renew'),

((SELECT id FROM l WHERE code='L5'), (SELECT id FROM y WHERE code='math'),  'Second Law',     'dS/dt ≥ 0 in closed systems'),
((SELECT id FROM l WHERE code='L5'), (SELECT id FROM y WHERE code='theo'),  'Fall',           'Universal drift to decay'),
((SELECT id FROM l WHERE code='L5'), (SELECT id FROM y WHERE code='info'),  'Uncertainty Rise','Loss of structure over time'),
((SELECT id FROM l WHERE code='L5'), (SELECT id FROM y WHERE code='divine'),'Sin Spread',     'Decay without intervention'),

((SELECT id FROM l WHERE code='L6'), (SELECT id FROM y WHERE code='math'),  'Duality',        'Wave–particle twofoldness'),
((SELECT id FROM l WHERE code='L6'), (SELECT id FROM y WHERE code='theo'),  'Two Natures',    'Fully God and fully man'),
((SELECT id FROM l WHERE code='L6'), (SELECT id FROM y WHERE code='info'),  'Ambiguity',      'State dual description'),
((SELECT id FROM l WHERE code='L6'), (SELECT id FROM y WHERE code='divine'),'Mystery Veil',   'Revealed yet hidden'),

((SELECT id FROM l WHERE code='L7'), (SELECT id FROM y WHERE code='math'),  'Invariance',     'Laws hold across frames'),
((SELECT id FROM l WHERE code='L7'), (SELECT id FROM y WHERE code='theo'),  'Omnipresence',   'Presence across perspectives'),
((SELECT id FROM l WHERE code='L7'), (SELECT id FROM y WHERE code='info'),  'Observer Bias',  'Relational description'),
((SELECT id FROM l WHERE code='L7'), (SELECT id FROM y WHERE code='divine'),'Timeless View',  'Eternal vantage'),

((SELECT id FROM l WHERE code='L8'), (SELECT id FROM y WHERE code='math'),  'Nonlocal',       'EPR/Bell correlations'),
((SELECT id FROM l WHERE code='L8'), (SELECT id FROM y WHERE code='theo'),  'Communion',      'Body unity across distance'),
((SELECT id FROM l WHERE code='L8'), (SELECT id FROM y WHERE code='info'),  'Correlation Max','Mutual information peak'),
((SELECT id FROM l WHERE code='L8'), (SELECT id FROM y WHERE code='divine'),'Prayer Chain',   'Petition linkage'),

((SELECT id FROM l WHERE code='L9'), (SELECT id FROM y WHERE code='math'),  'Bounds',         'Δx·Δp ≥ ħ/2 type limits'),
((SELECT id FROM l WHERE code='L9'), (SELECT id FROM y WHERE code='theo'),  'Freedom',        'Real choice under bounds'),
((SELECT id FROM l WHERE code='L9'), (SELECT id FROM y WHERE code='info'),  'Prob Cloud',     'Distributions over states'),
((SELECT id FROM l WHERE code='L9'), (SELECT id FROM y WHERE code='divine'),'Will Granted',   'Delegated agency'),

((SELECT id FROM l WHERE code='L10'), (SELECT id FROM y WHERE code='math'), 'Unification',    'Single field / gauge synthesis'),
((SELECT id FROM l WHERE code='L10'), (SELECT id FROM y WHERE code='theo'), 'Logos',          'Word sustains all things'),
((SELECT id FROM l WHERE code='L10'), (SELECT id FROM y WHERE code='info'), 'Master Integral','χ as integral over creation'),
((SELECT id FROM l WHERE code='L10'), (SELECT id FROM y WHERE code='divine'),'Divine Code',   'The code of creation')
ON CONFLICT DO NOTHING;

WITH l AS (SELECT code, id FROM laws), v AS (SELECT code, id FROM variables)
INSERT INTO law_variables (law_id, variable_id, role, weight) VALUES
((SELECT id FROM l WHERE code='L1'), (SELECT id FROM v WHERE code='S'), 'driver', 0.9),
((SELECT id FROM l WHERE code='L1'), (SELECT id FROM v WHERE code='G'), 'counter', 0.7),
((SELECT id FROM l WHERE code='L2'), (SELECT id FROM v WHERE code='M'), 'driver', 0.85),
((SELECT id FROM l WHERE code='L2'), (SELECT id FROM v WHERE code='K'), 'lock',   0.6),
((SELECT id FROM l WHERE code='L3'), (SELECT id FROM v WHERE code='E'), 'carrier',0.95),
((SELECT id FROM l WHERE code='L3'), (SELECT id FROM v WHERE code='K'), 'content',0.7),
((SELECT id FROM l WHERE code='L8'), (SELECT id FROM v WHERE code='C'), 'mediator',0.9),
((SELECT id FROM l WHERE code='L8'), (SELECT id FROM v WHERE code='Q'), 'mechanism',0.75),
((SELECT id FROM l WHERE code='L10'), (SELECT id FROM v WHERE code='G'),'synth',  0.9),
((SELECT id FROM l WHERE code='L10'), (SELECT id FROM v WHERE code='K'),'synth',  0.85)
ON CONFLICT DO NOTHING;

WITH l AS (SELECT code, id FROM laws)
INSERT INTO law_links (src_law_id, dst_law_id, relation, weight) VALUES
( (SELECT id FROM l WHERE code='L1'),  (SELECT id FROM l WHERE code='L5'), 'implies', 0.8 ),
( (SELECT id FROM l WHERE code='L3'),  (SELECT id FROM l WHERE code='L10'),'supports',0.7 ),
( (SELECT id FROM l WHERE code='L4'),  (SELECT id FROM l WHERE code='L9'), 'mediates',0.6 ),
( (SELECT id FROM l WHERE code='L8'),  (SELECT id FROM l WHERE code='L10'),'lifts',   0.75 )
ON CONFLICT DO NOTHING;

-- Indexes
CREATE INDEX IF NOT EXISTS idx_axioms_law_layer ON axioms(law_id, layer_id);
CREATE INDEX IF NOT EXISTS idx_lawvars_law ON law_variables(law_id);
CREATE INDEX IF NOT EXISTS idx_lawvars_var ON law_variables(variable_id);
CREATE INDEX IF NOT EXISTS idx_links_src ON law_links(src_law_id);
CREATE INDEX IF NOT EXISTS idx_links_dst ON law_links(dst_law_id);
CREATE INDEX IF NOT EXISTS idx_paper_mentions_var ON paper_mentions(variable_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_item ON embeddings(item_type, item_id);

-- Views
CREATE OR REPLACE VIEW law_coherence AS
SELECT
  l.id AS law_id,
  l.code AS law_code,
  l.name AS law_name,
  COALESCE(SUM(lv.weight),0) AS var_weight_sum,
  COUNT(lv.variable_id)      AS var_count
FROM laws l
LEFT JOIN law_variables lv ON lv.law_id = l.id
GROUP BY l.id, l.code, l.name;

CREATE OR REPLACE VIEW law_adjacency AS
SELECT src_law_id, dst_law_id, relation, weight FROM law_links;

CREATE OR REPLACE VIEW suggested_links AS
WITH pairs AS (
  SELECT lv1.law_id AS a, lv2.law_id AS b,
         COUNT(*) AS shared_vars,
         AVG((lv1.weight + lv2.weight)/2.0) AS avg_shared_weight
  FROM law_variables lv1
  JOIN law_variables lv2
    ON lv1.variable_id = lv2.variable_id
   AND lv1.law_id < lv2.law_id
  GROUP BY lv1.law_id, lv2.law_id
),
existing AS (
  SELECT src_law_id AS a, dst_law_id AS b FROM law_links
)
SELECT p.a AS law_a, p.b AS law_b, p.shared_vars, p.avg_shared_weight
FROM pairs p
LEFT JOIN existing e ON e.a = p.a AND e.b = p.b
WHERE e.a IS NULL AND p.shared_vars >= 2
ORDER BY p.avg_shared_weight DESC, p.shared_vars DESC;

CREATE OR REPLACE VIEW law_variable_bridges AS
SELECT
  l1.code AS law_a,
  l2.code AS law_b,
  v.code  AS variable_code,
  (lv1.weight + lv2.weight)/2.0 AS bridge_weight
FROM law_variables lv1
JOIN law_variables lv2 ON lv2.variable_id = lv1.variable_id AND lv2.law_id > lv1.law_id
JOIN laws l1 ON l1.id = lv1.law_id
JOIN laws l2 ON l2.id = lv2.law_id
JOIN variables v ON v.id = lv1.variable_id;

-- Example queries are in comments at end of file.
