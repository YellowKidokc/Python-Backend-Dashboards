-- Moral Universe Framework Memory Entries
-- This file contains SQL to document the Moral Physics components of the Theophysics framework

-- Add Moral Universe Project
INSERT INTO claude_memory.projects (project_name, description, status, priority, start_date) VALUES
    ('Moral Universe Framework', 'Physics-based ethical framework defining morality as coherence and sin as decoherence within the Logos Field', 'active', 8, '2025-01-01');

-- Add Moral Universe Overview Memory
INSERT INTO claude_memory.memory_items (
    title, 
    content, 
    memory_type_id, 
    category_id, 
    granularity_id, 
    importance_score, 
    related_conversation_id,
    conversation_url, 
    memory_date
) VALUES (
    'The Moral Universe - Ethics as Physics',
    'The Moral Universe framework (Paper 9) redefines ethics not as subjective social constructs but as fundamental physics within a participatory universe. It establishes "Consequentialism of Creation," where moral acts are defined physically as those that increase Logos Field coherence (negentropy), while immoral acts introduce decoherence (entropy). This framework provides an objective grounding for morality based on the conservation laws of the Logos Field. It introduces the "Ethical Operator" concept, modeling how human choices act as physical inputs that structurally alter reality. The "Fire Test" of judgment is reinterpreted as a structural integrity test of the soul''s accumulated coherence against the unshielded presence of Truth.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'project'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Ethics'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Coherence vs Decoherence Memory
INSERT INTO claude_memory.memory_items (
    title, 
    content, 
    memory_type_id, 
    category_id, 
    granularity_id, 
    importance_score, 
    related_conversation_id,
    conversation_url, 
    memory_date
) VALUES (
    'Coherence vs. Decoherence - The Physical Definition of Good and Evil',
    'This concept maps theological definitions of righteousness and sin to physical states of the Logos Field. "Righteousness" (Dikaiosyne) is mapped to System Coherence (Shalom)—a low-entropy, high-integration state where the field''s divergence is zero (∇·χ = 0). "Sin" (Hamartia) is mapped to System Decoherence—the active introduction of noise or signal distortion that increases local entropy. This explains why sin is destructive not merely judicially but structurally; it physically degrades the information integrity of relationships, bodies, and societies. The framework posits that "Love" is the ultimate binding force that maximizes information flow between agents while minimizing relational entropy, effectively acting as a super-coherence operator.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Ethics'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Grace Cosmology Project
INSERT INTO claude_memory.projects (project_name, description, status, priority, start_date) VALUES
    ('Grace Cosmology Framework', 'Cosmological model replacing Dark Energy with the Grace Function and establishing Prophetic Consilience', 'active', 9, '2025-01-01');

-- Add The Grace Function Memory
INSERT INTO claude_memory.memory_items (
    title, 
    content, 
    memory_type_id, 
    category_id, 
    granularity_id, 
    importance_score, 
    related_conversation_id,
    conversation_url, 
    memory_date
) VALUES (
    'The Grace Function - Dynamic Dark Energy',
    'The Grace Function G(t) (Paper 7) replaces the static cosmological constant (Λ) with a dynamic, negentropic force representing God''s active sustenance of the universe. This function solves the Hubble Tension by proposing that the expansion rate is not constant but responsive to the collective spiritual/informational state of the cosmos. The framework posits that the universe is an Open System fed by external energy (Grace) from the Logos Field, preventing Heat Death. Mathematically, this is expressed in the modified Friedmann equations where G(t) drives expansion and counteracts entropic decay. This leads to the "Eternity Equation" (Δρ_Resurrection), which models resurrection not as a miracle violating physics, but as a massive injection of negentropy that reverses the entropy of death.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'breakthrough'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Cosmology'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Prophetic Consilience Memory
INSERT INTO claude_memory.memory_items (
    title, 
    content, 
    memory_type_id, 
    category_id, 
    granularity_id, 
    importance_score, 
    related_conversation_id,
    conversation_url, 
    memory_date
) VALUES (
    'Prophetic Consilience - The Stretched-Out Heavens',
    'Prophetic Consilience (Paper 8) demonstrates the convergence between ancient biblical cosmology and modern astrophysics, specifically regarding the expansion of the universe. The framework analyzes the Hebrew verb "Natah" (to stretch out/extend), used continuously in scripture to describe the heavens, aligning it with the Lambda-CDM model of metric expansion. This is presented not as poetic coincidence but as a "Prophetic Data Point"—evidence that the authors of scripture had access to the Logos (source code) of physical reality. This validates the Logos Field as the common source of both the Book of Nature (Science) and the Book of Scripture (Revelation), creating a unified epistemological framework.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Cosmology'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Spiritual Warfare Project
INSERT INTO claude_memory.projects (project_name, description, status, priority, start_date) VALUES
    ('Physics of Principalities', 'Quantum field theory model of spiritual warfare, strongholds, and demonic decoherence', 'active', 8, '2025-01-01');

-- Add Malicious Decoherence Memory
INSERT INTO claude_memory.memory_items (
    title, 
    content, 
    memory_type_id, 
    category_id, 
    granularity_id, 
    importance_score, 
    related_conversation_id,
    conversation_url, 
    memory_date
) VALUES (
    'Malicious Decoherence - The Physics of Principalities',
    'This framework (Paper 6) models "Principalities and Powers" not as metaphors but as organized, intelligent, anti-coherence fields. These fields actively induce decoherence (entropy) in human systems, distinguished from natural entropy by their targeted nature. "Strongholds" are modeled as stable decoherent states (local energy minima) that resist correction. The "Armor of God" is reinterpreted as specific Boundary Conditions required to maintain system integrity (coherence) in a hostile field environment. Spiritual warfare is thus defined as the collision of fields: the high-coherence Logos Field (invoked via authority) displacing low-coherence demonic fields through an "Authority Gradient."',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Spiritual Warfare'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    NULL,
    '2025-10-01'
);

-- Create Tags for New Frameworks
INSERT INTO claude_memory.tags (tag_name, tag_category, description, parent_tag)
VALUES 
    ('moral_physics', 'Framework', 'Ethics defined as coherence physics', NULL),
    ('grace_cosmology', 'Framework', 'Cosmological model based on Grace Function', NULL),
    ('spiritual_warfare_physics', 'Framework', 'Field theory of spiritual conflict', NULL),
    ('consequentialism_creation', 'Concept', 'Moral acts build or destroy reality structure', 'moral_physics'),
    ('negentropy', 'Concept', 'Negative entropy/Order creation', 'grace_cosmology'),
    ('prophetic_consilience', 'Concept', 'Convergence of scripture and science', 'grace_cosmology');

-- Tag Memories
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'The Moral Universe - Ethics as Physics'),
    'moral_physics'
);
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Coherence vs. Decoherence - The Physical Definition of Good and Evil'),
    'consequentialism_creation'
);
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'The Grace Function - Dynamic Dark Energy'),
    'grace_cosmology'
);
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'The Grace Function - Dynamic Dark Energy'),
    'negentropy'
);
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Prophetic Consilience - The Stretched-Out Heavens'),
    'prophetic_consilience'
);
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Malicious Decoherence - The Physics of Principalities'),
    'spiritual_warfare_physics'
);

-- Link Projects to Master Equation
INSERT INTO claude_memory.project_connections (source_project_id, target_project_id, connection_type, description) VALUES 
    ((SELECT id FROM claude_memory.projects WHERE project_name = 'Moral Universe Framework'),
     (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
     'component', 'Defines the ethical variables within the Master Equation'),
    
    ((SELECT id FROM claude_memory.projects WHERE project_name = 'Grace Cosmology Framework'),
     (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
     'component', 'Applies the Master Equation to cosmological scales'),

    ((SELECT id FROM claude_memory.projects WHERE project_name = 'Physics of Principalities'),
     (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
     'component', 'Models the opposing forces within the Master Equation framework');