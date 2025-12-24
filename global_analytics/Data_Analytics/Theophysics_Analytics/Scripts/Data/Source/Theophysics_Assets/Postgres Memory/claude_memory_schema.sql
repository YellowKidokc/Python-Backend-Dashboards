-- Claude Memory System Schema Design
-- This schema stores memories from Claude-David conversations, with compression
-- from daily → weekly → monthly for efficient long-term storage.

-- Schema Creation
CREATE SCHEMA IF NOT EXISTS claude_memory;

-- Memory Types table - defines the different types of memories
CREATE TABLE claude_memory.memory_types (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    priority INTEGER NOT NULL DEFAULT 5,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Memory Categories table - organizes memories into categories
CREATE TABLE claude_memory.categories (
    id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    parent_category_id INTEGER REFERENCES claude_memory.categories(id),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Memory Granularity Levels - daily, weekly, monthly
CREATE TABLE claude_memory.granularity_levels (
    id SERIAL PRIMARY KEY,
    level_name VARCHAR(20) NOT NULL UNIQUE,
    description TEXT,
    retention_days INTEGER, -- How many days to retain memories at this level
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Core Memory Items table
CREATE TABLE claude_memory.memory_items (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    memory_type_id INTEGER NOT NULL REFERENCES claude_memory.memory_types(id),
    category_id INTEGER REFERENCES claude_memory.categories(id),
    granularity_id INTEGER NOT NULL REFERENCES claude_memory.granularity_levels(id),
    importance_score INTEGER NOT NULL DEFAULT 5 CHECK (importance_score BETWEEN 1 AND 10),
    related_conversation_id UUID, -- Optional link to conversation
    conversation_url TEXT, -- Optional direct link to Claude conversation
    memory_date DATE NOT NULL, -- When this memory occurred/applies to
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP, -- When this memory should expire (if applicable)
    is_compressed BOOLEAN NOT NULL DEFAULT FALSE, -- Whether this is a compressed memory
    source_memory_ids INTEGER[] -- Array of IDs that were compressed to create this memory
);

-- Memory Tags junction table
CREATE TABLE claude_memory.memory_tags (
    memory_id INTEGER NOT NULL REFERENCES claude_memory.memory_items(id) ON DELETE CASCADE,
    tag_name VARCHAR(50) NOT NULL,
    PRIMARY KEY (memory_id, tag_name)
);

-- Memory Relationships table - for connecting related memories
CREATE TABLE claude_memory.memory_relationships (
    id SERIAL PRIMARY KEY,
    source_memory_id INTEGER NOT NULL REFERENCES claude_memory.memory_items(id) ON DELETE CASCADE,
    target_memory_id INTEGER NOT NULL REFERENCES claude_memory.memory_items(id) ON DELETE CASCADE,
    relationship_type VARCHAR(50) NOT NULL, -- e.g., 'derived_from', 'contradicts', 'supports', etc.
    strength FLOAT NOT NULL DEFAULT 1.0 CHECK (strength BETWEEN 0.0 AND 1.0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(source_memory_id, target_memory_id, relationship_type)
);

-- Projects table - for tracking projects discussed in conversations
CREATE TABLE claude_memory.projects (
    id SERIAL PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) NOT NULL DEFAULT 'active', -- 'active', 'completed', 'paused', etc.
    priority INTEGER NOT NULL DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    start_date DATE,
    target_completion_date DATE,
    actual_completion_date DATE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Memory-Project junction table
CREATE TABLE claude_memory.memory_projects (
    memory_id INTEGER NOT NULL REFERENCES claude_memory.memory_items(id) ON DELETE CASCADE,
    project_id INTEGER NOT NULL REFERENCES claude_memory.projects(id) ON DELETE CASCADE,
    relevance_score FLOAT NOT NULL DEFAULT 1.0 CHECK (relevance_score BETWEEN 0.0 AND 1.0),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (memory_id, project_id)
);

-- Entity Types table - defines types of entities (person, concept, location, etc.)
CREATE TABLE claude_memory.entity_types (
    id SERIAL PRIMARY KEY,
    type_name VARCHAR(50) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Entities table - key entities mentioned in conversations
CREATE TABLE claude_memory.entities (
    id SERIAL PRIMARY KEY,
    entity_name VARCHAR(255) NOT NULL,
    entity_type_id INTEGER NOT NULL REFERENCES claude_memory.entity_types(id),
    description TEXT,
    importance_score INTEGER NOT NULL DEFAULT 5 CHECK (importance_score BETWEEN 1 AND 10),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(entity_name, entity_type_id)
);

-- Memory-Entity junction table
CREATE TABLE claude_memory.memory_entities (
    memory_id INTEGER NOT NULL REFERENCES claude_memory.memory_items(id) ON DELETE CASCADE,
    entity_id INTEGER NOT NULL REFERENCES claude_memory.entities(id) ON DELETE CASCADE,
    mention_count INTEGER NOT NULL DEFAULT 1,
    sentiment_score FLOAT, -- Optional sentiment of mention (-1.0 to 1.0)
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (memory_id, entity_id)
);

-- Decisions table - tracks key decisions made during conversations
CREATE TABLE claude_memory.decisions (
    id SERIAL PRIMARY KEY,
    decision_text TEXT NOT NULL,
    decision_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    memory_id INTEGER REFERENCES claude_memory.memory_items(id) ON DELETE SET NULL,
    related_project_id INTEGER REFERENCES claude_memory.projects(id) ON DELETE SET NULL,
    importance_score INTEGER NOT NULL DEFAULT 5 CHECK (importance_score BETWEEN 1 AND 10),
    decision_status VARCHAR(50) NOT NULL DEFAULT 'active', -- 'active', 'superseded', 'revoked', etc.
    superseded_by_id INTEGER REFERENCES claude_memory.decisions(id),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Actions/Tasks table - tracks required actions discussed in conversations
CREATE TABLE claude_memory.tasks (
    id SERIAL PRIMARY KEY,
    task_description TEXT NOT NULL,
    assigned_to VARCHAR(100),
    due_date DATE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending', -- 'pending', 'completed', 'canceled', etc.
    priority INTEGER NOT NULL DEFAULT 5 CHECK (priority BETWEEN 1 AND 10),
    memory_id INTEGER REFERENCES claude_memory.memory_items(id) ON DELETE SET NULL,
    related_project_id INTEGER REFERENCES claude_memory.projects(id) ON DELETE SET NULL,
    related_decision_id INTEGER REFERENCES claude_memory.decisions(id) ON DELETE SET NULL,
    completed_at TIMESTAMP,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_memory_items_memory_type ON claude_memory.memory_items(memory_type_id);
CREATE INDEX idx_memory_items_category ON claude_memory.memory_items(category_id);
CREATE INDEX idx_memory_items_granularity ON claude_memory.memory_items(granularity_id);
CREATE INDEX idx_memory_items_memory_date ON claude_memory.memory_items(memory_date);
CREATE INDEX idx_memory_items_importance ON claude_memory.memory_items(importance_score);
CREATE INDEX idx_memory_tags_tag_name ON claude_memory.memory_tags(tag_name);
CREATE INDEX idx_memory_relationships_source ON claude_memory.memory_relationships(source_memory_id);
CREATE INDEX idx_memory_relationships_target ON claude_memory.memory_relationships(target_memory_id);
CREATE INDEX idx_memory_projects_project ON claude_memory.memory_projects(project_id);
CREATE INDEX idx_memory_entities_entity ON claude_memory.memory_entities(entity_id);

-- Insert default values for lookup tables
-- Memory Types
INSERT INTO claude_memory.memory_types (type_name, description, priority) VALUES
    ('breakthrough', 'Major insight or discovery', 10),
    ('decision', 'Key decision made during conversation', 9),
    ('concept', 'Important concept discussed', 7),
    ('question', 'Significant question raised', 6),
    ('action_item', 'Task or action to be performed', 8),
    ('preference', 'User preference or working style', 5),
    ('context', 'Background information for reference', 4),
    ('session_summary', 'Summary of entire conversation session', 6);

-- Memory Granularity
INSERT INTO claude_memory.granularity_levels (level_name, description, retention_days) VALUES
    ('daily', 'Daily memories - high detail, short retention', 30),
    ('weekly', 'Weekly compressed memories - medium detail', 90),
    ('monthly', 'Monthly compressed memories - low detail, long retention', 365),
    ('permanent', 'Critical memories never to be removed', NULL);

-- Entity Types
INSERT INTO claude_memory.entity_types (type_name, description) VALUES
    ('person', 'Individual person'),
    ('organization', 'Organization or institution'),
    ('concept', 'Theoretical or abstract concept'),
    ('project', 'Work project or initiative'),
    ('framework', 'Theoretical or methodological framework'),
    ('technology', 'Technology or technical system'),
    ('location', 'Physical or virtual location');

-- Default Categories for Theophysics project
INSERT INTO claude_memory.categories (category_name, description) VALUES
    ('Theophysics', 'Core Theophysics framework and concepts');

INSERT INTO claude_memory.categories (category_name, parent_category_id, description) VALUES
    ('Master Equation', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'The χ equation and related mathematical formulations'),
    ('Universal Laws', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'The 10 Universal Laws and their implications'),
    ('Quantum Dynamics', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Quantum mechanics aspects of the framework'),
    ('Consciousness Studies', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Consciousness integration with physics'),
    ('Biblical Integration', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Connections to Biblical concepts and principles'),
    ('Research Methods', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Methodologies for research and validation'),
    ('Publications', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Papers, articles, and publication strategies'),
    ('Experiments', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Proposed and conducted experiments'),
    ('Breakthrough Machine', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Systems for automating research insights'),
    ('Collaboration', 
     (SELECT id FROM claude_memory.categories WHERE category_name = 'Theophysics'), 
     'Collaboration methods and protocols');

-- Create default projects
INSERT INTO claude_memory.projects (project_name, description, status, priority, start_date) VALUES
    ('Logos Papers Series', 'The 12-paper series for Substack publication', 'active', 10, '2024-10-01'),
    ('Master Equation Database', 'Development of the Master Equation database system', 'active', 8, '2024-09-15'),
    ('Breakthrough Machine', 'Research automation system development', 'active', 9, '2024-08-01'),
    ('Backwards Kingdom', 'Systematic framework exposing inverted cultural truths', 'active', 7, '2024-07-01'),
    ('Theophysics Website', 'Development of the Theophysics website and infrastructure', 'active', 6, '2024-10-01');

-- Add sample entities for the Theophysics framework
INSERT INTO claude_memory.entities (entity_name, entity_type_id, description, importance_score) VALUES
    ('Master Equation', 
     (SELECT id FROM claude_memory.entity_types WHERE type_name = 'concept'), 
     'The central mathematical equation χ = ∭(G⋅M⋅E⋅S⋅T⋅K⋅R⋅Q⋅F⋅C) dx dy dt that unifies physics and theology', 
     10),
    ('David Lowe', 
     (SELECT id FROM claude_memory.entity_types WHERE type_name = 'person'), 
     'Independent researcher and theologian developing the Theophysics framework', 
     10),
    ('Lee', 
     (SELECT id FROM claude_memory.entity_types WHERE type_name = 'person'), 
     'Partner who provides feedback on Theophysics work', 
     8),
    ('Logos Principle', 
     (SELECT id FROM claude_memory.entity_types WHERE type_name = 'concept'), 
     'Foundational principle that information precedes matter and energy', 
     9),
    ('Backwards Kingdom', 
     (SELECT id FROM claude_memory.entity_types WHERE type_name = 'framework'), 
     'Framework exposing how cultural institutions systematically invert divine truth', 
     8);

-- Create views for easy access to memories by different criteria
CREATE VIEW claude_memory.daily_memories AS
SELECT m.*, t.type_name, c.category_name, g.level_name
FROM claude_memory.memory_items m
JOIN claude_memory.memory_types t ON m.memory_type_id = t.id
LEFT JOIN claude_memory.categories c ON m.category_id = c.id
JOIN claude_memory.granularity_levels g ON m.granularity_id = g.id
WHERE g.level_name = 'daily'
ORDER BY m.memory_date DESC, m.importance_score DESC;

CREATE VIEW claude_memory.weekly_memories AS
SELECT m.*, t.type_name, c.category_name, g.level_name
FROM claude_memory.memory_items m
JOIN claude_memory.memory_types t ON m.memory_type_id = t.id
LEFT JOIN claude_memory.categories c ON m.category_id = c.id
JOIN claude_memory.granularity_levels g ON m.granularity_id = g.id
WHERE g.level_name = 'weekly'
ORDER BY m.memory_date DESC, m.importance_score DESC;

CREATE VIEW claude_memory.monthly_memories AS
SELECT m.*, t.type_name, c.category_name, g.level_name
FROM claude_memory.memory_items m
JOIN claude_memory.memory_types t ON m.memory_type_id = t.id
LEFT JOIN claude_memory.categories c ON m.category_id = c.id
JOIN claude_memory.granularity_levels g ON m.granularity_id = g.id
WHERE g.level_name = 'monthly'
ORDER BY m.memory_date DESC, m.importance_score DESC;

CREATE VIEW claude_memory.important_memories AS
SELECT m.*, t.type_name, c.category_name, g.level_name
FROM claude_memory.memory_items m
JOIN claude_memory.memory_types t ON m.memory_type_id = t.id
LEFT JOIN claude_memory.categories c ON m.category_id = c.id
JOIN claude_memory.granularity_levels g ON m.granularity_id = g.id
WHERE m.importance_score >= 8
ORDER BY m.importance_score DESC, m.memory_date DESC;

CREATE VIEW claude_memory.permanent_memories AS
SELECT m.*, t.type_name, c.category_name, g.level_name
FROM claude_memory.memory_items m
JOIN claude_memory.memory_types t ON m.memory_type_id = t.id
LEFT JOIN claude_memory.categories c ON m.category_id = c.id
JOIN claude_memory.granularity_levels g ON m.granularity_id = g.id
WHERE g.level_name = 'permanent'
ORDER BY m.importance_score DESC, m.memory_date DESC;

CREATE VIEW claude_memory.all_decisions AS
SELECT d.*, p.project_name, m.title AS related_memory
FROM claude_memory.decisions d
LEFT JOIN claude_memory.projects p ON d.related_project_id = p.id
LEFT JOIN claude_memory.memory_items m ON d.memory_id = m.id
ORDER BY d.decision_date DESC, d.importance_score DESC;

CREATE VIEW claude_memory.pending_tasks AS
SELECT t.*, p.project_name, d.decision_text, m.title AS related_memory
FROM claude_memory.tasks t
LEFT JOIN claude_memory.projects p ON t.related_project_id = p.id
LEFT JOIN claude_memory.decisions d ON t.related_decision_id = d.id
LEFT JOIN claude_memory.memory_items m ON t.memory_id = m.id
WHERE t.status = 'pending'
ORDER BY t.due_date ASC, t.priority DESC;

-- Create functions for memory management

-- Function to add a daily memory
CREATE OR REPLACE FUNCTION claude_memory.add_daily_memory(
    p_title VARCHAR(255),
    p_content TEXT,
    p_memory_type VARCHAR(50),
    p_category VARCHAR(100),
    p_importance_score INTEGER,
    p_conversation_url TEXT DEFAULT NULL,
    p_tags VARCHAR[] DEFAULT NULL,
    p_related_entities VARCHAR[] DEFAULT NULL,
    p_related_project VARCHAR DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_memory_type_id INTEGER;
    v_category_id INTEGER;
    v_granularity_id INTEGER;
    v_memory_id INTEGER;
    v_project_id INTEGER;
    v_entity_id INTEGER;
    v_tag VARCHAR;
BEGIN
    -- Get IDs from lookup tables
    SELECT id INTO v_memory_type_id FROM claude_memory.memory_types 
    WHERE type_name = p_memory_type;
    
    IF v_memory_type_id IS NULL THEN
        RAISE EXCEPTION 'Invalid memory type: %', p_memory_type;
    END IF;
    
    SELECT id INTO v_category_id FROM claude_memory.categories 
    WHERE category_name = p_category;
    
    SELECT id INTO v_granularity_id FROM claude_memory.granularity_levels 
    WHERE level_name = 'daily';
    
    -- Insert the memory item
    INSERT INTO claude_memory.memory_items (
        title,
        content,
        memory_type_id,
        category_id,
        granularity_id,
        importance_score,
        conversation_url,
        memory_date
    ) VALUES (
        p_title,
        p_content,
        v_memory_type_id,
        v_category_id,
        v_granularity_id,
        p_importance_score,
        p_conversation_url,
        CURRENT_DATE
    ) RETURNING id INTO v_memory_id;
    
    -- Add tags if provided
    IF p_tags IS NOT NULL THEN
        FOREACH v_tag IN ARRAY p_tags LOOP
            INSERT INTO claude_memory.memory_tags (memory_id, tag_name)
            VALUES (v_memory_id, v_tag);
        END LOOP;
    END IF;
    
    -- Add entities if provided
    IF p_related_entities IS NOT NULL THEN
        FOREACH v_tag IN ARRAY p_related_entities LOOP
            SELECT id INTO v_entity_id FROM claude_memory.entities 
            WHERE entity_name = v_tag;
            
            IF v_entity_id IS NOT NULL THEN
                INSERT INTO claude_memory.memory_entities (memory_id, entity_id)
                VALUES (v_memory_id, v_entity_id);
            END IF;
        END LOOP;
    END IF;
    
    -- Link to project if provided
    IF p_related_project IS NOT NULL THEN
        SELECT id INTO v_project_id FROM claude_memory.projects 
        WHERE project_name = p_related_project;
        
        IF v_project_id IS NOT NULL THEN
            INSERT INTO claude_memory.memory_projects (memory_id, project_id)
            VALUES (v_memory_id, v_project_id);
        END IF;
    END IF;
    
    RETURN v_memory_id;
END;
$$ LANGUAGE plpgsql;

-- Function to compress daily memories into a weekly memory
CREATE OR REPLACE FUNCTION claude_memory.compress_to_weekly(
    p_start_date DATE,
    p_end_date DATE,
    p_category VARCHAR(100) DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_daily_granularity_id INTEGER;
    v_weekly_granularity_id INTEGER;
    v_category_id INTEGER;
    v_weekly_memory_id INTEGER;
    v_daily_memory_ids INTEGER[];
    v_compressed_content TEXT;
    v_title VARCHAR(255);
BEGIN
    -- Get granularity IDs
    SELECT id INTO v_daily_granularity_id FROM claude_memory.granularity_levels 
    WHERE level_name = 'daily';
    
    SELECT id INTO v_weekly_granularity_id FROM claude_memory.granularity_levels 
    WHERE level_name = 'weekly';
    
    -- Get category ID if provided
    IF p_category IS NOT NULL THEN
        SELECT id INTO v_category_id FROM claude_memory.categories 
        WHERE category_name = p_category;
    END IF;
    
    -- Get daily memory IDs to compress
    SELECT array_agg(id) INTO v_daily_memory_ids
    FROM claude_memory.memory_items
    WHERE granularity_id = v_daily_granularity_id
    AND memory_date BETWEEN p_start_date AND p_end_date
    AND (p_category IS NULL OR category_id = v_category_id);
    
    -- Generate compressed content from daily memories
    SELECT string_agg(content, E'\n\n') INTO v_compressed_content
    FROM claude_memory.memory_items
    WHERE id = ANY(v_daily_memory_ids)
    ORDER BY importance_score DESC;
    
    -- Create title for weekly memory
    v_title := 'Weekly Summary: ' || to_char(p_start_date, 'YYYY-MM-DD') || 
               ' to ' || to_char(p_end_date, 'YYYY-MM-DD');
    IF p_category IS NOT NULL THEN
        v_title := v_title || ' (' || p_category || ')';
    END IF;
    
    -- Insert the weekly memory
    INSERT INTO claude_memory.memory_items (
        title,
        content,
        memory_type_id,
        category_id,
        granularity_id,
        importance_score,
        memory_date,
        is_compressed,
        source_memory_ids
    ) VALUES (
        v_title,
        v_compressed_content,
        (SELECT id FROM claude_memory.memory_types WHERE type_name = 'session_summary'),
        v_category_id,
        v_weekly_granularity_id,
        7, -- Default importance for compressed memories
        p_end_date,
        TRUE,
        v_daily_memory_ids
    ) RETURNING id INTO v_weekly_memory_id;
    
    RETURN v_weekly_memory_id;
END;
$$ LANGUAGE plpgsql;

-- Function to compress weekly memories into a monthly memory
CREATE OR REPLACE FUNCTION claude_memory.compress_to_monthly(
    p_year INTEGER,
    p_month INTEGER,
    p_category VARCHAR(100) DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_weekly_granularity_id INTEGER;
    v_monthly_granularity_id INTEGER;
    v_category_id INTEGER;
    v_monthly_memory_id INTEGER;
    v_weekly_memory_ids INTEGER[];
    v_compressed_content TEXT;
    v_title VARCHAR(255);
    v_start_date DATE;
    v_end_date DATE;
BEGIN
    -- Calculate start and end dates for the month
    v_start_date := make_date(p_year, p_month, 1);
    v_end_date := (v_start_date + interval '1 month' - interval '1 day')::date;
    
    -- Get granularity IDs
    SELECT id INTO v_weekly_granularity_id FROM claude_memory.granularity_levels 
    WHERE level_name = 'weekly';
    
    SELECT id INTO v_monthly_granularity_id FROM claude_memory.granularity_levels 
    WHERE level_name = 'monthly';
    
    -- Get category ID if provided
    IF p_category IS NOT NULL THEN
        SELECT id INTO v_category_id FROM claude_memory.categories 
        WHERE category_name = p_category;
    END IF;
    
    -- Get weekly memory IDs to compress
    SELECT array_agg(id) INTO v_weekly_memory_ids
    FROM claude_memory.memory_items
    WHERE granularity_id = v_weekly_granularity_id
    AND memory_date BETWEEN v_start_date AND v_end_date
    AND (p_category IS NULL OR category_id = v_category_id);
    
    -- Generate compressed content from weekly memories
    SELECT string_agg(content, E'\n\n') INTO v_compressed_content
    FROM claude_memory.memory_items
    WHERE id = ANY(v_weekly_memory_ids)
    ORDER BY importance_score DESC;
    
    -- Create title for monthly memory
    v_title := 'Monthly Summary: ' || to_char(v_start_date, 'YYYY-MM');
    IF p_category IS NOT NULL THEN
        v_title := v_title || ' (' || p_category || ')';
    END IF;
    
    -- Insert the monthly memory
    INSERT INTO claude_memory.memory_items (
        title,
        content,
        memory_type_id,
        category_id,
        granularity_id,
        importance_score,
        memory_date,
        is_compressed,
        source_memory_ids
    ) VALUES (
        v_title,
        v_compressed_content,
        (SELECT id FROM claude_memory.memory_types WHERE type_name = 'session_summary'),
        v_category_id,
        v_monthly_granularity_id,
        6, -- Default importance for compressed memories
        v_end_date,
        TRUE,
        v_weekly_memory_ids
    ) RETURNING id INTO v_monthly_memory_id;
    
    RETURN v_monthly_memory_id;
END;
$$ LANGUAGE plpgsql;

-- Function to add a decision
CREATE OR REPLACE FUNCTION claude_memory.add_decision(
    p_decision_text TEXT,
    p_importance_score INTEGER,
    p_related_project VARCHAR DEFAULT NULL,
    p_related_memory_id INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_decision_id INTEGER;
    v_project_id INTEGER;
BEGIN
    -- Get project ID if provided
    IF p_related_project IS NOT NULL THEN
        SELECT id INTO v_project_id FROM claude_memory.projects 
        WHERE project_name = p_related_project;
    END IF;
    
    -- Insert the decision
    INSERT INTO claude_memory.decisions (
        decision_text,
        importance_score,
        related_project_id,
        memory_id
    ) VALUES (
        p_decision_text,
        p_importance_score,
        v_project_id,
        p_related_memory_id
    ) RETURNING id INTO v_decision_id;
    
    RETURN v_decision_id;
END;
$$ LANGUAGE plpgsql;

-- Function to add a task
CREATE OR REPLACE FUNCTION claude_memory.add_task(
    p_task_description TEXT,
    p_assigned_to VARCHAR DEFAULT NULL,
    p_due_date DATE DEFAULT NULL,
    p_priority INTEGER DEFAULT 5,
    p_related_project VARCHAR DEFAULT NULL,
    p_related_decision_id INTEGER DEFAULT NULL,
    p_related_memory_id INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
DECLARE
    v_task_id INTEGER;
    v_project_id INTEGER;
BEGIN
    -- Get project ID if provided
    IF p_related_project IS NOT NULL THEN
        SELECT id INTO v_project_id FROM claude_memory.projects 
        WHERE project_name = p_related_project;
    END IF;
    
    -- Insert the task
    INSERT INTO claude_memory.tasks (
        task_description,
        assigned_to,
        due_date,
        priority,
        related_project_id,
        related_decision_id,
        memory_id
    ) VALUES (
        p_task_description,
        p_assigned_to,
        p_due_date,
        p_priority,
        v_project_id,
        p_related_decision_id,
        p_related_memory_id
    ) RETURNING id INTO v_task_id;
    
    RETURN v_task_id;
END;
$$ LANGUAGE plpgsql;

-- Function to search memories by keywords
CREATE OR REPLACE FUNCTION claude_memory.search_memories(
    p_query TEXT,
    p_category VARCHAR DEFAULT NULL,
    p_memory_type VARCHAR DEFAULT NULL,
    p_start_date DATE DEFAULT NULL,
    p_end_date DATE DEFAULT NULL,
    p_min_importance INTEGER DEFAULT 1
) RETURNS TABLE (
    id INTEGER,
    title VARCHAR,
    content TEXT,
    memory_type VARCHAR,
    category VARCHAR,
    granularity VARCHAR,
    importance_score INTEGER,
    memory_date DATE,
    created_at TIMESTAMP,
    is_compressed BOOLEAN,
    relevance FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        m.id,
        m.title,
        m.content,
        mt.type_name AS memory_type,
        c.category_name AS category,
        g.level_name AS granularity,
        m.importance_score,
        m.memory_date,
        m.created_at,
        m.is_compressed,
        ts_rank_cd(
            setweight(to_tsvector('english', coalesce(m.title,'')), 'A') ||
            setweight(to_tsvector('english', coalesce(m.content,'')), 'B'),
            plainto_tsquery('english', p_query)
        ) AS relevance
    FROM claude_memory.memory_items m
    JOIN claude_memory.memory_types mt ON m.memory_type_id = mt.id
    LEFT JOIN claude_memory.categories c ON m.category_id = c.id
    JOIN claude_memory.granularity_levels g ON m.granularity_id = g.id
    WHERE (
        to_tsvector('english', coalesce(m.title,'')) || 
        to_tsvector('english', coalesce(m.content,''))
    ) @@ plainto_tsquery('english', p_query)
    AND (p_category IS NULL OR c.category_name = p_category)
    AND (p_memory_type IS NULL OR mt.type_name = p_memory_type)
    AND (p_start_date IS NULL OR m.memory_date >= p_start_date)
    AND (p_end_date IS NULL OR m.memory_date <= p_end_date)
    AND m.importance_score >= p_min_importance
    ORDER BY relevance DESC;
END;
$$ LANGUAGE plpgsql;
