// Apply Sample Tags Script
async function applyTags(tp) {
    // Read Tags-Samples.md
    const samplesFile = app.vault.getAbstractFileByPath('_WORKFLOW/Tags-Samples.md');
    if (!samplesFile) {
        new Notice('Tags-Samples.md not found!');
        return '';
    }
    
    const content = await app.vault.read(samplesFile);
    
    // Extract all tags from the reference table
    const tagMatches = content.match(/#[\w\/]+/g) || [];
    const uniqueTags = [...new Set(tagMatches)];
    
    // Let user select tags
    const selectedTags = await tp.system.suggester(
        uniqueTags,
        uniqueTags,
        true, // Allow multiple selection
        "Select tags to apply"
    );
    
    if (!selectedTags || selectedTags.length === 0) {
        return '';
    }
    
    // Format as YAML array
    const tagArray = selectedTags.map(tag => tag.replace('#', '')).join(', ');
    
    // Get current file
    const activeFile = app.workspace.getActiveFile();
    if (!activeFile) {
        new Notice('No active file!');
        return '';
    }
    
    // Read current content
    let fileContent = await app.vault.read(activeFile);
    
    // Check if YAML frontmatter exists
    const yamlRegex = /^---\n([\s\S]*?)\n---/;
    const yamlMatch = fileContent.match(yamlRegex);
    
    if (yamlMatch) {
        // Update existing YAML
        const existingYaml = yamlMatch[1];
        const tagLineRegex = /tags:\s*\[(.*?)\]/;
        
        if (existingYaml.match(tagLineRegex)) {
            // Merge with existing tags
            const existingTags = existingYaml.match(tagLineRegex)[1];
            const mergedTags = existingTags ? `${existingTags}, ${tagArray}` : tagArray;
            fileContent = fileContent.replace(
                tagLineRegex,
                `tags: [${mergedTags}]`
            );
        } else {
            // Add tags line to existing YAML
            const newYaml = existingYaml + `\ntags: [${tagArray}]`;
            fileContent = fileContent.replace(yamlRegex, `---\n${newYaml}\n---`);
        }
    } else {
        // Create new YAML frontmatter
        const yaml = `---\ntags: [${tagArray}]\ndate: ${tp.date.now("YYYY-MM-DD")}\n---\n\n`;
        fileContent = yaml + fileContent;
    }
    
    // Write back to file
    await app.vault.modify(activeFile, fileContent);
    
    new Notice(`Applied ${selectedTags.length} tags!`);
    return '';
}

module.exports = applyTags;
