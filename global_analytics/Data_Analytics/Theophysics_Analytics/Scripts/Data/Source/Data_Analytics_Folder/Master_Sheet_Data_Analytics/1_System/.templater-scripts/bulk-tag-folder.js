// Bulk Tag Folder Script
async function bulkTagFolder(tp) {
    // Get all folders
    const folders = app.vault.getAllLoadedFiles()
        .filter(f => f.children)
        .map(f => f.path)
        .sort();
    
    // Let user select folder
    const selectedFolder = await tp.system.suggester(
        folders,
        folders,
        false,
        "Select folder to tag"
    );
    
    if (!selectedFolder) {
        return '';
    }
    
    // Get tags to apply
    const tagInput = await tp.system.prompt("Enter tags (comma-separated, no #)");
    if (!tagInput) {
        return '';
    }
    
    const tags = tagInput.split(',').map(t => t.trim());
    
    // Get all markdown files in folder
    const files = app.vault.getMarkdownFiles()
        .filter(f => f.path.startsWith(selectedFolder));
    
    if (files.length === 0) {
        new Notice('No markdown files in folder!');
        return '';
    }
    
    // Confirm action
    const confirm = await tp.system.suggester(
        ['Yes', 'No'],
        [true, false],
        false,
        `Tag ${files.length} files with: ${tags.join(', ')}?`
    );
    
    if (!confirm) {
        return '';
    }
    
    // Apply tags to each file
    let count = 0;
    for (const file of files) {
        let content = await app.vault.read(file);
        
        // Check for YAML
        const yamlRegex = /^---\n([\s\S]*?)\n---/;
        const yamlMatch = content.match(yamlRegex);
        
        if (yamlMatch) {
            const existingYaml = yamlMatch[1];
            const tagLineRegex = /tags:\s*\[(.*?)\]/;
            
            if (existingYaml.match(tagLineRegex)) {
                // Merge tags
                const existingTags = existingYaml.match(tagLineRegex)[1];
                const mergedTags = existingTags ? `${existingTags}, ${tags.join(', ')}` : tags.join(', ');
                content = content.replace(tagLineRegex, `tags: [${mergedTags}]`);
            } else {
                // Add tags line
                const newYaml = existingYaml + `\ntags: [${tags.join(', ')}]`;
                content = content.replace(yamlRegex, `---\n${newYaml}\n---`);
            }
        } else {
            // Create YAML
            const yaml = `---\ntags: [${tags.join(', ')}]\n---\n\n`;
            content = yaml + content;
        }
        
        await app.vault.modify(file, content);
        count++;
    }
    
    new Notice(`Tagged ${count} files!`);
    return '';
}

module.exports = bulkTagFolder;
