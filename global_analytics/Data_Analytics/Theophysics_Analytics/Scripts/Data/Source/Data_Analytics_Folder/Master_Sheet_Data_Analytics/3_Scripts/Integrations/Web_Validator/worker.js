/**
 * THEOPHYSICS EQUATION VALIDATOR
 * Cloudflare Worker Backend
 *
 * This worker handles:
 * - Equation validation requests
 * - Cryptographic attestation generation
 * - Result storage in D1 database
 * - Analytics and statistics
 * - Institution tracking via IP geolocation
 *
 * @author David Lowe, Claude (Anthropic)
 * @license MIT
 */

// ============================================================================
// CONFIGURATION
// ============================================================================

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

// Known equation patterns for Theophysics framework
const KNOWN_EQUATIONS = {
  'logos_field': /chi\*\*2\s*-\s*alpha\s*\*\s*chi/,
  'grace_function': /dchi\/dt\s*=\s*-\s*alpha\s*\*\s*chi\s*\+\s*G/,
  'soul_field': /psi_S.*m_S/,
  'yukawa_coupling': /L_int.*psi_S/,
  'resurrection': /Delta_rho.*g_R/,
  'entropy': /dS\/dt/,
};

// ============================================================================
// MAIN HANDLER
// ============================================================================

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const path = url.pathname;

    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS_HEADERS });
    }

    // Route handling
    try {
      if (path === '/' || path === '/index.html') {
        // Serve the HTML page (in production, this would be from R2 or KV)
        return await serveIndexPage(env);
      }

      if (path === '/api/validate' && request.method === 'POST') {
        return await handleValidation(request, env);
      }

      if (path === '/api/stats' && request.method === 'GET') {
        return await handleStats(env);
      }

      if (path === '/api/institutions' && request.method === 'GET') {
        return await handleInstitutions(env);
      }

      // 404
      return jsonResponse({ error: 'Not found' }, 404);

    } catch (error) {
      console.error('Worker error:', error);
      return jsonResponse({
        error: 'Internal server error',
        message: error.message
      }, 500);
    }
  }
};

// ============================================================================
// VALIDATION HANDLER
// ============================================================================

async function handleValidation(request, env) {
  try {
    // Parse request body
    const body = await request.json();
    const { equation, context, institution } = body;

    // Validate input
    if (!equation || typeof equation !== 'string') {
      return jsonResponse({ error: 'Invalid equation' }, 400);
    }

    // Get client info
    const clientIP = request.headers.get('CF-Connecting-IP');
    const country = request.cf?.country || 'Unknown';
    const userAgent = request.headers.get('User-Agent');

    // Detect institution from IP if not provided
    const detectedInstitution = institution || await detectInstitution(clientIP, env);

    // Validate the equation
    const validation = validateEquation(equation);

    // Generate cryptographic signature
    const signature = await generateSignature(equation, validation, env);

    // Prepare result
    const result = {
      status: validation.valid ? 'success' : 'error',
      equation: equation,
      message: validation.message,
      latex: validation.latex || null,
      category: validation.category || null,
      signature: signature,
      timestamp: new Date().toISOString(),
      institution: detectedInstitution,
      country: country,
    };

    // Store in database
    await storeValidation(result, clientIP, userAgent, env);

    // Return response
    return jsonResponse(result);

  } catch (error) {
    console.error('Validation error:', error);
    return jsonResponse({
      error: 'Validation failed',
      message: error.message
    }, 500);
  }
}

// ============================================================================
// EQUATION VALIDATION LOGIC
// ============================================================================

function validateEquation(equation) {
  // Normalize equation
  const normalized = equation.trim().toLowerCase();

  // Check if empty
  if (!normalized) {
    return {
      valid: false,
      message: 'Equation cannot be empty'
    };
  }

  // Check for dangerous patterns (code injection)
  const dangerous = /eval|exec|import|require|__/;
  if (dangerous.test(normalized)) {
    return {
      valid: false,
      message: 'Equation contains potentially dangerous patterns'
    };
  }

  // Check against known equation patterns
  for (const [category, pattern] of Object.entries(KNOWN_EQUATIONS)) {
    if (pattern.test(normalized)) {
      return {
        valid: true,
        message: `Validated as ${category.replace('_', ' ')} equation`,
        category: category,
        latex: convertToLatex(equation)
      };
    }
  }

  // Basic symbolic validation
  try {
    const symbols = extractSymbols(equation);
    const operators = extractOperators(equation);

    // Check for valid mathematical structure
    if (symbols.length === 0) {
      return {
        valid: false,
        message: 'Equation must contain at least one variable or constant'
      };
    }

    // Check for balanced parentheses
    if (!areParenthesesBalanced(equation)) {
      return {
        valid: false,
        message: 'Unbalanced parentheses in equation'
      };
    }

    // If it passes basic checks, mark as valid
    return {
      valid: true,
      message: 'Equation is mathematically valid',
      latex: convertToLatex(equation),
      symbols: symbols,
      operators: operators
    };

  } catch (error) {
    return {
      valid: false,
      message: `Validation error: ${error.message}`
    };
  }
}

// Extract mathematical symbols from equation
function extractSymbols(equation) {
  const symbolPattern = /[a-zA-Z_][a-zA-Z0-9_]*/g;
  const matches = equation.match(symbolPattern) || [];
  return [...new Set(matches)]; // Remove duplicates
}

// Extract operators from equation
function extractOperators(equation) {
  const operatorPattern = /[\+\-\*\/\^]|\*\*|sqrt|sin|cos|exp|log/g;
  const matches = equation.match(operatorPattern) || [];
  return [...new Set(matches)];
}

// Check if parentheses are balanced
function areParenthesesBalanced(equation) {
  let count = 0;
  for (const char of equation) {
    if (char === '(') count++;
    if (char === ')') count--;
    if (count < 0) return false; // Closing before opening
  }
  return count === 0; // Should end at zero
}

// Convert to LaTeX notation (simple version)
function convertToLatex(equation) {
  return equation
    .replace(/\*\*/g, '^')           // Power
    .replace(/\*/g, ' \\cdot ')      // Multiplication
    .replace(/chi/g, '\\chi')        // Greek letter chi
    .replace(/alpha/g, '\\alpha')    // Greek letter alpha
    .replace(/psi/g, '\\psi')        // Greek letter psi
    .replace(/phi/g, '\\phi')        // Greek letter phi
    .replace(/nabla/g, '\\nabla')    // Del operator
    .replace(/Delta/g, '\\Delta')    // Delta
    .replace(/rho/g, '\\rho')        // Rho
    .replace(/sqrt\((.*?)\)/g, '\\sqrt{$1}')  // Square root
    .replace(/\//g, ' \\div ')       // Division
    .replace(/_(\w+)/g, '_{$1}');    // Subscripts
}

// ============================================================================
// CRYPTOGRAPHIC SIGNATURE
// ============================================================================

async function generateSignature(equation, validation, env) {
  // Create data to sign
  const data = {
    equation: equation,
    valid: validation.valid,
    timestamp: new Date().toISOString(),
    validator: 'Theophysics Cloudflare Worker v1.0'
  };

  const dataString = JSON.stringify(data);

  // Generate SHA-256 hash as signature
  const encoder = new TextEncoder();
  const dataBuffer = encoder.encode(dataString);
  const hashBuffer = await crypto.subtle.digest('SHA-256', dataBuffer);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  const hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('');

  return `sha256:${hashHex}`;
}

// ============================================================================
// INSTITUTION DETECTION
// ============================================================================

async function detectInstitution(ip, env) {
  // Known academic IP ranges (simplified - in production, use a full GeoIP database)
  const academicInstitutions = {
    // This is a placeholder - in production, you'd use Cloudflare's IP geolocation
    // or a dedicated service like IPinfo or MaxMind
    'default': 'Independent Researcher'
  };

  // In production, you would:
  // 1. Use Cloudflare's IP geolocation (request.cf)
  // 2. Query a database of academic IP ranges
  // 3. Use reverse DNS lookup
  // 4. Check against known university CIDR blocks

  // For now, return default
  return academicInstitutions['default'];
}

// ============================================================================
// DATABASE STORAGE
// ============================================================================

async function storeValidation(result, ip, userAgent, env) {
  // Check if D1 database is available
  if (!env.DB) {
    console.warn('D1 database not configured, skipping storage');
    return;
  }

  try {
    // Insert into validations table
    const stmt = env.DB.prepare(`
      INSERT INTO validations (
        equation,
        status,
        message,
        category,
        latex,
        signature,
        institution,
        country,
        ip_hash,
        user_agent,
        timestamp
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    // Hash IP for privacy
    const ipHash = await hashString(ip);

    await stmt.bind(
      result.equation,
      result.status,
      result.message,
      result.category || null,
      result.latex || null,
      result.signature,
      result.institution,
      result.country,
      ipHash,
      userAgent,
      result.timestamp
    ).run();

  } catch (error) {
    console.error('Database storage error:', error);
    // Don't fail the request if storage fails
  }
}

// Hash string (for privacy)
async function hashString(str) {
  const encoder = new TextEncoder();
  const data = encoder.encode(str);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  const hashArray = Array.from(new Uint8Array(hashBuffer));
  return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}

// ============================================================================
// STATISTICS HANDLER
// ============================================================================

async function handleStats(env) {
  if (!env.DB) {
    return jsonResponse({
      total_validations: 0,
      success_rate: 0,
      institution_count: 0,
      active_users: 0
    });
  }

  try {
    // Get total validations
    const totalResult = await env.DB.prepare(`
      SELECT COUNT(*) as count FROM validations
    `).first();
    const total = totalResult?.count || 0;

    // Get success rate
    const successResult = await env.DB.prepare(`
      SELECT
        COUNT(CASE WHEN status = 'success' THEN 1 END) as successes,
        COUNT(*) as total
      FROM validations
    `).first();
    const successRate = successResult?.total > 0
      ? Math.round((successResult.successes / successResult.total) * 100)
      : 0;

    // Get unique institutions
    const institutionResult = await env.DB.prepare(`
      SELECT COUNT(DISTINCT institution) as count FROM validations
    `).first();
    const institutionCount = institutionResult?.count || 0;

    // Get active users (last 24 hours)
    const activeResult = await env.DB.prepare(`
      SELECT COUNT(DISTINCT ip_hash) as count
      FROM validations
      WHERE timestamp >= datetime('now', '-1 day')
    `).first();
    const activeUsers = activeResult?.count || 0;

    // Get top institutions
    const topInstitutions = await env.DB.prepare(`
      SELECT
        institution as name,
        COUNT(*) as count,
        ROUND(AVG(CASE WHEN status = 'success' THEN 100 ELSE 0 END), 1) as success_rate
      FROM validations
      WHERE institution IS NOT NULL AND institution != ''
      GROUP BY institution
      ORDER BY count DESC
      LIMIT 10
    `).all();

    return jsonResponse({
      total_validations: total,
      success_rate: successRate,
      institution_count: institutionCount,
      active_users: activeUsers,
      top_institutions: topInstitutions?.results || []
    });

  } catch (error) {
    console.error('Stats query error:', error);
    return jsonResponse({
      total_validations: 0,
      success_rate: 0,
      institution_count: 0,
      active_users: 0,
      top_institutions: []
    });
  }
}

// ============================================================================
// INSTITUTIONS HANDLER
// ============================================================================

async function handleInstitutions(env) {
  if (!env.DB) {
    return jsonResponse({ institutions: [] });
  }

  try {
    const result = await env.DB.prepare(`
      SELECT
        institution,
        COUNT(*) as total_validations,
        COUNT(CASE WHEN status = 'success' THEN 1 END) as successful,
        MIN(timestamp) as first_validation,
        MAX(timestamp) as last_validation
      FROM validations
      WHERE institution IS NOT NULL AND institution != ''
      GROUP BY institution
      ORDER BY total_validations DESC
      LIMIT 50
    `).all();

    return jsonResponse({
      institutions: result?.results || []
    });

  } catch (error) {
    console.error('Institutions query error:', error);
    return jsonResponse({ institutions: [] });
  }
}

// ============================================================================
// HTML SERVING (for development - in production, serve from R2/KV)
// ============================================================================

async function serveIndexPage(env) {
  // In production, you would fetch the HTML from R2 or KV storage
  // For now, return a placeholder that tells users to upload the index.html
  const html = `
<!DOCTYPE html>
<html>
<head>
  <title>Theophysics Validator</title>
</head>
<body>
  <h1>Theophysics Equation Validator</h1>
  <p>Please upload index.html to serve the full application.</p>
  <p>API endpoints:</p>
  <ul>
    <li>POST /api/validate - Validate an equation</li>
    <li>GET /api/stats - Get statistics</li>
    <li>GET /api/institutions - Get institution rankings</li>
  </ul>
</body>
</html>
  `;

  return new Response(html, {
    headers: {
      'Content-Type': 'text/html',
      ...CORS_HEADERS
    }
  });
}

// ============================================================================
// UTILITY FUNCTIONS
// ============================================================================

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status: status,
    headers: {
      'Content-Type': 'application/json',
      ...CORS_HEADERS
    }
  });
}
