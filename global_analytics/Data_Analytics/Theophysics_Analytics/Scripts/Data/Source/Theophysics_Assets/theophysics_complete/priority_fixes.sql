-- ===============================================================
-- MASTER EQUATION - PRIORITY FIXES
-- Run this AFTER loading the main schema to fill critical gaps
-- ===============================================================

-- ============== STEP 1: Add Missing Variables to Laws ==============

-- Add Time (T) to L7 (Relativity ↔ Eternal Perspective)
INSERT INTO law_variables (law_id, variable_id, role, weight)
VALUES (
  (SELECT id FROM laws WHERE code='L7'),
  (SELECT id FROM variables WHERE code='T'),
  'frame_axis',
  0.85
) ON CONFLICT DO NOTHING;

-- Add Resurrection (R) to L4 (Weak Nuclear ↔ Transformation)
INSERT INTO law_variables (law_id, variable_id, role, weight)
VALUES (
  (SELECT id FROM laws WHERE code='L4'),
  (SELECT id FROM variables WHERE code='R'),
  'mechanism',
  0.9
) ON CONFLICT DO NOTHING;

-- Add Faith (F) to L9 (Uncertainty ↔ Free Will)
INSERT INTO law_variables (law_id, variable_id, role, weight)
VALUES (
  (SELECT id FROM laws WHERE code='L9'),
  (SELECT id FROM variables WHERE code='F'),
  'actuator',
  0.8
) ON CONFLICT DO NOTHING;

-- Add Entropy (S) to L5 (Entropy ↔ Decay) - it was in L1 but should also be in L5
INSERT INTO law_variables (law_id, variable_id, role, weight)
VALUES (
  (SELECT id FROM laws WHERE code='L5'),
  (SELECT id FROM variables WHERE code='S'),
  'driver',
  0.95
) ON CONFLICT DO NOTHING;

-- Add Quantum (Q) to L6 (Wave-Particle ↔ Divine Complexity)
INSERT INTO law_variables (law_id, variable_id, role, weight)
VALUES (
  (SELECT id FROM laws WHERE code='L6'),
  (SELECT id FROM variables WHERE code='Q'),
  'basis',
  0.85
) ON CONFLICT DO NOTHING;

COMMIT;

-- ============== STEP 2: Connect Isolated Laws ==============

-- L6 (Duality) enables L8 (Entanglement) via superposition
WITH l AS (SELECT code, id FROM laws)
INSERT INTO law_links (src_law_id, dst_law_id, relation, weight)
VALUES (
  (SELECT id FROM l WHERE code='L6'),
  (SELECT id FROM l WHERE code='L8'),
  'enables',
  0.7
) ON CONFLICT DO NOTHING;

-- L7 (Relativity) supports L10 (Unified Theory)
WITH l AS (SELECT code, id FROM laws)
INSERT INTO law_links (src_law_id, dst_law_id, relation, weight)
VALUES (
  (SELECT id FROM l WHERE code='L7'),
  (SELECT id FROM l WHERE code='L10'),
  'supports',
  0.75
) ON CONFLICT DO NOTHING;

-- L2 (Divine Unity) supports L10 (Logos) via knowledge bridge
WITH l AS (SELECT code, id FROM laws)
INSERT INTO law_links (src_law_id, dst_law_id, relation, weight)
VALUES (
  (SELECT id FROM l WHERE code='L2'),
  (SELECT id FROM l WHERE code='L10'),
  'supports',
  0.65
) ON CONFLICT DO NOTHING;

-- L5 (Decay) opposes L4 (Transformation) - entropy vs redemption
WITH l AS (SELECT code, id FROM laws)
INSERT INTO law_links (src_law_id, dst_law_id, relation, weight)
VALUES (
  (SELECT id FROM l WHERE code='L4'),
  (SELECT id FROM l WHERE code='L5'),
  'opposes',
  0.8
) ON CONFLICT DO NOTHING;

COMMIT;

-- ============== STEP 3: Verification Queries ==============

-- Check that all variables are now used
SELECT 
  v.code,
  v.name,
  COUNT(lv.law_id) as used_in_laws
FROM variables v
LEFT JOIN law_variables lv ON lv.variable_id = v.id
GROUP BY v.code, v.name
ORDER BY used_in_laws DESC, v.code;

-- Check that no laws are isolated
SELECT 
  l.code,
  l.name,
  COUNT(DISTINCT CASE WHEN ll1.src_law_id = l.id THEN 1 END) as outgoing,
  COUNT(DISTINCT CASE WHEN ll2.dst_law_id = l.id THEN 1 END) as incoming,
  COUNT(DISTINCT lv.variable_id) as variables
FROM laws l
LEFT JOIN law_links ll1 ON ll1.src_law_id = l.id
LEFT JOIN law_links ll2 ON ll2.dst_law_id = l.id
LEFT JOIN law_variables lv ON lv.law_id = l.id
GROUP BY l.code, l.name
ORDER BY (outgoing + incoming + variables) ASC;

-- Show the complete law network
SELECT 
  l1.code || ' (' || l1.name || ')' as from_law,
  ll.relation,
  l2.code || ' (' || l2.name || ')' as to_law,
  ll.weight
FROM law_links ll
JOIN laws l1 ON l1.id = ll.src_law_id
JOIN laws l2 ON l2.id = ll.dst_law_id
ORDER BY ll.weight DESC;

-- ============== STEP 4: Example Paper Entry ==============

-- Add an example paper (replace with your actual papers)
INSERT INTO papers (slug, title, published_on, url, summary)
VALUES (
  'master-equation-intro',
  'The Master Equation: Unifying Physics and Theology',
  '2024-01-15',
  'https://theophysics.com/papers/master-equation-intro',
  'Introduces χ as the master integral unifying physical laws with theological principles'
)
ON CONFLICT (slug) DO NOTHING;

-- Link this paper to variables it discusses
INSERT INTO paper_mentions (paper_id, variable_id, count, weight)
SELECT 
  (SELECT id FROM papers WHERE slug='master-equation-intro'),
  v.id,
  CASE v.code
    WHEN 'G' THEN 25  -- Grace mentioned 25 times
    WHEN 'K' THEN 30  -- Knowledge mentioned 30 times
    WHEN 'S' THEN 15  -- Entropy mentioned 15 times
    ELSE 5
  END,
  CASE v.code
    WHEN 'G' THEN 0.9
    WHEN 'K' THEN 0.95
    WHEN 'S' THEN 0.8
    ELSE 0.5
  END
FROM variables v
WHERE v.code IN ('G', 'K', 'S')
ON CONFLICT DO NOTHING;

COMMIT;

-- ============== SUCCESS MESSAGE ==============

SELECT '==================================================' as message
UNION ALL SELECT 'MASTER EQUATION DATABASE - PRIORITY FIXES APPLIED'
UNION ALL SELECT '=================================================='
UNION ALL SELECT ''
UNION ALL SELECT '✓ All 10 variables now mapped to laws'
UNION ALL SELECT '✓ All laws now have at least one connection'
UNION ALL SELECT '✓ Example paper added to demonstrate integration'
UNION ALL SELECT ''
UNION ALL SELECT 'Next steps:'
UNION ALL SELECT '1. Start adding your 1300+ papers'
UNION ALL SELECT '2. Build semantic embeddings for search'
UNION ALL SELECT '3. Query the graph to find connections'
UNION ALL SELECT ''
UNION ALL SELECT 'Example queries:'
UNION ALL SELECT '- SELECT * FROM suggested_links;'
UNION ALL SELECT '- SELECT * FROM law_variable_bridges;'
UNION ALL SELECT '- SELECT * FROM law_coherence ORDER BY var_weight_sum DESC;';
