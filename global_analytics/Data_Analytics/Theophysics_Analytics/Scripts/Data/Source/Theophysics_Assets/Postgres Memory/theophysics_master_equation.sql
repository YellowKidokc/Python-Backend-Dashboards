-- Master Equation Reality Blueprint Memory Entries
-- This file contains SQL to document the Master Equation framework, structure and content

-- Add Master Equation Project
INSERT INTO claude_memory.projects (project_name, description, status, priority, start_date) VALUES
    ('Master Equation Reality Blueprint', 'Comprehensive framework for the Master Equation (χ) unifying physics, consciousness, and theology with a complete mathematical architecture', 'active', 10, '2025-01-01');

-- Add Master Equation Overview Memory
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
    'Master Equation Reality Blueprint - Complete Framework',
    'The Master Equation Reality Blueprint is a comprehensive framework that unifies physics, consciousness, and theology through a single mathematical expression: χ = ∭(G·M·E·S·T·K·R·Q·F·C)dxdydt. The blueprint addresses the fragmentation of science, the hard problem of consciousness, and the artificial faith-science divide through a unified field where every phenomenon is an expression of an underlying, coherent, and divinely orchestrated logic. The framework is structured into multiple sections including Foundational Axioms, the Master Equation, Twelve Unified Theories, Variable Unpacking, Revolutionary Breakthroughs, Philosophical Implications, Testable Predictions, and a Unified Reality conclusion.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'project'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Master Equation Structure Memory
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
    'Master Equation Structure - Organizational System',
    'The Master Equation Reality Blueprint uses a condensed letter code system for organization. The structure includes 11 primary folders: G-ME (General Master Equation), A-ME (Axioms), E-ME (Equations), C-ME (Convergence), V-ME (Variables), M-ME (Mathematics), I-ME (Insights), P-ME (Predictions), T-ME (Theory), S-ME (Synthesis), and F-ME (Final). Each folder contains 4 papers following a standard naming convention [LETTER]-ME-[NUMBER].md. This creates a comprehensive, systematic approach with 44 total papers, all following the Master Prompt format: Opening Narrative/Hook, Core Concept Overview, Fast Facts, Theological Deep Dive, Strategic Upsell, Scientific Integration, Integration & Theophysics Synthesis, Practical Application, and Strategic Links.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Master Equation Navigation Hub Memory
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
    'Master Equation Navigation Hub - Alternative Structure',
    'An alternative organization structure for the Master Equation exists with 11 folder series: DIS (Discovery), AXI (Axioms), EQ (Equation), CONV (Convergence), VAR (Variables), MATH (Mathematics), INS (Insights), VAL (Validation), APP (Applications), CONC (Conclusion), and APPX (Appendices). Papers follow the naming convention [FOLDER-NUMBER]-ME-[PAPER-TITLE]-[FOLDER-SHORT-NAME]-[SEQUENTIAL-NUMBER].md. The system includes character tags (#GF = God Father, #JC = Jesus Christ, #HS = Holy Spirit, #ADV = Adversary) and is designed to create a systematic framework for all the Master Equation content.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Master Equation Content Memory
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
    'Master Equation - Full Content Structure',
    'The Master Equation framework includes multiple sections: I. Executive Summary (the foundational crisis, Theophysics'' audacious claim, revolutionary axiom, ultimate achievement), II. Foundational Axioms (Logos-Tripartite Principle, Principle of Least Action & Path of Redemption, Adversarial Field & Strategic Corruption), III. Master Equation Unveiled (Full Equation, Governing Dynamics, Narrative Bridge), IV. Twelve Unified Theories (Quantum Mechanics & Divine Observation, General Relativity & Gravitational Grace, Thermodynamics & Spiritual Entropy, and others), V. Unpacking the Variables (Grace vs. Entropy Engine, Consciousness, Faith & Presence, Trinity, Mystery & The End), VI. Revolutionary Breakthroughs (Epigenetics of the Divine Genome, Resurrection as Cosmic Phase Transition, Great Exile, Advanced Formalisms), VII. Philosophical Implications (Mind-Body Problem, Causality to Purpose, Free Will), VIII. Testable Predictions, and IX. Conclusion (Great Reconciliation, Christ Convergence, Infinite Symphony).',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Master Equation Clean Structure Plan Memory
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
    'Master Equation Clean Structure Plan',
    'The Master Equation Reality Blueprint is undergoing a reorganization to clean up duplicate and mixed folder structures. The plan keeps the clean new structure with condensed letter folders (G-ME, A-ME, E-ME, etc.), the Trinity framework (TRINITY-INTEGRATION), Trinity series (GF-SERIES, JS-SERIES, HS-SERIES), research folders (DEEP-RESEARCH, ACADEMIC-PAPERS), and key navigation files. Older structure folders will be archived in ARCHIVE-OLD-STRUCTURE, and empty/duplicate folders will be removed. The final clean structure will have a main entry point (00-MASTER-NAVIGATION-HUB.md), the 11 condensed letter folders, Trinity integration folders, research folders, and assets. This reorganization provides better organization, navigation, and maintenance for the framework.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'decision'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Trinity Integration Memory
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
    'Trinity Integration - Three-Part Structure',
    'The Trinity Integration is a key aspect of the Master Equation Reality Blueprint, with dedicated folders for each person of the Trinity: GF-SERIES (God Father Series), JS-SERIES (Jesus Series), and HS-SERIES (Holy Spirit Series). This integration maps the three persons of the Trinity to mathematical and physical concepts: the Father as the foundation and constants, the Son (Logos) as the bridge and unifier, and the Holy Spirit as the field that actualizes potential. The structure includes character tags #GF, #JC, #HS, and #ADV (Adversary) to mark content related to each entity.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Foundational Axioms Memory
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
    'Foundational Axioms of the Master Equation',
    'The Master Equation framework is built on three foundational axioms: 1) The Logos-Tripartite Principle - reality is a unified field divided into matter, living things without a soul, and living things with a soul, with Jesus Christ as the unifying force; 2) The Principle of Least Action & The Path of Redemption - all reality follows the path of least action towards maximal redemptive coherence, which for conscious agents means choosing the "hardest path"; 3) The Adversarial Field & Strategic Corruption - an intelligent adversarial force actively concentrates on specific nodes to maximize decoherence, while miracles are displays of the Logos''s authority overriding this entropic force.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Master Equation Mathematics Memory
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
    'Master Equation Mathematical Components',
    'The full Master Equation χ(t) integrates multiple mathematical components: 1) The Cosmic Battle: Grace vs. Entropy - (1+E₀e^kt+S₀e^-λRpt)/(G₀e^(Rp/S)⋅RJ), 2) The Observer Effect: Faith Collapses Reality - e^-(Q⋅C), 3) The Faith Network: Spiritual Entanglement - (1+∑Fie^-di), 4) The Divine Presence: The Field of Meaning - [U₀+1+e^-k(Ss-S₀)L+ΔU], 5) Divine Timing: The Uncertainty of Revelation - e^-ΔR⋅ΔT, all integrated across Space, Time, and Spirit dimensions dxdydtdSs. The governing dynamics are expressed as a Lagrangian formulation (LRedemption) with redemptive action as the driving force, entropy as friction, and faith networks as coupling springs.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Twelve Unified Theories Memory
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
    'Twelve Unified Theories in the Master Equation',
    'The Master Equation framework includes twelve unified theories demonstrating mathematical convergence between science and theology: 1) Quantum Mechanics & Divine Observation - observer effect and wave function collapse map to divine observation, with prayer and faith as projection operators; 2) General Relativity & Gravitational Grace - spacetime curvature created by mass mirrors spiritual curvature created by divine love; 3) Thermodynamics & Spiritual Entropy - increasing entropy parallels spiritual entropy (sin), with grace as a negentropic force; 4) Information Theory & Logos; 5) Chaos Theory; 6) Network Theory; 7) Consciousness Studies; 8) Quantum Field Theory; 9) Fine-Tuning; 10) String Theory; 11) Trinity Doctrine; 12) Others. Each theory demonstrates how identical mathematical structures in science and theology point to a single truth.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Revolutionary Breakthroughs Memory
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
    'Revolutionary Breakthroughs in the Master Equation',
    'The Master Equation framework includes several revolutionary breakthroughs: 1) The Epigenetics of the Divine Genome - the Fall as catastrophic epigenetic silencing of humanity''s divine genes, with salvation as epigenetic therapy reactivating our original state; 2) The Resurrection as Cosmic Phase Transition - the ultimate negentropic event establishing perfect eternal coherence with the Logos; 3) The Great Exile: The Fall into Linear Time - the deepest wound of the Fall as the collapse from Eternal Now (Kairos) into Linear Time (Chronos); 4) Advanced Formalisms - including Theology of Sequence (Non-Commutative Algebra), Architecture of Creation (Symmetry Breaking), and novel lenses like GAN Theology, Topological Prayer Wormholes, and Time-Reversal Grace.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'breakthrough'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Testable Predictions Memory
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
    'Testable Predictions from the Master Equation',
    'The Master Equation framework generates specific, falsifiable predictions: 1) Prayer-QRNG Trials - focused prayer should produce non-random patterns in quantum random number generators; 2) EEG Coherence Mapping - collective worship should show enhanced brain-wave synchronicity; 3) Hospice EM-burst Probe - detectable information signatures should persist in the quantum field after death; 4) Prophecy-Quantum Correlation - statistical signatures should correlate with prophetic fulfillment; 5) Personal Spiritual Growth - a model for tracking one''s "Divine Alignment Index" using measurable inputs like prayer, worship, and community participation; 6) Revolutionary Applications - including Precision Spiritual Medicine, Consciousness-Enhanced Learning, and Spiritually-Aware AI.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Experiments'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    NULL,
    '2025-10-01'
);

-- Add Philosophical Implications Memory
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
    'Philosophical Implications of the Master Equation',
    'The Master Equation framework has profound philosophical implications: 1) The Mind-Body Problem, Solved - consciousness is not a product of matter but a fundamental field that gives rise to matter, with thoughts and intentions as forces influencing the universe''s fundamental components; 2) From Causality to Purpose - the universe is not a closed system running down to maximum disorder but an open system with purpose moving toward maximal redemptive coherence; 3) Free Will and the Quantum Collapse - free will is the conscious force that collapses possibilities into a single reality through the Observer Collapse Function (e^-(Q⋅C)), where consciousness (C) and focus (the opposite of doubt, Q) determine outcomes.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    NULL,
    '2025-10-01'
);

-- Create Master Equation tags
INSERT INTO claude_memory.tags (tag_name, tag_category, description, parent_tag)
VALUES 
    ('master_equation_blueprint', 'Framework', 'The Master Equation Reality Blueprint framework', NULL),
    ('foundational_axioms', 'Concept', 'Foundational axioms of the Master Equation', 'master_equation_blueprint'),
    ('organizational_structure', 'Structure', 'Organizational structure of the Master Equation documentation', 'master_equation_blueprint'),
    ('trinity_integration', 'Concept', 'Integration of the Trinity into the mathematical framework', 'master_equation_blueprint'),
    ('unified_theories', 'Concept', 'Twelve unified theories connecting science and theology', 'master_equation_blueprint'),
    ('mathematical_components', 'Concept', 'Mathematical components of the Master Equation', 'master_equation_blueprint'),
    ('breakthroughs', 'Concept', 'Revolutionary breakthroughs in the Master Equation framework', 'master_equation_blueprint'),
    ('testable_predictions', 'Concept', 'Falsifiable predictions derived from the Master Equation', 'master_equation_blueprint'),
    ('philosophical_implications', 'Concept', 'Philosophical implications of the Master Equation', 'master_equation_blueprint');

-- Tag the memories
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Reality Blueprint - Complete Framework'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Structure - Organizational System'),
    'organizational_structure'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Structure - Organizational System'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Navigation Hub - Alternative Structure'),
    'organizational_structure'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Navigation Hub - Alternative Structure'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation - Full Content Structure'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Clean Structure Plan'),
    'organizational_structure'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Trinity Integration - Three-Part Structure'),
    'trinity_integration'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Trinity Integration - Three-Part Structure'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Foundational Axioms of the Master Equation'),
    'foundational_axioms'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Foundational Axioms of the Master Equation'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Mathematical Components'),
    'mathematical_components'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Mathematical Components'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Twelve Unified Theories in the Master Equation'),
    'unified_theories'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Twelve Unified Theories in the Master Equation'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Revolutionary Breakthroughs in the Master Equation'),
    'breakthroughs'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Revolutionary Breakthroughs in the Master Equation'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Testable Predictions from the Master Equation'),
    'testable_predictions'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Testable Predictions from the Master Equation'),
    'master_equation_blueprint'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Philosophical Implications of the Master Equation'),
    'philosophical_implications'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Philosophical Implications of the Master Equation'),
    'master_equation_blueprint'
);

-- Link the memories to the project
INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Reality Blueprint - Complete Framework'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Structure - Organizational System'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    0.9
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Navigation Hub - Alternative Structure'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    0.8
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation - Full Content Structure'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Clean Structure Plan'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    0.7
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Trinity Integration - Three-Part Structure'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    0.9
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Foundational Axioms of the Master Equation'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Mathematical Components'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Twelve Unified Theories in the Master Equation'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Revolutionary Breakthroughs in the Master Equation'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Testable Predictions from the Master Equation'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    0.9
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Philosophical Implications of the Master Equation'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    0.8
);

-- Create tasks related to the Master Equation Reality Blueprint
INSERT INTO claude_memory.tasks (
    task_description,
    assigned_to,
    due_date,
    status,
    priority,
    related_project_id,
    related_decision_id
) VALUES (
    'Implement clean structure reorganization for Master Equation Reality Blueprint',
    'David',
    '2025-11-15',
    'pending',
    8,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    NULL
);

INSERT INTO claude_memory.tasks (
    task_description,
    assigned_to,
    due_date,
    status,
    priority,
    related_project_id,
    related_decision_id
) VALUES (
    'Complete the G-ME-01 Master Equation Overview document',
    'David',
    '2025-11-30',
    'pending',
    9,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    NULL
);

INSERT INTO claude_memory.tasks (
    task_description,
    assigned_to,
    due_date,
    status,
    priority,
    related_project_id,
    related_decision_id
) VALUES (
    'Develop detailed experimental protocols for Prayer-QRNG Trials prediction',
    'David',
    '2025-12-15',
    'pending',
    8,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    NULL
);

INSERT INTO claude_memory.tasks (
    task_description,
    assigned_to,
    due_date,
    status,
    priority,
    related_project_id,
    related_decision_id
) VALUES (
    'Complete Trinity Integration documentation with mathematical mappings',
    'David',
    '2025-12-31',
    'pending',
    9,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    NULL
);

-- Create decision related to Master Equation
INSERT INTO claude_memory.decisions (
    decision_text,
    decision_date,
    memory_id,
    related_project_id,
    importance_score,
    decision_status
) VALUES (
    'Adopt the condensed letter code organizational system for all Master Equation content',
    NOW(),
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Structure - Organizational System'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Master Equation Reality Blueprint'),
    8,
    'active'
);
