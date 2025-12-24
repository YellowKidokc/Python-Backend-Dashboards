// Insert Master YAML Template Script
async function insertMasterYAML(tp) {
    // Read the YAML Master Template
    const templateFile = app.vault.getAbstractFileByPath('_WORKFLOW/YAML-Master-Template.md');
    if (!templateFile) {
        new Notice('YAML-Master-Template.md not found!');
        return '';
    }
    
    const templateContent = await app.vault.read(templateFile);
    
    // Extract just the YAML block from the template
    const yamlMatch = templateContent.match(/```yaml\n([\s\S]*?)\n```/);
    if (!yamlMatch) {
        new Notice('Could not extract YAML template!');
        return '';
    }
    
    let yaml = yamlMatch[1];
    
    // Auto-fill timestamp fields
    const now = new Date().toISOString();
    yaml = yaml.replace(/\[\[YYYY-MM-DDTHH:MM:SSZ\]\]/g, now);
    
    // Auto-generate UUID
    const uuid = crypto.randomUUID();
    yaml = yaml.replace('[[AUTO_GENERATE_UUID]]', uuid);
    
    // Auto-fill title from filename
    const title = tp.file.title || 'Untitled';
    yaml = yaml.replace('[[Placeholder Title for Your Note/Paper/Research]]', title);
    
    // Prompt for basic metadata
    const status = await tp.system.suggester(
        ['Draft', 'Outline Complete', 'Under Review', 'Published', 'Canonized'],
        ['draft', 'outline_complete', 'under_review', 'published', 'canonized'],
        false,
        "Select document status"
    );
    
    if (status) {
        yaml = yaml.replace('status: "draft"', `status: "${status}"`);
    }
    
    // Prompt for core concept
    const coreConcept = await tp.system.prompt("Enter core concept (or leave blank)");
    if (coreConcept) {
        yaml = yaml.replace(
            '[[Concise statement of the main concept, e.g., Biological Re-Patterning, Grace Function as Dark Energy, Axiom of Ontological Asymmetry, Matter Actualization from Vacuum Energy, Ultimate Entropy Reversal (Resurrection)]]',
            coreConcept
        );
    }
    
    // Prompt for abstract
    const abstract = await tp.system.prompt("Enter abstract summary (or leave blank)");
    if (abstract) {
        yaml = yaml.replace(
            '[[A brief, 2-3 sentence summary of the document\'s main findings/arguments]]',
            abstract
        );
    }
    
    // Ask if this is a miracle analysis
    const isMiracle = await tp.system.suggester(
        ['Yes', 'No'],
        [true, false],
        false,
        "Is this a miracle analysis?"
    );
    
    if (isMiracle) {
        const miracleType = await tp.system.suggester(
            ['Biological Re-patterning', 'Environmental Orchestration', 'Matter Actualization'],
            ['biological_repatterning', 'environmental_orchestration', 'matter_actualization'],
            false,
            "Select miracle sequence type"
        );
        
        if (miracleType) {
            yaml = yaml.replace(
                'sequence_type: ""',
                `sequence_type: "${miracleType}"`
            );
        }
    }
    
    // Ask about pillars
    const pillars = await tp.system.suggester(
        ['Physics', 'Theology', 'Mathematics', 'Consciousness'],
        ['physics', 'theology', 'math', 'consciousness'],
        true,
        "Select relevant pillars (multiple)"
    );
    
    if (pillars && pillars.length > 0) {
        const pillarList = pillars.join(', ');
        yaml = yaml.replace(
            'pillar: []',
            `pillar: [${pillarList}]`
        );
    }
    
    // Ask about χ variables
    const chiVars = await tp.system.suggester(
        ['G (Negentropy/Grace)', 'M (Mutual Information)', 'E (Entropy)', 'S (Self-Reference)', 
         'T (Time)', 'K (Knowledge)', 'R (Relationality)', 'Q (Quantum)', 'F (Faith/Force)', 'C (Coherence)'],
        ['Negentropy', 'MutualInformation', 'Entropy', 'SelfReference', 'Time', 'Knowledge', 'Relationality', 'Quantum', 'Faith', 'Coherence'],
        true,
        "Select relevant χ variables (multiple)"
    );
    
    if (chiVars && chiVars.length > 0) {
        const chiList = chiVars.join(', ');
        yaml = yaml.replace(
            'chi_variable: []',
            `chi_variable: [${chiList}]`
        );
    }
    
    new Notice('Master YAML template inserted with auto-filled fields!');
    return yaml + '\n\n';
}

module.exports = insertMasterYAML;
