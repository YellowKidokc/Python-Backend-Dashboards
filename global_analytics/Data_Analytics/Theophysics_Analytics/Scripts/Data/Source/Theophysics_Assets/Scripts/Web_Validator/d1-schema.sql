-- ============================================================================
-- THEOPHYSICS VALIDATOR - D1 DATABASE SCHEMA
-- Cloudflare D1 (SQLite) Compatible
-- Created: 2025-11-11
-- ============================================================================

-- Drop tables if they exist (for clean reinstall)
DROP TABLE IF EXISTS validations;
DROP TABLE IF EXISTS analytics_events;

-- ============================================================================
-- VALIDATIONS TABLE
-- Stores all equation validation attempts
-- ============================================================================

CREATE TABLE validations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Equation data
    equation TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('success', 'error')),
    message TEXT NOT NULL,
    category TEXT,
    latex TEXT,

    -- Verification
    signature TEXT NOT NULL,

    -- Source tracking
    institution TEXT,
    country TEXT,
    ip_hash TEXT NOT NULL,  -- SHA-256 hashed IP for privacy
    user_agent TEXT,

    -- Context (optional)
    context TEXT,

    -- Timestamp
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    -- Indexes
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX idx_validations_status ON validations(status);
CREATE INDEX idx_validations_institution ON validations(institution);
CREATE INDEX idx_validations_category ON validations(category);
CREATE INDEX idx_validations_timestamp ON validations(timestamp);
CREATE INDEX idx_validations_country ON validations(country);

-- ============================================================================
-- ANALYTICS EVENTS TABLE
-- Tracks detailed user interactions
-- ============================================================================

CREATE TABLE analytics_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Event details
    event_type TEXT NOT NULL,  -- 'page_view', 'validation', 'download', etc.
    event_data TEXT,           -- JSON blob with additional data

    -- User tracking
    session_id TEXT,
    ip_hash TEXT NOT NULL,
    user_agent TEXT,
    referrer TEXT,

    -- Location
    country TEXT,
    city TEXT,

    -- Timestamp
    timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX idx_events_type ON analytics_events(event_type);
CREATE INDEX idx_events_timestamp ON analytics_events(timestamp);
CREATE INDEX idx_events_session ON analytics_events(session_id);

-- ============================================================================
-- SAMPLE DATA (for testing)
-- ============================================================================

-- Insert some sample validations
INSERT INTO validations (equation, status, message, category, latex, signature, institution, country, ip_hash, user_agent, timestamp)
VALUES
('chi**2 - alpha*chi + G(t)', 'success', 'Validated as logos field equation', 'logos_field',
 '\\chi^2 - \\alpha \\cdot \\chi + G(t)',
 'sha256:abc123def456...', 'MIT', 'US',
 'hash_12345', 'Mozilla/5.0', '2025-11-10 10:00:00'),

('dchi/dt = -alpha*chi + G(t, psi)', 'success', 'Validated as grace function equation', 'grace_function',
 '\\frac{d\\chi}{dt} = -\\alpha \\cdot \\chi + G(t, \\psi)',
 'sha256:def456ghi789...', 'Harvard University', 'US',
 'hash_67890', 'Mozilla/5.0', '2025-11-10 11:30:00'),

('psi_S**2 + m_S**2', 'success', 'Validated as soul field equation', 'soul_field',
 '\\psi_S^2 + m_S^2',
 'sha256:ghi789jkl012...', 'Stanford', 'US',
 'hash_abcde', 'Mozilla/5.0', '2025-11-10 13:45:00'),

('invalid equation!!!', 'error', 'Equation contains potentially dangerous patterns', NULL, NULL,
 'sha256:jkl012mno345...', 'Independent Researcher', 'GB',
 'hash_fghij', 'Mozilla/5.0', '2025-11-10 15:20:00');

-- ============================================================================
-- VIEWS FOR ANALYTICS
-- ============================================================================

-- View: Success rate by institution
CREATE VIEW v_institution_stats AS
SELECT
    institution,
    COUNT(*) as total_validations,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful_validations,
    ROUND(100.0 * SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate,
    MIN(timestamp) as first_validation,
    MAX(timestamp) as last_validation
FROM validations
WHERE institution IS NOT NULL AND institution != ''
GROUP BY institution
ORDER BY total_validations DESC;

-- View: Daily statistics
CREATE VIEW v_daily_stats AS
SELECT
    DATE(timestamp) as date,
    COUNT(*) as total_validations,
    SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN status = 'error' THEN 1 ELSE 0 END) as errors,
    COUNT(DISTINCT ip_hash) as unique_users,
    COUNT(DISTINCT institution) as unique_institutions
FROM validations
GROUP BY DATE(timestamp)
ORDER BY date DESC;

-- View: Popular equations
CREATE VIEW v_popular_equations AS
SELECT
    equation,
    category,
    COUNT(*) as validation_count,
    COUNT(DISTINCT institution) as tested_by_institutions,
    ROUND(100.0 * SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate,
    MAX(timestamp) as last_tested
FROM validations
GROUP BY equation, category
ORDER BY validation_count DESC;

-- ============================================================================
-- USEFUL QUERIES (as comments for reference)
-- ============================================================================

-- Get top 10 institutions by validation count
-- SELECT * FROM v_institution_stats LIMIT 10;

-- Get validations from last 24 hours
-- SELECT * FROM validations WHERE timestamp >= datetime('now', '-1 day');

-- Get success rate by country
-- SELECT
--   country,
--   COUNT(*) as total,
--   ROUND(100.0 * SUM(CASE WHEN status = 'success' THEN 1 ELSE 0 END) / COUNT(*), 1) as success_rate
-- FROM validations
-- GROUP BY country
-- ORDER BY total DESC;

-- Get hourly validation rate
-- SELECT
--   strftime('%Y-%m-%d %H:00', timestamp) as hour,
--   COUNT(*) as validations
-- FROM validations
-- GROUP BY hour
-- ORDER BY hour DESC
-- LIMIT 24;

-- ============================================================================
-- SCHEMA VERSION
-- ============================================================================

CREATE TABLE schema_version (
    version TEXT PRIMARY KEY,
    applied_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial schema for Theophysics Validator');

-- Success message
SELECT 'Theophysics Validator D1 schema created successfully!' as message;
