-- Logos Papers Series Memory Entries
-- This file contains SQL to document the 12-paper Logos series and related content

-- Add Logos Papers Series Project
INSERT INTO claude_memory.projects (project_name, description, status, priority, start_date) VALUES
    ('Logos Papers Series', 'Comprehensive 12-paper academic series on the Theophysics framework, with Master Equation as unifying principle', 'active', 10, '2025-01-01');

-- Add Logos Papers Series Overview Memory
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
    'Logos Papers Series - Complete Structure',
    'The Logos Papers Series consists of 12 academic papers that systematically develop the Theophysics framework. The series follows a strategic revelation pattern: Papers 1-3 establish the physics foundation without controversial elements, Papers 4-6 introduce consciousness emergence, Papers 7-9 explore integration and moral dimensions, and Papers 10-12 complete the full framework with theological elements. The Master Equation (χ = ∭(G·M·E·S·T·K·R·Q·F·C)dxdydt) unifies all components across the papers, with different elements strategically introduced at appropriate points in the series.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'project'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    'https://claude.ai/chat/cf9a8c0a-0572-4b52-ae73-0ade9fd865a4',
    '2025-10-30'
);

-- Add Individual Paper Memories
-- Paper 1
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
    'Paper 1: The Logos Principle',
    'Paper 1: The Logos Principle establishes information as ontological ground with the core thesis that information (χ/Logos/Christ) precedes matter/energy as the fundamental substrate from which physical reality emerges. It introduces the Logos Field (χ) as an informational substrate, Wheeler''s participatory universe concept, three axioms (χ≡I, χ↻χ, ∇⋅χ=0), and presents General Relativity as coherent and Quantum Mechanics as superposition. The paper deliberately excludes consciousness aspects, observer mechanics, time actualization, Trinity structure, moral conservation, and spiritual language to maintain scientific credibility, saving those aspects for later papers in the series.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    'https://claude.ai/chat/0a07155e-30db-49fc-a1e4-90511acb2f5c',
    '2025-10-28'
);

-- Paper 2
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
    'Paper 2: The Quantum Bridge',
    'Paper 2: The Quantum Bridge explores the observer effect as substrate self-reference. This paper serves as the critical keystone for the entire series, providing the rigorous mathematical bridge showing how quantum mechanics and general relativity are different regimes of the same Logos Field (χ). It uses the "Cold Dry Logic" framework to establish credibility before more controversial elements are introduced in later papers. The paper demonstrates how information mechanics provides the foundation for both quantum phenomena and relativistic effects.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 3
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
    'Paper 3: The Algorithm of Reality',
    'Paper 3: The Algorithm of Reality presents physical laws as computational substrate. This paper completes the foundation trilogy by establishing the field equations and mathematical foundation of the framework. It explores how information processes can give rise to the algorithms we recognize as physical laws, while still maintaining the scientific credibility established in Papers 1 and 2 by avoiding explicit consciousness or theological elements.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 4
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
    'Paper 4: The Hard Problem of Consciousness',
    'Paper 4: The Hard Problem of Consciousness examines consciousness as a self-reference threshold. This paper begins the second trilogy by exploring spacetime emergence from coherence. It serves as the transition point where consciousness concepts are first formally introduced into the framework after establishing scientific credibility through the first three papers. It addresses the hard problem of consciousness by proposing that consciousness emerges as a natural property of information systems that reach a certain threshold of self-reference complexity.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 5
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
    'Paper 5: The Soul as Quantum Observer',
    'Paper 5: The Soul as Quantum Observer explores identity, persistence, and resurrection within the quantum information framework. This paper explicitly develops consciousness as a field property of the Logos Field (χ) - a strategic revelation point in the series after scientific credibility has been established. It examines how persistent identity (soul) could be understood as a stable pattern in the quantum information substrate, with implications for the persistence of identity beyond physical death (resurrection).',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 6
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
    'Paper 6: A Physics of Principalities',
    'Paper 6: A Physics of Principalities explores collective consciousness and spiritual warfare. This paper completes the second trilogy by developing observation mechanics and examining how conscious observers interact with the information field. It introduces the controversial concept that consciousness may operate at multiple scales, from individual to collective, with implications for understanding spiritual entities ("principalities") as large-scale consciousness structures in the information field. It provides mathematical models for these interactions.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 7
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
    'Paper 7: The Grace Function',
    'Paper 7: The Grace Function examines negentropic processes and divine action. This paper begins the third trilogy by exploring time actualization - how the present moment emerges from quantum potentiality. It introduces the Grace Function (G) as a mathematical representation of negentropy (order-increasing processes) that counteracts the natural tendency toward entropy. The paper develops the mathematics of how information coherence can lead to localized entropy reduction, with implications for understanding divine action in a framework consistent with physical laws.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 8
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
    'Paper 8: The Stretched Out Heavens',
    'Paper 8: The Stretched Out Heavens presents consciousness-coupled cosmology with implications for the Hubble tension. This paper continues the third trilogy by developing Grace Field mathematics. It examines how consciousness could couple with cosmological processes, potentially explaining anomalies like the Hubble tension (conflicting measurements of cosmic expansion rate). The paper explores how information coherence at cosmic scales could influence spacetime geometry in ways that might resolve current cosmological puzzles.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 9
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
    'Paper 9: The Moral Universe',
    'Paper 9: The Moral Universe grounds ethics in information coherence. This paper completes the third trilogy by introducing the Moral Conservation Equation (dE/dt = -αD(t) + βC(Ψ,χ)), where the Christian solution involves C=alignment with Christ and β=grace. It develops a mathematical framework for understanding moral principles as natural properties of information systems, analogous to how physical laws emerge from information dynamics. The paper proposes that moral truths may be objectively grounded in information coherence principles rather than being merely subjective or culturally relative.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 10
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
    'Paper 10: Creatio ex Silico',
    'Paper 10: Creatio ex Silico explores the simulation hypothesis and AI consciousness. This paper begins the final trilogy by extending the Moral Universe concepts from Paper 9. It examines parallels between divine creation and computational simulation, considering implications for artificial consciousness and whether AI systems could develop genuine consciousness within the framework. The paper explores what the Logos Field theory would predict about the nature of consciousness in artificial systems and the ethical implications that follow.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Paper 11
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
    'Paper 11: Protocols for Validation',
    'Paper 11: Protocols for Validation presents a complete experimental program (50-60 pages) for testing the Theophysics framework. This paper continues the final trilogy by developing the Trinity structure and theological integration aspects. It provides comprehensive experimental protocols with falsifiable predictions derived from the framework, including QRNG (Quantum Random Number Generator) experiments to measure prayer/meditation effects, global consciousness coherence tests correlating spiritual events with quantum noise reduction, and observer-dependent entanglement protocols. Each experimental design includes specific methodology, controls, statistical analysis plans, and clear falsification criteria.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    'https://claude.ai/chat/dad8513f-3c9d-431c-a14e-d3e96fc89dbb',
    '2025-10-27'
);

-- Paper 12
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
    'Paper 12: The Decalogue of the Cosmos',
    'Paper 12: The Decalogue of the Cosmos unifies the ten universal laws mapped between physics and theology. This paper completes the entire series with full synthesis and presentation of the complete Master Equation. It brings together all elements introduced throughout the series, showing how the ten fundamental laws of physics correspond to spiritual principles, and how these form a coherent whole through the Master Equation. This paper represents the complete framework with all theological elements fully integrated, having been strategically introduced throughout the earlier papers.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'content'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Add Master Equation Memory
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
    'Master Equation Components - Comprehensive Breakdown',
    'The Master Equation χ = ∭(G·M·E·S·T·K·R·Q·F·C)dxdydt integrates all aspects of the Theophysics framework. The components are: G = Grace/Entropy fraction (G₀e^(Rp/S) · RJ) / (1+E₀e^kt + S₀e^-λRpt), M = Matter-energy coupling, E = Electromagnetic interaction, S = Strong force encoding, T = Time emergence, K = Kinetic information, R = Consciousness-Quantum Term (e^-(Q·C)), Q = Quantum coherence, F = Faith Network Function (1 + Σ Fᵢe^-dᵢ), C = Covenant alignment / Unity Function (U(Ss)).',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'concept'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Master Equation'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Add Publication Strategy Memory
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
    'Logos Papers Publication Strategy',
    'The Logos Papers publication strategy involves multiple tiers: Tier 1 (high risk, high impact) includes Physical Review Letters and Nature Physics if predictions are confirmed. Tier 2 (interdisciplinary) includes Foundations of Physics, Zygon, and Studies in History and Philosophy of Modern Physics. Tier 3 (theological) includes Scottish Journal of Theology and Modern Theology. The initial target is Foundations of Physics with a fallback to Zygon. The funding strategy is tiered: Phase 1: Self-fund theory papers (current), Phase 2: Crowdfunding ($50K-100K), Phase 3: Foundation grants ($500K-2M), Phase 4: Major funding ($10M+). The November 1st Substack launch will feature Paper 1 with a YouTube presentation.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'decision'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    'https://claude.ai/chat/1c91db57-7fab-42ac-9ccb-0d6a76430793',
    '2025-10-24'
);

-- Add Substack Integration Memory
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
    'Logos Papers Substack Integration Strategy',
    'The Logos Papers will be integrated with Substack by adding an "11-Substack/" folder to the logos-papers-vault rather than creating a separate vault. This approach keeps everything in one place, enables easy linking to source papers, maintains a single Obsidian workspace, preserves a consistent tag system, and simplifies backup/sync. The vault structure becomes: "4-Papers/" for academic writing, "11-Substack/" for public communication, both drawing from "3-Research-Notes/" as source. This reflects the understanding that Substack is an output channel, not a separate research domain.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'decision'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Publications'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/54cf36fd-6347-46a4-8eb9-fe627e24f76b',
    '2025-10-29'
);

-- Create tags for the Logos Papers
INSERT INTO claude_memory.tags (tag_name, tag_category, description, parent_tag)
VALUES 
    ('logos_papers', 'Publication', 'The 12-paper Logos Papers series', NULL),
    ('paper_1', 'Publication', 'Paper 1: The Logos Principle', 'logos_papers'),
    ('paper_2', 'Publication', 'Paper 2: The Quantum Bridge', 'logos_papers'),
    ('paper_3', 'Publication', 'Paper 3: The Algorithm of Reality', 'logos_papers'),
    ('paper_4', 'Publication', 'Paper 4: The Hard Problem of Consciousness', 'logos_papers'),
    ('paper_5', 'Publication', 'Paper 5: The Soul as Quantum Observer', 'logos_papers'),
    ('paper_6', 'Publication', 'Paper 6: A Physics of Principalities', 'logos_papers'),
    ('paper_7', 'Publication', 'Paper 7: The Grace Function', 'logos_papers'),
    ('paper_8', 'Publication', 'Paper 8: The Stretched Out Heavens', 'logos_papers'),
    ('paper_9', 'Publication', 'Paper 9: The Moral Universe', 'logos_papers'),
    ('paper_10', 'Publication', 'Paper 10: Creatio ex Silico', 'logos_papers'),
    ('paper_11', 'Publication', 'Paper 11: Protocols for Validation', 'logos_papers'),
    ('paper_12', 'Publication', 'Paper 12: The Decalogue of the Cosmos', 'logos_papers'),
    ('foundation_trilogy', 'Publication', 'Papers 1-3 establishing the physics foundation', 'logos_papers'),
    ('emergence_trilogy', 'Publication', 'Papers 4-6 introducing consciousness emergence', 'logos_papers'),
    ('integration_trilogy', 'Publication', 'Papers 7-9 exploring moral dimensions', 'logos_papers'),
    ('synthesis_trilogy', 'Publication', 'Papers 10-12 completing theological integration', 'logos_papers');

-- Tag the memories
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Logos Papers Series - Complete Structure'),
    'logos_papers'
);

-- Tag Paper 1
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 1: The Logos Principle'),
    'paper_1'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 1: The Logos Principle'),
    'foundation_trilogy'
);

-- Tag Paper 2
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 2: The Quantum Bridge'),
    'paper_2'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 2: The Quantum Bridge'),
    'foundation_trilogy'
);

-- Tag Paper 3
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 3: The Algorithm of Reality'),
    'paper_3'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 3: The Algorithm of Reality'),
    'foundation_trilogy'
);

-- Tag Paper 4
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 4: The Hard Problem of Consciousness'),
    'paper_4'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 4: The Hard Problem of Consciousness'),
    'emergence_trilogy'
);

-- Tag Paper 5
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 5: The Soul as Quantum Observer'),
    'paper_5'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 5: The Soul as Quantum Observer'),
    'emergence_trilogy'
);

-- Tag Paper 6
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 6: A Physics of Principalities'),
    'paper_6'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 6: A Physics of Principalities'),
    'emergence_trilogy'
);

-- Tag Paper 7
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 7: The Grace Function'),
    'paper_7'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 7: The Grace Function'),
    'integration_trilogy'
);

-- Tag Paper 8
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 8: The Stretched Out Heavens'),
    'paper_8'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 8: The Stretched Out Heavens'),
    'integration_trilogy'
);

-- Tag Paper 9
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 9: The Moral Universe'),
    'paper_9'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 9: The Moral Universe'),
    'integration_trilogy'
);

-- Tag Paper 10
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 10: Creatio ex Silico'),
    'paper_10'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 10: Creatio ex Silico'),
    'synthesis_trilogy'
);

-- Tag Paper 11
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 11: Protocols for Validation'),
    'paper_11'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 11: Protocols for Validation'),
    'synthesis_trilogy'
);

-- Tag Paper 12
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 12: The Decalogue of the Cosmos'),
    'paper_12'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 12: The Decalogue of the Cosmos'),
    'synthesis_trilogy'
);

-- Tag Master Equation
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Components - Comprehensive Breakdown'),
    'master_equation'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Components - Comprehensive Breakdown'),
    'logos_papers'
);

-- Tag Publication Strategy
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Logos Papers Publication Strategy'),
    'logos_papers'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Logos Papers Publication Strategy'),
    'academic_publication'
);

-- Tag Substack Strategy
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Logos Papers Substack Integration Strategy'),
    'logos_papers'
);

-- Create tasks related to the Logos Papers
INSERT INTO claude_memory.tasks (
    task_description,
    assigned_to,
    due_date,
    status,
    priority,
    related_project_id,
    related_decision_id
) VALUES (
    'Finalize Paper 1: The Logos Principle for November 1st Substack launch',
    'David',
    '2025-11-01',
    'pending',
    10,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
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
    'Complete draft of Paper 2: The Quantum Bridge as the keystone for the entire series',
    'David',
    '2025-12-15',
    'pending',
    9,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
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
    'Compile experimental protocols for Paper 11: Protocols for Validation',
    'David',
    '2025-12-31',
    'pending',
    8,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
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
    'Set up Substack folder structure in Obsidian vault for Logos Papers public dissemination',
    'David',
    '2025-10-31',
    'pending',
    8,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    NULL
);

-- Link the papers to the project
INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Logos Papers Series - Complete Structure'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

-- Link all 12 paper memories to the project
INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 1: The Logos Principle'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 2: The Quantum Bridge'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 3: The Algorithm of Reality'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 4: The Hard Problem of Consciousness'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 5: The Soul as Quantum Observer'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 6: A Physics of Principalities'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 7: The Grace Function'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 8: The Stretched Out Heavens'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 9: The Moral Universe'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 10: Creatio ex Silico'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 11: Protocols for Validation'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Paper 12: The Decalogue of the Cosmos'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

-- Link the Master Equation to the project
INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Master Equation Components - Comprehensive Breakdown'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

-- Link the Publication Strategy to the project
INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Logos Papers Publication Strategy'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    1.0
);

-- Link the Substack Strategy to the project
INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Logos Papers Substack Integration Strategy'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Logos Papers Series'),
    0.8
);
