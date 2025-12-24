// Quick YAML Insert Script
async function quickYAML(tp) {
    const templates = {
        'Physics Paper': `---
tags: [pillar/physics, logos/field, χ_var/Grace]
paper_id: 
status: draft
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Theology Note': `---
tags: [pillar/theology, logos/grace]
scripture_ref: 
topic: 
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Master Equation Component': `---
tags: [pillar/mathematics, logos/master, math_role/operator]
equation_id: 
component: 
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Miracle Analysis': `---
tags: [pillar/theology, pillar/physics, miracle/healing]
scripture_ref: 
miracle_type: 
physics_mechanism: 
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Experiment Protocol': `---
tags: [pillar/physics, experiment/APCT, χ_var/Coherence]
experiment_id: 
status: Design Phase
priority: High
date: ${tp.date.now("YYYY-MM-DD")}
---`,
        
        'Deep Law': `---
tags: [law/Law01, logos/field, χ_var/Grace]
law_number: 
law_name: 
date: ${tp.date.now("YYYY-MM-DD")}
---`
    };
    
    const selected = await tp.system.suggester(
        Object.keys(templates),
        Object.values(templates),
        false,
        "Select YAML template"
    );
    
    if (!selected) {
        return '';
    }
    
    return selected + '\n\n';
}

module.exports = quickYAML;
