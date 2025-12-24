// Parse Pasted Headers Script
async function parseHeaders(tp) {
    // Get clipboard content
    const pasted = await tp.system.clipboard();
    
    if (!pasted) {
        new Notice('Clipboard is empty!');
        return '';
    }
    
    // Extract headers (## Header format)
    const headerRegex = /^#{1,6}\s+(.+)$/gm;
    const headers = [];
    let match;
    
    while ((match = headerRegex.exec(pasted)) !== null) {
        const level = match[0].match(/^#+/)[0].length;
        const text = match[1].trim();
        headers.push({ level, text });
    }
    
    if (headers.length === 0) {
        new Notice('No headers found in clipboard!');
        return pasted; // Return original content
    }
    
    // Build structured output
    let output = `---\ntags: []\ndate: ${tp.date.now("YYYY-MM-DD")}\nsource: imported\n---\n\n`;
    output += `# ${headers[0].text}\n\n`;
    
    // Add table of contents
    output += `## Table of Contents\n\n`;
    for (const header of headers.slice(1)) {
        const indent = '  '.repeat(header.level - 2);
        const link = header.text.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]/g, '');
        output += `${indent}- [[#${link}|${header.text}]]\n`;
    }
    output += `\n---\n\n`;
    
    // Add sections
    for (const header of headers.slice(1)) {
        output += `${'#'.repeat(header.level)} ${header.text}\n\n`;
        output += `<!-- Content for ${header.text} -->\n\n`;
    }
    
    new Notice(`Parsed ${headers.length} headers!`);
    return output;
}

module.exports = parseHeaders;
