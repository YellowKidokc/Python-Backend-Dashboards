// Find Untagged Notes Script
async function findUntagged(tp) {
    // Get all markdown files
    const allFiles = app.vault.getMarkdownFiles();
    const untagged = [];
    
    // Check each file for tags
    for (const file of allFiles) {
        const cache = app.metadataCache.getFileCache(file);
        const hasTags = cache?.frontmatter?.tags || cache?.tags;
        
        if (!hasTags || (Array.isArray(hasTags) && hasTags.length === 0)) {
            untagged.push(file);
        }
    }
    
    if (untagged.length === 0) {
        new Notice('All notes are tagged! 🎉');
        return '';
    }
    
    // Build report
    let report = `# Untagged Notes Report\n\n`;
    report += `**Total Untagged**: ${untagged.length}\n`;
    report += `**Date**: ${tp.date.now("YYYY-MM-DD HH:mm")}\n\n`;
    report += `---\n\n`;
    
    // Group by folder
    const byFolder = {};
    for (const file of untagged) {
        const folder = file.parent.path || 'Root';
        if (!byFolder[folder]) {
            byFolder[folder] = [];
        }
        byFolder[folder].push(file);
    }
    
    // Add to report
    for (const [folder, files] of Object.entries(byFolder).sort()) {
        report += `## ${folder} (${files.length})\n\n`;
        for (const file of files) {
            report += `- [[${file.basename}]]\n`;
        }
        report += `\n`;
    }
    
    new Notice(`Found ${untagged.length} untagged notes!`);
    return report;
}

module.exports = findUntagged;
