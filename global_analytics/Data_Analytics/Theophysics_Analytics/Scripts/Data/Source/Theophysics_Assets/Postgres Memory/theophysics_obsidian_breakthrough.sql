-- Obsidian Integration and File Classification Breakthrough
-- This file contains SQL to add memories about the recent breakthrough with Obsidian integration and file classification

-- Add Obsidian breakthrough memories
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
    'Streamlit File Folder Cleaner Breakthrough with MCP Integration',
    'David developed a breakthrough Streamlit application that serves as an intuitive AI file classification system using the Model Context Protocol (MCP). This isn''t just a file classification tool but a complete architecture for domain-driven AI orchestration. The system features an information theory approach (truth density, noise filtering), dynamic classification (not fixed categories), learning from user decisions (building a model of preferences), and full MCP integration for file operations. This system serves as the foundation for the entire Breakthrough Machine architecture and enables domain-driven classification of research materials.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'breakthrough'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Research Methods'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    10,
    NULL,
    'https://claude.ai/chat/ab8010fc-bf63-431a-8f09-35afc19ad700',
    '2025-10-25'
);

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
    'MCP Server Architecture for Theophysics Framework',
    'Developed a comprehensive MCP Server architecture that connects to the File Folder Cleaner at "D:\\Streamlit File Folder Cleaner" and provides 15+ tools for Claude. The integration includes file operations, worker management, memory, and vector operations. The file cleaner integration provides tools for scanning folders (inventory + duplicates + suggestions), organizing files (by type/date/project/AI), cleaning duplicates (smart duplicate handling), reading cleaner code, and listing cleaner files. This creates a complete integration with worker orchestration, memory management, and vector operations all accessible through natural language with Claude.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'project'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Research Methods'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    'https://claude.ai/chat/6822b0bd-725a-4026-a9dd-a5175c4f3c96',
    '2025-10-25'
);

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
    'Ultimate Obsidian Vault Cleaner for Quantum-Spiritual Framework',
    'Developed a specialized Python script called "Ultimate Obsidian Vault Cleaner for David''s Quantum-Spiritual Framework" that organizes and cleans Obsidian vaults. The script includes functionality for deleting confirmed duplicates and organizing framework content into a structured hierarchy including Master Equation, Laws, Trinity, Physics, and Publications categories. This tool addresses the challenge of managing the massive collection of notes, research materials, and documents in the Theophysics framework.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'project'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Research Methods'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    8,
    NULL,
    'https://claude.ai/chat/3df2eac6-ef20-4ace-83eb-1ed9b2735e1a',
    '2025-05-25'
);

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
    'Obsidian Python Files Organization Script',
    'Developed a Python script to organize a large collection of Python files in the "zzz python" folder of the Obsidian vault. The script extracts files from nested subfolders, identifies and combines similar files, and eliminates duplicates. The organization approach uses a phased methodology: 1) Create base folder structure, 2) Extract all files into a single location, 3) Identify similar files for combination, 4) Get user confirmation for each combination, and 5) Delete duplicates.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'project'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Research Methods'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    7,
    NULL,
    'https://claude.ai/chat/c2ac46b0-310d-47b0-8407-a6f6ad1ef0b8',
    '2025-05-25'
);

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
    'Three-Agent Static Architecture for AI Research System',
    'Designed a three-agent static architecture for the AI research system, consisting of: 1) David (framework guardian), 2) Synthesis (integrator), and 3) Claude (orchestrator). This architecture provides the foundation for the dynamic domain-based agents in the Breakthrough Machine. The architecture includes role prompts, search strategies, evaluation criteria, and output formats for each agent, creating a structured prompt library for the system.',
    (SELECT id FROM claude_memory.memory_types WHERE type_name = 'project'),
    (SELECT id FROM claude_memory.categories WHERE category_name = 'Breakthrough Machine'),
    (SELECT id FROM claude_memory.granularity_levels WHERE level_name = 'permanent'),
    9,
    NULL,
    'https://claude.ai/chat/ab8010fc-bf63-431a-8f09-35afc19ad700',
    '2025-10-25'
);

-- Create Obsidian and file management tags
INSERT INTO claude_memory.tags (tag_name, tag_category, description, parent_tag)
VALUES 
    ('obsidian_integration', 'Technology', 'Integration with Obsidian knowledge management system', 'research_methodology'),
    ('file_classification', 'Process', 'Methods for automatically classifying and organizing files', 'research_methodology'),
    ('mcp_integration', 'Technology', 'Model Context Protocol integration for AI systems', 'technical_issue'),
    ('streamlit_app', 'Technology', 'Streamlit-based web applications', 'technical_issue'),
    ('vault_management', 'Process', 'Management of knowledge vaults and repositories', 'research_methodology'),
    ('ai_orchestration', 'Process', 'Orchestration of multiple AI agents for research tasks', 'research_methodology'),
    ('worker_swarm', 'System', 'Coordinated system of AI workers with specialized roles', 'ai_orchestration'),
    ('domain_driven', 'Process', 'Classification and analysis based on domain-specific knowledge', 'file_classification');

-- Tag the memories
SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Streamlit File Folder Cleaner Breakthrough with MCP Integration'),
    'file_classification'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Streamlit File Folder Cleaner Breakthrough with MCP Integration'),
    'mcp_integration'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Streamlit File Folder Cleaner Breakthrough with MCP Integration'),
    'streamlit_app'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Streamlit File Folder Cleaner Breakthrough with MCP Integration'),
    'domain_driven'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'MCP Server Architecture for Theophysics Framework'),
    'mcp_integration'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'MCP Server Architecture for Theophysics Framework'),
    'ai_orchestration'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'MCP Server Architecture for Theophysics Framework'),
    'worker_swarm'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Ultimate Obsidian Vault Cleaner for Quantum-Spiritual Framework'),
    'obsidian_integration'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Ultimate Obsidian Vault Cleaner for Quantum-Spiritual Framework'),
    'vault_management'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Obsidian Python Files Organization Script'),
    'obsidian_integration'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Obsidian Python Files Organization Script'),
    'file_classification'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Three-Agent Static Architecture for AI Research System'),
    'ai_orchestration'
);

SELECT claude_memory.add_tag_to_memory(
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Three-Agent Static Architecture for AI Research System'),
    'worker_swarm'
);

-- Add project for Obsidian and file classification system
INSERT INTO claude_memory.projects (project_name, description, status, priority, start_date) VALUES
    ('Obsidian-MCP Integration', 'Integration of Obsidian with Model Context Protocol for automated research workflows', 'active', 9, '2025-10-20');

-- Link memories to project
INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Streamlit File Folder Cleaner Breakthrough with MCP Integration'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Obsidian-MCP Integration'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'MCP Server Architecture for Theophysics Framework'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Obsidian-MCP Integration'),
    1.0
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Ultimate Obsidian Vault Cleaner for Quantum-Spiritual Framework'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Obsidian-MCP Integration'),
    0.9
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Obsidian Python Files Organization Script'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Obsidian-MCP Integration'),
    0.8
);

INSERT INTO claude_memory.memory_projects (
    memory_id, 
    project_id, 
    relevance_score
) VALUES (
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Three-Agent Static Architecture for AI Research System'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Breakthrough Machine'),
    1.0
);

-- Add decision based on breakthrough
INSERT INTO claude_memory.decisions (
    decision_text,
    decision_date,
    memory_id,
    related_project_id,
    importance_score,
    decision_status
) VALUES (
    'Adopt the Streamlit File Folder Cleaner with MCP integration as the file management foundation for the Breakthrough Machine',
    NOW(),
    (SELECT id FROM claude_memory.memory_items WHERE title = 'Streamlit File Folder Cleaner Breakthrough with MCP Integration'),
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Breakthrough Machine'),
    10,
    'active'
);

-- Add related tasks
INSERT INTO claude_memory.tasks (
    task_description,
    assigned_to,
    due_date,
    status,
    priority,
    related_project_id,
    related_decision_id
) VALUES (
    'Deploy the MCP Server architecture for Theophysics Framework with all 15+ tools',
    'David',
    '2025-11-15',
    'pending',
    9,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Obsidian-MCP Integration'),
    (SELECT id FROM claude_memory.decisions WHERE decision_text LIKE 'Adopt the Streamlit File Folder%')
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
    'Integrate Streamlit File Folder Cleaner with the three-agent static architecture',
    'David',
    '2025-11-30',
    'pending',
    9,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Breakthrough Machine'),
    (SELECT id FROM claude_memory.decisions WHERE decision_text LIKE 'Adopt the Streamlit File Folder%')
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
    'Document the domain classification approach used in the Streamlit app for other researchers',
    'David',
    '2025-12-15',
    'pending',
    7,
    (SELECT id FROM claude_memory.projects WHERE project_name = 'Obsidian-MCP Integration'),
    (SELECT id FROM claude_memory.decisions WHERE decision_text LIKE 'Adopt the Streamlit File Folder%')
);
